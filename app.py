import tkinter as tk
from views.login_view import LoginView
from views.main_window import MainWindow

class SistemaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión y Ventas (Tkinter - MVC)")
        self.root.geometry("1100x700")
        self.root.minsize(950, 600)

        self.current_user = None
        self.current_screen = None

        self.mostrar_login()

    def mostrar_login(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_user = None
        self.current_screen = LoginView(self.root, on_login_success=self.on_login_success)

    def on_login_success(self, user_data):
        self.current_user = user_data
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = MainWindow(
            self.root, 
            user_session=self.current_user, 
            on_logout=self.mostrar_login
        )

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = SistemaApp()
    app.run()
