import tkinter as tk
from tkinter import ttk, messagebox
from controllers.categories_controller import CategoriesController

class CategoriesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = CategoriesController()
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self._build_ui()
        self.cargar_categorias()

    def _build_ui(self):
        header_frame = tk.Frame(self, bg="#f4f6f9")
        header_frame.pack(fill="x", pady=(0, 15))

        lbl_titulo = tk.Label(
            header_frame, 
            text="GESTIÓN DE CATEGORÍAS", 
            font=("Helvetica", 14, "bold"), 
            bg="#f4f6f9", 
            fg="#2c3e50"
        )
        lbl_titulo.pack(side="left")

        btn_nuevo = tk.Button(
            header_frame, 
            text="+ Nueva Categoría", 
            font=("Helvetica", 10, "bold"), 
            bg="#2ecc71", 
            fg="#ffffff", 
            cursor="hand2",
            padx=10, 
            pady=5, 
            command=self.abrir_modal_crear
        )
        btn_nuevo.pack(side="right")

        tree_frame = tk.Frame(self, bg="#ffffff")
        tree_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            tree_frame, 
            columns=("id", "nombre", "descripcion"), 
            show="headings", 
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre Categoría")
        self.tree.heading("descripcion", text="Descripción")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=200)
        self.tree.column("descripcion", width=400)

        self.tree.pack(fill="both", expand=True)

        actions_frame = tk.Frame(self, bg="#f4f6f9")
        actions_frame.pack(fill="x", pady=(10, 0))

        btn_editar = tk.Button(
            actions_frame, 
            text="Editar Seleccionada", 
            font=("Helvetica", 9, "bold"), 
            bg="#f39c12", 
            fg="#ffffff", 
            command=self.abrir_modal_editar
        )
        btn_editar.pack(side="left", padx=(0, 10))

        btn_eliminar = tk.Button(
            actions_frame, 
            text="Eliminar Seleccionada", 
            font=("Helvetica", 9, "bold"), 
            bg="#e74c3c", 
            fg="#ffffff", 
            command=self.eliminar_categoria
        )
        btn_eliminar.pack(side="left")

    def cargar_categorias(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        categorias = self.controller.listar()
        for cat in categorias:
            self.tree.insert("", "end", values=(cat[0], cat[1], cat[2]))

    def abrir_modal_crear(self):
        ModalCategoria(self, titulo="Nueva Categoría", on_guardar=self._guardar_nueva)

    def _guardar_nueva(self, datos):
        self.controller.crear(datos['nombre'], datos['descripcion'])
        messagebox.showinfo("Éxito", "Categoría creada satisfactoriamente.")
        self.cargar_categorias()

    def abrir_modal_editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor seleccione una categoría de la lista.")
            return

        values = self.tree.item(selected[0], "values")
        cat_datos = {
            'id': values[0],
            'nombre': values[1],
            'descripcion': values[2]
        }

        ModalCategoria(self, titulo="Editar Categoría", categoria=cat_datos, on_guardar=self._guardar_edicion)

    def _guardar_edicion(self, datos):
        self.controller.actualizar(datos['id'], datos['nombre'], datos['descripcion'])
        messagebox.showinfo("Éxito", "Categoría actualizada satisfactoriamente.")
        self.cargar_categorias()

    def eliminar_categoria(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor seleccione una categoría de la lista.")
            return

        values = self.tree.item(selected[0], "values")
        id_categoria = values[0]
        nombre = values[1]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la categoría '{nombre}'?"):
            self.controller.eliminar(id_categoria)
            messagebox.showinfo("Éxito", "Categoría eliminada satisfactoriamente.")
            self.cargar_categorias()


class ModalCategoria(tk.Toplevel):
    def __init__(self, parent, titulo, categoria=None, on_guardar=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("380x250")
        self.resizable(False, False)
        self.grab_set()

        self.categoria = categoria
        self.on_guardar = on_guardar

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        lbl_nombre = tk.Label(frame, text="Nombre Categoría:", font=("Helvetica", 9, "bold"), anchor="w")
        lbl_nombre.pack(fill="x", pady=(0, 2))
        self.ent_nombre = ttk.Entry(frame, font=("Helvetica", 10))
        self.ent_nombre.pack(fill="x", pady=(0, 10))

        lbl_desc = tk.Label(frame, text="Descripción:", font=("Helvetica", 9, "bold"), anchor="w")
        lbl_desc.pack(fill="x", pady=(0, 2))
        self.ent_desc = ttk.Entry(frame, font=("Helvetica", 10))
        self.ent_desc.pack(fill="x", pady=(0, 15))

        if self.categoria:
            self.ent_nombre.insert(0, self.categoria['nombre'])
            self.ent_desc.insert(0, self.categoria['descripcion'])

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x")

        btn_guardar = tk.Button(
            btn_frame, 
            text="Guardar", 
            font=("Helvetica", 10, "bold"), 
            bg="#2ecc71", 
            fg="#ffffff", 
            command=self._guardar
        )
        btn_guardar.pack(side="right", padx=(10, 0))

        btn_cancelar = tk.Button(
            btn_frame, 
            text="Cancelar", 
            font=("Helvetica", 10), 
            bg="#95a5a6", 
            fg="#ffffff", 
            command=self.destroy
        )
        btn_cancelar.pack(side="right")

    def _guardar(self):
        nombre = self.ent_nombre.get().strip()
        descripcion = self.ent_desc.get().strip()

        if not nombre:
            messagebox.showwarning("Campo Requerido", "El nombre de la categoría es obligatorio.", parent=self)
            return

        datos = {'nombre': nombre, 'descripcion': descripcion}
        if self.categoria:
            datos['id'] = self.categoria['id']

        if self.on_guardar:
            self.on_guardar(datos)

        self.destroy()
