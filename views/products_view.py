import tkinter as tk
from tkinter import ttk, messagebox
from controllers.products_controller import ProductsController
from controllers.categories_controller import CategoriesController

class ProductsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = ProductsController()
        self.categories_controller = CategoriesController()
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self._build_ui()
        self.cargar_productos()

    def _build_ui(self):
        header_frame = tk.Frame(self, bg="#f4f6f9")
        header_frame.pack(fill="x", pady=(0, 15))

        lbl_titulo = tk.Label(
            header_frame, 
            text="GESTIÓN DE PRODUCTOS", 
            font=("Helvetica", 14, "bold"), 
            bg="#f4f6f9", 
            fg="#2c3e50"
        )
        lbl_titulo.pack(side="left")

        btn_nuevo = tk.Button(
            header_frame, 
            text="+ Nuevo Producto", 
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
            columns=("id", "nombre", "descripcion", "material", "precio", "stock", "categoria"), 
            show="headings", 
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre Producto")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("material", text="Material")
        self.tree.heading("precio", text="Precio ($)")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("categoria", text="Categoría")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nombre", width=160)
        self.tree.column("descripcion", width=180)
        self.tree.column("material", width=100)
        self.tree.column("precio", width=80, anchor="e")
        self.tree.column("stock", width=60, anchor="center")
        self.tree.column("categoria", width=120)

        self.tree.pack(fill="both", expand=True)

        actions_frame = tk.Frame(self, bg="#f4f6f9")
        actions_frame.pack(fill="x", pady=(10, 0))

        btn_editar = tk.Button(
            actions_frame, 
            text="Editar Seleccionado", 
            font=("Helvetica", 9, "bold"), 
            bg="#f39c12", 
            fg="#ffffff", 
            command=self.abrir_modal_editar
        )
        btn_editar.pack(side="left", padx=(0, 10))

        btn_eliminar = tk.Button(
            actions_frame, 
            text="Eliminar Seleccionado", 
            font=("Helvetica", 9, "bold"), 
            bg="#e74c3c", 
            fg="#ffffff", 
            command=self.eliminar_producto
        )
        btn_eliminar.pack(side="left")

    def cargar_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos = self.controller.listar()
        categorias = {cat[0]: cat[1] for cat in self.categories_controller.listar()}

        for p in productos:
            id_cat = p[6]
            nombre_cat = categorias.get(id_cat, f"ID: {id_cat}")
            precio_str = f"${float(p[4]):.2f}"
            self.tree.insert("", "end", values=(p[0], p[1], p[2], p[3], precio_str, p[5], nombre_cat))

    def abrir_modal_crear(self):
        ModalProducto(self, titulo="Nuevo Producto", on_guardar=self._guardar_nuevo)

    def _guardar_nuevo(self, datos):
        self.controller.crear(
            datos['nombre'], 
            datos['descripcion'], 
            datos['material'], 
            datos['precio'], 
            datos['stock'], 
            datos['id_categoria']
        )
        messagebox.showinfo("Éxito", "Producto agregado satisfactoriamente.")
        self.cargar_productos()

    def abrir_modal_editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor seleccione un producto de la lista.")
            return

        values = self.tree.item(selected[0], "values")
        id_producto = values[0]
        datos_raw = self.controller.obtener_por_id(id_producto)
        if not datos_raw:
            return

        prod_datos = {
            'id': datos_raw[0],
            'nombre': datos_raw[1],
            'descripcion': datos_raw[2],
            'material': datos_raw[3],
            'precio': datos_raw[4],
            'stock': datos_raw[5],
            'id_categoria': datos_raw[6]
        }

        ModalProducto(self, titulo="Editar Producto", producto=prod_datos, on_guardar=self._guardar_edicion)

    def _guardar_edicion(self, datos):
        self.controller.actualizar(
            datos['id'],
            datos['nombre'], 
            datos['descripcion'], 
            datos['material'], 
            datos['precio'], 
            datos['stock'], 
            datos['id_categoria']
        )
        messagebox.showinfo("Éxito", "Producto actualizado satisfactoriamente.")
        self.cargar_productos()

    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor seleccione un producto de la lista.")
            return

        values = self.tree.item(selected[0], "values")
        id_producto = values[0]
        nombre = values[1]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto '{nombre}'?"):
            self.controller.eliminar(id_producto)
            messagebox.showinfo("Éxito", "Producto eliminado satisfactoriamente.")
            self.cargar_productos()


class ModalProducto(tk.Toplevel):
    def __init__(self, parent, titulo, producto=None, on_guardar=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("420x450")
        self.resizable(False, False)
        self.grab_set()

        self.producto = producto
        self.on_guardar = on_guardar
        self.categories_controller = CategoriesController()
        self.categorias_lista = self.categories_controller.listar()

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        lbl_nombre = tk.Label(frame, text="Nombre del Producto:", font=("Helvetica", 9, "bold"), anchor="w")
        lbl_nombre.pack(fill="x", pady=(2, 2))
        self.ent_nombre = ttk.Entry(frame, font=("Helvetica", 10))
        self.ent_nombre.pack(fill="x", pady=(0, 5))

        lbl_desc = tk.Label(frame, text="Descripción:", font=("Helvetica", 9, "bold"), anchor="w")
        lbl_desc.pack(fill="x", pady=(2, 2))
        self.ent_desc = ttk.Entry(frame, font=("Helvetica", 10))
        self.ent_desc.pack(fill="x", pady=(0, 5))

        lbl_mat = tk.Label(frame, text="Material:", font=("Helvetica", 9, "bold"), anchor="w")
        lbl_mat.pack(fill="x", pady=(2, 2))
        self.ent_mat = ttk.Entry(frame, font=("Helvetica", 10))
        self.ent_mat.pack(fill="x", pady=(0, 5))

        row_ps = tk.Frame(frame)
        row_ps.pack(fill="x", pady=(2, 5))

        f_precio = tk.Frame(row_ps)
        f_precio.pack(side="left", fill="x", expand=True, padx=(0, 5))
        lbl_prec = tk.Label(f_precio, text="Precio ($):", font=("Helvetica", 9, "bold"), anchor="w")
        lbl_prec.pack(fill="x")
        self.ent_prec = ttk.Entry(f_precio, font=("Helvetica", 10))
        self.ent_prec.pack(fill="x")

        f_stock = tk.Frame(row_ps)
        f_stock.pack(side="left", fill="x", expand=True, padx=(5, 0))
        lbl_stk = tk.Label(f_stock, text="Stock:", font=("Helvetica", 9, "bold"), anchor="w")
        lbl_stk.pack(fill="x")
        self.ent_stk = ttk.Entry(f_stock, font=("Helvetica", 10))
        self.ent_stk.pack(fill="x")

        lbl_cat = tk.Label(frame, text="Categoría:", font=("Helvetica", 9, "bold"), anchor="w")
        lbl_cat.pack(fill="x", pady=(5, 2))
        
        self.cat_map = {f"{c[1]} (ID: {c[0]})": c[0] for c in self.categorias_lista}
        cat_names = list(self.cat_map.keys())

        self.cmb_cat = ttk.Combobox(frame, values=cat_names, state="readonly", font=("Helvetica", 10))
        self.cmb_cat.pack(fill="x", pady=(0, 15))
        if cat_names:
            self.cmb_cat.current(0)

        if self.producto:
            self.ent_nombre.insert(0, self.producto['nombre'])
            self.ent_desc.insert(0, self.producto['descripcion'])
            self.ent_mat.insert(0, self.producto['material'])
            self.ent_prec.insert(0, str(self.producto['precio']))
            self.ent_stk.insert(0, str(self.producto['stock']))
            
            for text, cat_id in self.cat_map.items():
                if cat_id == self.producto['id_categoria']:
                    self.cmb_cat.set(text)
                    break

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
        material = self.ent_mat.get().strip()
        prec_str = self.ent_prec.get().strip()
        stk_str = self.ent_stk.get().strip()
        cat_str = self.cmb_cat.get()

        if not nombre or not prec_str or not stk_str or not cat_str:
            messagebox.showwarning("Campos Requeridos", "Por favor complete todos los campos obligatorios.", parent=self)
            return

        try:
            precio = float(prec_str)
            stock = int(stk_str)
        except ValueError:
            messagebox.showwarning("Error de Formato", "El precio debe ser un número decimal y el stock un número entero.", parent=self)
            return

        id_cat = self.cat_map[cat_str]

        datos = {
            'nombre': nombre,
            'descripcion': descripcion,
            'material': material,
            'precio': precio,
            'stock': stock,
            'id_categoria': id_cat
        }
        if self.producto:
            datos['id'] = self.producto['id']

        if self.on_guardar:
            self.on_guardar(datos)

        self.destroy()
