import tkinter as tk
from tkinter import ttk, messagebox
from controllers.sales_controller import SalesController
from controllers.customers_controller import CustomersController
from controllers.products_controller import ProductsController

class SalesView(tk.Frame):
    def __init__(self, parent, user_session):
        super().__init__(parent, bg="#f4f6f9")
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.user_session = user_session

        self.sales_controller = SalesController()
        self.customers_controller = CustomersController()
        self.products_controller = ProductsController()

        self.carrito = []

        self._build_ui()
        self.cargar_combos_y_ventas()

    def _build_ui(self):
        lbl_titulo = tk.Label(
            self, 
            text="PUNTO DE VENTA / REGISTRO DE VENTAS", 
            font=("Helvetica", 14, "bold"), 
            bg="#f4f6f9", 
            fg="#2c3e50"
        )
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        pos_frame = tk.Frame(self, bg="#f4f6f9")
        pos_frame.pack(fill="x", pady=(0, 15))

        form_frame = tk.Frame(pos_frame, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        form_frame.pack(side="left", fill="y", padx=(0, 10))

        lbl_sec1 = tk.Label(form_frame, text="1. Seleccionar Cliente", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#34495e")
        lbl_sec1.pack(anchor="w", pady=(0, 5))

        self.cmb_cliente = ttk.Combobox(form_frame, state="readonly", font=("Helvetica", 10), width=32)
        self.cmb_cliente.pack(fill="x", pady=(0, 15))

        lbl_sec2 = tk.Label(form_frame, text="2. Seleccionar Producto", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#34495e")
        lbl_sec2.pack(anchor="w", pady=(0, 5))

        self.cmb_producto = ttk.Combobox(form_frame, state="readonly", font=("Helvetica", 10), width=32)
        self.cmb_producto.pack(fill="x", pady=(0, 10))

        lbl_cant = tk.Label(form_frame, text="Cantidad:", font=("Helvetica", 9, "bold"), bg="#ffffff")
        lbl_cant.pack(anchor="w", pady=(0, 2))

        self.spn_cantidad = ttk.Spinbox(form_frame, from_=1, to=100, font=("Helvetica", 10), width=10)
        self.spn_cantidad.set(1)
        self.spn_cantidad.pack(anchor="w", pady=(0, 15))

        btn_agregar = tk.Button(
            form_frame, 
            text="+ Agregar al Carrito", 
            font=("Helvetica", 10, "bold"), 
            bg="#3498db", 
            fg="#ffffff", 
            command=self.agregar_al_carrito
        )
        btn_agregar.pack(fill="x")

        cart_frame = tk.Frame(pos_frame, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        cart_frame.pack(side="left", fill="both", expand=True)

        lbl_sec_cart = tk.Label(cart_frame, text="🛒 Carrito de Compras", font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#2c3e50")
        lbl_sec_cart.pack(anchor="w", pady=(0, 10))

        self.tree_cart = ttk.Treeview(cart_frame, columns=("nombre", "cantidad", "precio", "subtotal"), show="headings", height=5)
        self.tree_cart.heading("nombre", text="Producto")
        self.tree_cart.heading("cantidad", text="Cant.")
        self.tree_cart.heading("precio", text="P. Unit ($)")
        self.tree_cart.heading("subtotal", text="Subtotal ($)")

        self.tree_cart.column("nombre", width=160)
        self.tree_cart.column("cantidad", width=50, anchor="center")
        self.tree_cart.column("precio", width=80, anchor="e")
        self.tree_cart.column("subtotal", width=90, anchor="e")
        self.tree_cart.pack(fill="both", expand=True, pady=(0, 10))

        bottom_cart = tk.Frame(cart_frame, bg="#ffffff")
        bottom_cart.pack(fill="x")

        btn_quitar = tk.Button(
            bottom_cart, 
            text="Quitar Item", 
            font=("Helvetica", 9), 
            bg="#e74c3c", 
            fg="#ffffff", 
            command=self.quitar_del_carrito
        )
        btn_quitar.pack(side="left")

        totales_frame = tk.Frame(bottom_cart, bg="#ffffff")
        totales_frame.pack(side="right")

        self.lbl_subtotal = tk.Label(totales_frame, text="Subtotal: $0.00", font=("Helvetica", 9), bg="#ffffff")
        self.lbl_subtotal.pack(anchor="e")

        self.lbl_iva = tk.Label(totales_frame, text="IVA (15%): $0.00", font=("Helvetica", 9), bg="#ffffff")
        self.lbl_iva.pack(anchor="e")

        self.lbl_total = tk.Label(totales_frame, text="TOTAL: $0.00", font=("Helvetica", 12, "bold"), fg="#27ae60", bg="#ffffff")
        self.lbl_total.pack(anchor="e", pady=(2, 5))

        btn_registrar = tk.Button(
            totales_frame, 
            text="✓ REGISTRAR VENTA", 
            font=("Helvetica", 10, "bold"), 
            bg="#2ecc71", 
            fg="#ffffff", 
            padx=10, 
            pady=5, 
            command=self.registrar_venta
        )
        btn_registrar.pack(anchor="e")

        hist_frame = tk.Frame(self, bg="#f4f6f9")
        hist_frame.pack(fill="both", expand=True)

        lbl_hist = tk.Label(hist_frame, text=" Historial de Ventas Realizadas", font=("Helvetica", 11, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_hist.pack(anchor="w", pady=(0, 4))

        self.tree_ventas = ttk.Treeview(hist_frame, columns=("id", "factura", "fecha", "cliente", "total"), show="headings", height=6)
        self.tree_ventas.heading("id", text="ID")
        self.tree_ventas.heading("factura", text="N° Factura")
        self.tree_ventas.heading("fecha", text="Fecha")
        self.tree_ventas.heading("cliente", text="Cliente")
        self.tree_ventas.heading("total", text="Total ($)")

        self.tree_ventas.column("id", width=40, anchor="center")
        self.tree_ventas.column("factura", width=110, anchor="center")
        self.tree_ventas.column("fecha", width=140, anchor="center")
        self.tree_ventas.column("cliente", width=220)
        self.tree_ventas.column("total", width=100, anchor="e")
        self.tree_ventas.pack(fill="both", expand=True, pady=(0, 5))

        btn_ver_factura = tk.Button(
            hist_frame, 
            text="Ver Factura / Detalle", 
            font=("Helvetica", 9, "bold"), 
            bg="#f39c12", 
            fg="#ffffff", 
            command=self.ver_factura_modal
        )
        btn_ver_factura.pack(anchor="w")

    def cargar_combos_y_ventas(self):
        clientes = self.customers_controller.listar()
        self.clientes_map = {f"{c[1]} (Cédula: {c[2]})": c[0] for c in clientes}
        self.cmb_cliente['values'] = list(self.clientes_map.keys())
        if self.clientes_map:
            self.cmb_cliente.current(0)

        productos = self.products_controller.listar()
        self.productos_map = {}
        prod_names = []
        for p in productos:
            text = f"{p[1]} - ${float(p[4]):.2f} (Stock: {p[5]})"
            self.productos_map[text] = p
            prod_names.append(text)

        self.cmb_producto['values'] = prod_names
        if prod_names:
            self.cmb_producto.current(0)

        self.cargar_historial_ventas()

    def cargar_historial_ventas(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        ventas = self.sales_controller.obtener_ventas()
        for v in ventas:
            fecha_str = str(v[2]) if v[2] else ""
            self.tree_ventas.insert("", "end", values=(v[0], v[1], fecha_str, v[3], f"${float(v[4]):.2f}"))

    def agregar_al_carrito(self):
        prod_str = self.cmb_producto.get()
        if not prod_str or prod_str not in self.productos_map:
            messagebox.showwarning("Atención", "Seleccione un producto válido.")
            return

        try:
            cant = int(self.spn_cantidad.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atención", "Ingrese una cantidad válida mayor a cero.")
            return

        producto = self.productos_map[prod_str]
        id_prod = producto[0]
        nombre_prod = producto[1]
        precio_prod = float(producto[4])
        stock_actual = int(producto[5])

        encontrado = False
        for item in self.carrito:
            if item['id_producto'] == id_prod:
                nueva_cant = item['cantidad'] + cant
                if nueva_cant > stock_actual:
                    messagebox.showwarning("Stock Insuficiente", f"Stock disponible: {stock_actual}")
                    return
                item['cantidad'] = nueva_cant
                item['subtotal'] = nueva_cant * item['precio']
                encontrado = True
                break

        if not encontrado:
            if cant > stock_actual:
                messagebox.showwarning("Stock Insuficiente", f"Stock disponible: {stock_actual}")
                return
            self.carrito.append({
                'id_producto': id_prod,
                'nombre': nombre_prod,
                'cantidad': cant,
                'precio': precio_prod,
                'subtotal': cant * precio_prod
            })

        self.actualizar_vista_carrito()

    def quitar_del_carrito(self):
        selected = self.tree_cart.selection()
        if not selected:
            return
        idx = self.tree_cart.index(selected[0])
        if 0 <= idx < len(self.carrito):
            self.carrito.pop(idx)
            self.actualizar_vista_carrito()

    def actualizar_vista_carrito(self):
        for item in self.tree_cart.get_children():
            self.tree_cart.delete(item)

        subtotal = 0.0
        for item in self.carrito:
            self.tree_cart.insert("", "end", values=(
                item['nombre'], 
                item['cantidad'], 
                f"${item['precio']:.2f}", 
                f"${item['subtotal']:.2f}"
            ))
            subtotal += item['subtotal']

        iva = round(subtotal * 0.15, 2)
        total = subtotal + iva

        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal:,.2f}")
        self.lbl_iva.config(text=f"IVA (15%): ${iva:,.2f}")
        self.lbl_total.config(text=f"TOTAL: ${total:,.2f}")

    def registrar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Carrito Vacío", "No hay productos en el carrito para procesar la venta.")
            return

        client_str = self.cmb_cliente.get()
        if not client_str or client_str not in self.clientes_map:
            messagebox.showwarning("Cliente Requerido", "Por favor seleccione un cliente para la venta.")
            return

        id_cliente = self.clientes_map[client_str]
        id_usuario = self.user_session['id_usuario']

        id_venta, numero_factura = self.sales_controller.procesar_venta(id_cliente, id_usuario, self.carrito)

        messagebox.showinfo("Venta Exitosa", f"Venta registrada correctamente.\nFactura N°: {numero_factura}")

        self.carrito = []
        self.actualizar_vista_carrito()
        self.cargar_combos_y_ventas()

        ModalFactura(self, id_venta, self.sales_controller)

    def ver_factura_modal(self):
        selected = self.tree_ventas.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una venta del historial para ver su factura.")
            return

        values = self.tree_ventas.item(selected[0], "values")
        id_venta = values[0]
        ModalFactura(self, id_venta, self.sales_controller)


class ModalFactura(tk.Toplevel):
    def __init__(self, parent, id_venta, sales_controller):
        super().__init__(parent)
        self.title("Factura de Venta")
        self.geometry("480x520")
        self.resizable(False, False)
        self.grab_set()

        self.id_venta = id_venta
        self.sales_controller = sales_controller

        self._build_ui()

    def _build_ui(self):
        venta = self.sales_controller.obtener_venta_por_id(self.id_venta)
        if not venta:
            messagebox.showerror("Error", "No se encontró la información de la venta.", parent=self)
            self.destroy()
            return

        detalles = self.sales_controller.obtener_detalles_venta(self.id_venta)

        frame = tk.Frame(self, padx=20, pady=20, bg="#ffffff")
        frame.pack(fill="both", expand=True)

        lbl_empresa = tk.Label(frame, text="SISTEMA DE GESTIÓN & VENTAS", font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#2c3e50")
        lbl_empresa.pack()

        lbl_fac_num = tk.Label(frame, text=f"FACTURA: {venta[1]}", font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#e74c3c")
        lbl_fac_num.pack(pady=(2, 10))

        info_client_frame = tk.Frame(frame, bg="#ffffff", bd=1, relief="groove", padx=10, pady=8)
        info_client_frame.pack(fill="x", pady=(0, 15))

        lbl_c1 = tk.Label(info_client_frame, text=f"Cliente: {venta[6]}", font=("Helvetica", 9, "bold"), bg="#ffffff", anchor="w")
        lbl_c1.pack(fill="x")
        lbl_c2 = tk.Label(info_client_frame, text=f"Cédula: {venta[7]}   |   Teléfono: {venta[8]}", font=("Helvetica", 9), bg="#ffffff", anchor="w")
        lbl_c2.pack(fill="x")
        lbl_c3 = tk.Label(info_client_frame, text=f"Fecha: {venta[2]}", font=("Helvetica", 9), bg="#ffffff", anchor="w")
        lbl_c3.pack(fill="x")

        tree = ttk.Treeview(frame, columns=("producto", "cant", "precio", "subtotal"), show="headings", height=6)
        tree.heading("producto", text="Producto")
        tree.heading("cant", text="Cant.")
        tree.heading("precio", text="P.Unit")
        tree.heading("subtotal", text="Subtotal")

        tree.column("producto", width=180)
        tree.column("cant", width=50, anchor="center")
        tree.column("precio", width=70, anchor="e")
        tree.column("subtotal", width=80, anchor="e")
        tree.pack(fill="both", expand=True, pady=(0, 10))

        for d in detalles:
            tree.insert("", "end", values=(d[0], d[1], f"${float(d[2]):.2f}", f"${float(d[3]):.2f}"))

        tot_frame = tk.Frame(frame, bg="#ffffff")
        tot_frame.pack(fill="x")

        lbl_s = tk.Label(tot_frame, text=f"Subtotal:  ${float(venta[3]):.2f}", font=("Helvetica", 9), bg="#ffffff", anchor="e")
        lbl_s.pack(fill="x")
        lbl_i = tk.Label(tot_frame, text=f"IVA 15%:    ${float(venta[4]):.2f}", font=("Helvetica", 9), bg="#ffffff", anchor="e")
        lbl_i.pack(fill="x")
        lbl_t = tk.Label(tot_frame, text=f"TOTAL:      ${float(venta[5]):.2f}", font=("Helvetica", 11, "bold"), fg="#27ae60", bg="#ffffff", anchor="e")
        lbl_t.pack(fill="x", pady=(2, 10))

        btn_cerrar = tk.Button(frame, text="Cerrar", font=("Helvetica", 10), bg="#7f8c8d", fg="#ffffff", command=self.destroy)
        btn_cerrar.pack(anchor="center")
