import tkinter as tk
from tkinter import messagebox

from views.categories_view import CategoriesView
from views.customers_view import CustomersView
from views.dashboard_view import DashboardView
from views.products_view import ProductsView
from views.profile_view import ProfileView
from views.sales_view import SalesView


class MainWindow(tk.Frame):
    def __init__(self, parent, user_session, on_logout):
        super().__init__(parent, bg="#f4f6f9")
        self.user_session = user_session
        self.on_logout = on_logout
        self.pack(fill="both", expand=True)

        self.current_view_frame = None
        self._build_ui()
        self.mostrar_vista("dashboard")

    def _build_ui(self):
        header = tk.Frame(self, bg="#2c3e50", height=50, padx=15)
        header.pack(fill="x", side="top")

        lbl_app_name = tk.Label(
            header,
            text="SISTEMA DE GESTIÓN & VENTAS (MVC - TKINTER)",
            font=("Helvetica", 11, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        lbl_app_name.pack(side="left", pady=12)

        btn_logout = tk.Button(
            header,
            text="Cerrar Sesión",
            font=("Helvetica", 9, "bold"),
            bg="#e74c3c",
            fg="#ffffff",
            activebackground="#c0392b",
            activeforeground="#ffffff",
            cursor="hand2",
            command=self._logout,
        )
        btn_logout.pack(side="right", pady=8)

        lbl_user_info = tk.Label(
            header,
            text=f"Usuario: {self.user_session.get('nombre_usuario', 'Usuario')}",
            font=("Helvetica", 10),
            bg="#2c3e50",
            fg="#bdc3c7",
        )
        lbl_user_info.pack(side="right", padx=(0, 15), pady=12)

        body = tk.Frame(self, bg="#f4f6f9")
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, bg="#34495e", width=200, padx=10, pady=15)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        menu_items = [
            ("Dashboard", "dashboard"),
            ("Clientes", "clientes"),
            ("Categorías", "categorias"),
            ("Productos", "productos"),
            ("Ventas", "ventas"),
            ("Perfil", "perfil"),
        ]

        self.menu_buttons = {}
        for text, key in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Helvetica", 10, "bold"),
                bg="#34495e",
                fg="#ecf0f1",
                activebackground="#1abc9c",
                activeforeground="#ffffff",
                bd=0,
                anchor="w",
                padx=15,
                pady=10,
                cursor="hand2",
                command=lambda k=key: self.mostrar_vista(k),
            )
            btn.pack(fill="x", pady=2)
            self.menu_buttons[key] = btn

        self.content_area = tk.Frame(body, bg="#f4f6f9")
        self.content_area.pack(side="right", fill="both", expand=True)

    def mostrar_vista(self, vista_key):
        if self.current_view_frame:
            self.current_view_frame.destroy()

        for key, btn in self.menu_buttons.items():
            if key == vista_key:
                btn.config(bg="#1abc9c", fg="#ffffff")
            else:
                btn.config(bg="#34495e", fg="#ecf0f1")

        if vista_key == "dashboard":
            self.current_view_frame = DashboardView(self.content_area)
        elif vista_key == "clientes":
            self.current_view_frame = CustomersView(self.content_area)
        elif vista_key == "categorias":
            self.current_view_frame = CategoriesView(self.content_area)
        elif vista_key == "productos":
            self.current_view_frame = ProductsView(self.content_area)
        elif vista_key == "ventas":
            self.current_view_frame = SalesView(self.content_area, self.user_session)
        elif vista_key == "perfil":
            self.current_view_frame = ProfileView(self.content_area, self.user_session)

    def _logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de cerrar sesión?"):
            self.on_logout()
