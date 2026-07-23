from models.user import Usuario
from services.facial_recognition_service import FacialRecognitionError, FacialRecognitionService

class AuthController:
    def __init__(self):
        self.user_model = Usuario()
        self.face_service = FacialRecognitionService()

    def autenticar(self, usuario, password):
        return self.user_model.validar_login(usuario, password)

    def registrar_rostro(self, user_session):
        id_usuario = user_session.get("id_usuario")
        nombre = user_session.get("nombre_usuario", "usuario")

        if not id_usuario:
            raise FacialRecognitionError("No se encontró el usuario autenticado.")

        capturas = self.face_service.capturar_rostro_usuario(id_usuario, nombre)
        self.user_model.activar_rostro(id_usuario)
        return capturas

    def autenticar_con_rostro(self):
        id_usuario, confianza = self.face_service.reconocer_usuario()

        if id_usuario is None or confianza is None:
            return None, "Rostro no reconocido. Inicie sesión con usuario y contraseña."

        if confianza > self.face_service.confidence_limit:
            return None, "Rostro no reconocido. Inicie sesión con usuario y contraseña."

        datos_usuario = self.user_model.obtener_por_id(id_usuario)
        if not datos_usuario:
            return None, "El rostro coincide con un usuario que no existe en la base de datos."

        if len(datos_usuario) >= 4 and int(datos_usuario[3]) != 1:
            return None, "El usuario reconocido no tiene el login facial activo."

        return datos_usuario, None
