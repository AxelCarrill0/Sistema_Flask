import tkinter as tk
from tkinter import messagebox

from controllers.auth_controller import AuthController
from services.facial_recognition_service import FacialRecognitionError


class ProfileView(tk.Frame):
    def __init__(self, parent, user_session):
        super().__init__(parent, bg="#f4f6f9")
        self.user_session = user_session
        self.controller = AuthController()
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self._build_ui()

    def _build_ui(self):
        lbl_titulo = tk.Label(
            self,
            text="PERFIL Y SEGURIDAD",
            font=("Helvetica", 14, "bold"),
            bg="#f4f6f9",
            fg="#2c3e50",
        )
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(self, bg="#ffffff", bd=1, relief="solid", padx=20, pady=20)
        card.pack(fill="x")

        nombre = self.user_session.get("nombre_usuario", "Usuario")
        usuario = self.user_session.get("usuario", "")
        rostro_activo = int(self.user_session.get("rostro_activo", 0) or 0)

        tk.Label(
            card,
            text=f"Usuario: {nombre}",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            card,
            text=f"Cuenta: {usuario}",
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#7f8c8d",
        ).pack(anchor="w", pady=(0, 15))

        estado = "Activo" if rostro_activo else "No registrado"
        color = "#27ae60" if rostro_activo else "#c0392b"
        self.lbl_estado = tk.Label(
            card,
            text=f"Login facial: {estado}",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            fg=color,
        )
        self.lbl_estado.pack(anchor="w", pady=(0, 15))

        texto = (
            "El registro facial toma una ráfaga automática de 30 capturas. "
            "Mire a la cámara y mantenga el rostro visible durante el proceso."
        )
        tk.Label(
            card,
            text=texto,
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#34495e",
            wraplength=620,
            justify="left",
        ).pack(anchor="w", pady=(0, 15))

        btn_registrar = tk.Button(
            card,
            text="Registrar / Actualizar Rostro",
            font=("Helvetica", 10, "bold"),
            bg="#1abc9c",
            fg="#ffffff",
            activebackground="#16a085",
            activeforeground="#ffffff",
            cursor="hand2",
            padx=12,
            pady=8,
            command=self._registrar_rostro,
        )
        btn_registrar.pack(anchor="w")

    def _registrar_rostro(self):
        confirmar = messagebox.askyesno(
            "Registrar rostro",
            "Se abrirá la cámara para capturar su rostro. ¿Desea continuar?",
            parent=self,
        )
        if not confirmar:
            return

        try:
            capturas = self.controller.registrar_rostro(self.user_session)
        except FacialRecognitionError as exc:
            messagebox.showerror("Reconocimiento facial", str(exc), parent=self)
            return
        except Exception as exc:
            messagebox.showerror("Reconocimiento facial", f"No se pudo registrar el rostro: {exc}", parent=self)
            return

        self.user_session["rostro_activo"] = 1
        self.lbl_estado.config(text="Login facial: Activo", fg="#27ae60")
        messagebox.showinfo(
            "Reconocimiento facial",
            f"Rostro registrado correctamente con {capturas} capturas.",
            parent=self,
        )
