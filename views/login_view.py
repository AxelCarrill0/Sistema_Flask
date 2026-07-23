import tkinter as tk
from tkinter import ttk

from controllers.auth_controller import AuthController
from services.facial_recognition_service import FacialRecognitionError


class LoginView(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, bg="#f4f6f9")
        self.on_login_success = on_login_success
        self.controller = AuthController()
        self.pack(fill="both", expand=True)

        self._build_ui()

    def _build_ui(self):
        card_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid", padx=30, pady=30)
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        lbl_titulo_sistema = tk.Label(
            card_frame,
            text="SISTEMA DE GESTIÓN Y VENTAS",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
        )
        lbl_titulo_sistema.pack(pady=(0, 5))

        lbl_subtitulo = tk.Label(
            card_frame,
            text="Inicio de Sesión",
            font=("Helvetica", 11),
            bg="#ffffff",
            fg="#7f8c8d",
        )
        lbl_subtitulo.pack(pady=(0, 20))

        lbl_user = tk.Label(
            card_frame,
            text="Usuario:",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            anchor="w",
        )
        lbl_user.pack(fill="x", pady=(5, 2))

        self.ent_user = ttk.Entry(card_frame, font=("Helvetica", 11), width=30)
        self.ent_user.pack(fill="x", pady=(0, 15))
        self.ent_user.focus()

        lbl_pass = tk.Label(
            card_frame,
            text="Contraseña:",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            anchor="w",
        )
        lbl_pass.pack(fill="x", pady=(5, 2))

        self.ent_pass = ttk.Entry(card_frame, font=("Helvetica", 11), show="*", width=30)
        self.ent_pass.pack(fill="x", pady=(0, 20))
        self.ent_pass.bind("<Return>", lambda event: self._login())

        self.lbl_error = tk.Label(
            card_frame,
            text="",
            font=("Helvetica", 9),
            fg="#e74c3c",
            bg="#ffffff",
            wraplength=280,
        )
        self.lbl_error.pack(pady=(0, 10))

        btn_ingresar = tk.Button(
            card_frame,
            text="INGRESAR",
            font=("Helvetica", 10, "bold"),
            bg="#3498db",
            fg="#ffffff",
            activebackground="#2980b9",
            activeforeground="#ffffff",
            cursor="hand2",
            pady=8,
            command=self._login,
        )
        btn_ingresar.pack(fill="x")

        btn_facial = tk.Button(
            card_frame,
            text="INGRESAR CON ROSTRO",
            font=("Helvetica", 10, "bold"),
            bg="#1abc9c",
            fg="#ffffff",
            activebackground="#16a085",
            activeforeground="#ffffff",
            cursor="hand2",
            pady=8,
            command=self._login_facial,
        )
        btn_facial.pack(fill="x", pady=(10, 0))

    def _crear_sesion(self, datos_user):
        return {
            "id_usuario": datos_user[0],
            "nombre_usuario": datos_user[1],
            "usuario": datos_user[2],
            "rostro_activo": datos_user[3] if len(datos_user) > 3 else 0,
        }

    def _login(self):
        usuario = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()

        if not usuario or not password:
            self.lbl_error.config(text="Por favor ingrese usuario y contraseña.")
            return

        datos_user = self.controller.autenticar(usuario, password)

        if datos_user:
            self.lbl_error.config(text="")
            self.on_login_success(self._crear_sesion(datos_user))
        else:
            self.lbl_error.config(text="Usuario o contraseña incorrectos.")

    def _login_facial(self):
        self.lbl_error.config(text="")

        try:
            datos_user, error = self.controller.autenticar_con_rostro()
        except FacialRecognitionError as exc:
            self.lbl_error.config(text=str(exc))
            return
        except Exception as exc:
            self.lbl_error.config(text=f"No se pudo iniciar sesión con rostro: {exc}")
            return

        if error:
            self.lbl_error.config(text=error)
            return

        self.on_login_success(self._crear_sesion(datos_user))
