from pathlib import Path
import re
import time


class FacialRecognitionError(Exception):
    pass


class FacialRecognitionService:
    def __init__(self, base_dir=None):
        self.project_root = Path(base_dir or Path(__file__).resolve().parents[1])
        self.faces_dir = self.project_root / "data" / "rostros"
        self.classifier_path = self.project_root / "data" / "clasificador.yml"
        self.face_size = (150, 150)
        self.samples_per_user = 30
        self.confidence_limit = 70

    def _load_cv2(self):
        try:
            import cv2
        except ImportError as exc:
            raise FacialRecognitionError(
                "OpenCV no está instalado. Instale opencv-contrib-python para usar el reconocimiento facial."
            ) from exc

        if not hasattr(cv2, "face") or not hasattr(cv2.face, "LBPHFaceRecognizer_create"):
            raise FacialRecognitionError(
                "La instalación de OpenCV no incluye el reconocedor facial LBPH. Instale opencv-contrib-python."
            )

        return cv2

    def _face_detector(self, cv2):
        cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(str(cascade_path))
        if detector.empty():
            raise FacialRecognitionError("No se pudo cargar el detector de rostros de OpenCV.")
        return detector

    def capturar_rostro_usuario(self, id_usuario, nombre_usuario="usuario"):
        cv2 = self._load_cv2()
        detector = self._face_detector(cv2)
        self.faces_dir.mkdir(parents=True, exist_ok=True)

        camara = cv2.VideoCapture(0)
        if not camara.isOpened():
            raise FacialRecognitionError("No se pudo abrir la cámara.")

        capturas = 0
        try:
            while capturas < self.samples_per_user:
                ok, frame = camara.read()
                if not ok:
                    continue

                gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rostros = detector.detectMultiScale(gris, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))

                for (x, y, w, h) in rostros:
                    rostro = gris[y:y + h, x:x + w]
                    rostro = cv2.resize(rostro, self.face_size)
                    capturas += 1
                    archivo = self.faces_dir / f"user_{int(id_usuario)}_{capturas}.jpg"
                    cv2.imwrite(str(archivo), rostro)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (46, 204, 113), 2)
                    cv2.putText(
                        frame,
                        f"Capturando {capturas}/{self.samples_per_user}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (46, 204, 113),
                        2,
                    )
                    break

                cv2.putText(
                    frame,
                    f"Usuario: {nombre_usuario}",
                    (10, frame.shape[0] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )
                cv2.imshow("Registro facial - presione Q para cancelar", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    raise FacialRecognitionError("Registro facial cancelado por el usuario.")
        finally:
            camara.release()
            cv2.destroyAllWindows()

        self.entrenar_clasificador()
        return capturas

    def entrenar_clasificador(self):
        cv2 = self._load_cv2()
        self.faces_dir.mkdir(parents=True, exist_ok=True)

        rostros = []
        ids = []
        patron = re.compile(r"user_(\d+)_\d+\.jpg$", re.IGNORECASE)

        for archivo in self.faces_dir.glob("user_*_*.jpg"):
            match = patron.match(archivo.name)
            if not match:
                continue
            imagen = cv2.imread(str(archivo), cv2.IMREAD_GRAYSCALE)
            if imagen is None:
                continue
            rostros.append(cv2.resize(imagen, self.face_size))
            ids.append(int(match.group(1)))

        if not rostros:
            raise FacialRecognitionError("No existen imágenes faciales para entrenar el clasificador.")

        try:
            import numpy as np
        except ImportError as exc:
            raise FacialRecognitionError("NumPy es necesario para entrenar el reconocimiento facial.") from exc

        reconocedor = cv2.face.LBPHFaceRecognizer_create()
        reconocedor.train(rostros, np.array(ids, dtype="int32"))
        self.classifier_path.parent.mkdir(parents=True, exist_ok=True)
        reconocedor.write(str(self.classifier_path))

    def reconocer_usuario(self, timeout_seconds=15):
        cv2 = self._load_cv2()
        detector = self._face_detector(cv2)

        if not self.classifier_path.exists():
            raise FacialRecognitionError("Aún no existe un clasificador facial entrenado.")

        reconocedor = cv2.face.LBPHFaceRecognizer_create()
        reconocedor.read(str(self.classifier_path))

        camara = cv2.VideoCapture(0)
        if not camara.isOpened():
            raise FacialRecognitionError("No se pudo abrir la cámara.")

        inicio = time.time()
        mejor_id = None
        mejor_confianza = 999

        try:
            while time.time() - inicio < timeout_seconds:
                ok, frame = camara.read()
                if not ok:
                    continue

                gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rostros = detector.detectMultiScale(gris, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))

                for (x, y, w, h) in rostros:
                    rostro = gris[y:y + h, x:x + w]
                    rostro = cv2.resize(rostro, self.face_size)
                    id_encontrado, confianza = reconocedor.predict(rostro)

                    if confianza < mejor_confianza:
                        mejor_id = id_encontrado
                        mejor_confianza = confianza

                    color = (46, 204, 113) if confianza <= self.confidence_limit else (231, 76, 60)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(
                        frame,
                        f"Confianza: {confianza:.1f}",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2,
                    )

                    if confianza <= self.confidence_limit:
                        return int(id_encontrado), float(confianza)

                cv2.imshow("Login facial - presione Q para cancelar", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    raise FacialRecognitionError("Login facial cancelado por el usuario.")
        finally:
            camara.release()
            cv2.destroyAllWindows()

        if mejor_id is not None:
            return int(mejor_id), float(mejor_confianza)
        return None, None
