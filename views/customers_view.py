import tkinter as tk
from tkinter import ttk, messagebox
from controllers.customers_controller import CustomersController

class CustomersView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = CustomersController()
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self._build_ui()
        self.cargar_clientes()

    def _build_ui(self):
        header_frame = tk.Frame(self, bg="#f4f6f9")
        header_frame.pack(fill="x", pady=(0, 15))

        lbl_titulo = tk.Label(
            header_frame, 
            text="GESTIÓN DE CLIENTES", 
            font=("Helvetica", 14, "bold"), 
            bg="#f4f6f9", 
            fg="#2c3e50"
        )
        lbl_titulo.pack(side="left")

        btn_nuevo = tk.Button(
            header_frame, 
            text="+ Nuevo Cliente", 
            font=("Helvetica", 10, "bold"), 
            bg="#2ecc71", 
            fg="#ffffff", 
            cursor="hand2",
            padx=10, 
            pady=5, 
            command=self.abrir_modal_crear
        )
        btn_nuevo.pack(side="right")

        # Barra de Búsqueda
        search_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid", padx=10, pady=10)
        search_frame.pack(fill="x", pady=(0, 15))

        lbl_buscar = tk.Label(search_frame, text="Buscar por Nombre o Cédula:", font=("Helvetica", 10), bg="#ffffff")
        lbl_buscar.pack(side="left", padx=(0, 10))

        self.ent_buscar = ttk.Entry(search_frame, font=("Helvetica", 10), width=30)
        self.ent_buscar.pack(side="left", padx=(0, 10))
        self.ent_buscar.bind("<Return>", lambda event: self.buscar_clientes())

        btn_buscar = tk.Button(
            search_frame, 
            text="Buscar", 
            font=("Helvetica", 9, "bold"), 
            bg="#3498db", 
            fg="#ffffff", 
            command=self.buscar_clientes
        )
        btn_buscar.pack(side="left", padx=(0, 5))

        btn_limpiar = tk.Button(
            search_frame, 
            text="Mostrar Todos", 
            font=("Helvetica", 9), 
            bg="#95a5a6", 
            fg="#ffffff", 
            command=self.limpiar_busqueda
        )
        btn_limpiar.pack(side="left")

        # Tabla de Clientes
        tree_frame = tk.Frame(self, bg="#ffffff")
        tree_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            tree_frame, 
            columns=("id", "nombre", "cedula", "telefono", "correo", "direccion"), 
            show="headings", 
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre Completo")
        self.tree.heading("cedula", text="Cédula / RUC")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("correo", text="Correo Electrónico")
        self.tree.heading("direccion", text="Dirección")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nombre", width=180)
        self.tree.column("cedula", width=110, anchor="center")
        self.tree.column("telefono", width=110, anchor="center")
        self.tree.column("correo", width=160)
        self.tree.column("direccion", width=200)

        self.tree.pack(fill="both", expand=True)

        # Acciones inferiores
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
            command=self.eliminar_cliente
        )
        btn_eliminar.pack(side="left")

    def cargar_clientes(self, clientes=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if clientes is None:
            clientes = self.controller.listar()

        for c in clientes:
            self.tree.insert("", "end", values=(c[0], c[1], c[2], c[3], c[4], c[5]))

    def buscar_clientes(self):
        texto = self.ent_buscar.get().strip()
        if texto:
            resultados = self.controller.buscar(texto)
            self.cargar_clientes(resultados)
        else:
            self.cargar_clientes()

    def limpiar_busqueda(self):
        self.ent_buscar.delete(0, tk.END)
        self.cargar_clientes()

    def abrir_modal_crear(self):
        ModalCliente(self, titulo="Nuevo Cliente", on_guardar=self._guardar_nuevo)

    def _guardar_nuevo(self, datos):
        self.controller.crear(
            datos['nombre'], 
            datos['cedula'], 
            datos['telefono'], 
            datos['correo'], 
            datos['direccion']
        )
        messagebox.showinfo("Éxito", "Cliente creado satisfactoriamente.")
        self.cargar_clientes()

    def abrir_modal_editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor seleccione un cliente de la lista.")
            return

        values = self.tree.item(selected[0], "values")
        cliente_datos = {
            'id': values[0],
            'nombre': values[1],
            'cedula': values[2],
            'telefono': values[3],
            'correo': values[4],
            'direccion': values[5]
        }

        ModalCliente(self, titulo="Editar Cliente", cliente=cliente_datos, on_guardar=self._guardar_edicion)

    def _guardar_edicion(self, datos):
        self.controller.actualizar(
            datos['id'],
            datos['nombre'], 
            datos['cedula'], 
            datos['telefono'], 
            datos['correo'], 
            datos['direccion']
        )
        messagebox.showinfo("Éxito", "Cliente actualizado satisfactoriamente.")
        self.cargar_clientes()

    def eliminar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Por favor seleccione un cliente de la lista.")
            return

        values = self.tree.item(selected[0], "values")
        id_cliente = values[0]
        nombre = values[1]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al cliente '{nombre}'?"):
            self.controller.eliminar(id_cliente)
            messagebox.showinfo("Éxito", "Cliente eliminado satisfactoriamente.")
            self.cargar_clientes()


class ModalCliente(tk.Toplevel):
    def __init__(self, parent, titulo, cliente=None, on_guardar=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("400x380")
        self.resizable(False, False)
        self.grab_set()

        self.cliente = cliente
        self.on_guardar = on_guardar

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        fields = [
            ("Nombre Completo:", "ent_nombre"),
            ("Cédula / RUC:", "ent_cedula"),
            ("Teléfono:", "ent_telefono"),
            ("Correo Electrónico:", "ent_correo"),
            ("Dirección:", "ent_direccion")
        ]

        self.entries = {}
        for i, (label_text, var_name) in enumerate(fields):
            lbl = tk.Label(frame, text=label_text, font=("Helvetica", 9, "bold"), anchor="w")
            lbl.grid(row=i*2, column=0, sticky="w", pady=(5, 0))

            ent = ttk.Entry(frame, font=("Helvetica", 10), width=38)
            ent.grid(row=i*2+1, column=0, sticky="ew", pady=(0, 5))
            self.entries[var_name] = ent

        if self.cliente:
            self.entries['ent_nombre'].insert(0, self.cliente['nombre'])
            self.entries['ent_cedula'].insert(0, self.cliente['cedula'])
            self.entries['ent_telefono'].insert(0, self.cliente['telefono'])
            self.entries['ent_correo'].insert(0, self.cliente['correo'])
            self.entries['ent_direccion'].insert(0, self.cliente['direccion'])

        btn_frame = tk.Frame(frame, pady=15)
        btn_frame.grid(row=10, column=0, sticky="ew")

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
        nombre = self.entries['ent_nombre'].get().strip()
        cedula = self.entries['ent_cedula'].get().strip()
        telefono = self.entries['ent_telefono'].get().strip()
        correo = self.entries['ent_correo'].get().strip()
        direccion = self.entries['ent_direccion'].get().strip()

        if not nombre or not cedula:
            messagebox.showwarning("Campos Requeridos", "El Nombre y la Cédula son obligatorios.", parent=self)
            return

        datos = {
            'nombre': nombre,
            'cedula': cedula,
            'telefono': telefono,
            'correo': correo,
            'direccion': direccion
        }
        if self.cliente:
            datos['id'] = self.cliente['id']

        if self.on_guardar:
            self.on_guardar(datos)

        self.destroy()
