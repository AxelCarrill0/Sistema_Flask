import tkinter as tk
from tkinter import ttk
from controllers.dashboard_controller import DashboardController

class DashboardView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = DashboardController()
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self._build_ui()
        self.cargar_datos()

    def _build_ui(self):
        lbl_titulo = tk.Label(
            self, 
            text="PANEL GENERAL / DASHBOARD", 
            font=("Helvetica", 14, "bold"), 
            bg="#f4f6f9", 
            fg="#2c3e50"
        )
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        # Tarjetas de métricas
        cards_frame = tk.Frame(self, bg="#f4f6f9")
        cards_frame.pack(fill="x", pady=(0, 20))

        self.card_ventas = self._crear_tarjeta(cards_frame, "Ventas del Mes", "$ 0.00", "#2ecc71")
        self.card_ventas.grid(row=0, column=0, padx=5, sticky="ew")

        self.card_facturas = self._crear_tarjeta(cards_frame, "Facturas del Mes", "0", "#3498db")
        self.card_facturas.grid(row=0, column=1, padx=5, sticky="ew")

        self.card_productos = self._crear_tarjeta(cards_frame, "Total Productos", "0", "#e67e22")
        self.card_productos.grid(row=0, column=2, padx=5, sticky="ew")

        self.card_clientes = self._crear_tarjeta(cards_frame, "Total Clientes", "0", "#9b59b6")
        self.card_clientes.grid(row=0, column=3, padx=5, sticky="ew")

        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)

        # Tablas y resúmenes
        tables_frame = tk.Frame(self, bg="#f4f6f9")
        tables_frame.pack(fill="both", expand=True)
        tables_frame.columnconfigure(0, weight=1)
        tables_frame.columnconfigure(1, weight=1)

        left_column = tk.Frame(tables_frame, bg="#f4f6f9")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        lbl_top = tk.Label(left_column, text="🔥 Productos Más Vendidos", font=("Helvetica", 11, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_top.pack(anchor="w", pady=(0, 5))

        self.tree_top = ttk.Treeview(left_column, columns=("nombre", "cantidad"), show="headings", height=4)
        self.tree_top.heading("nombre", text="Producto")
        self.tree_top.heading("cantidad", text="Cantidad Vendida")
        self.tree_top.column("nombre", width=180)
        self.tree_top.column("cantidad", width=110, anchor="center")
        self.tree_top.pack(fill="x", pady=(0, 15))

        lbl_stock = tk.Label(left_column, text="⚠️ Alertas de Bajo Stock (<= 5)", font=("Helvetica", 11, "bold"), bg="#f4f6f9", fg="#c0392b")
        lbl_stock.pack(anchor="w", pady=(0, 5))

        self.tree_stock = ttk.Treeview(left_column, columns=("nombre", "stock"), show="headings", height=4)
        self.tree_stock.heading("nombre", text="Producto")
        self.tree_stock.heading("stock", text="Stock Actual")
        self.tree_stock.column("nombre", width=180)
        self.tree_stock.column("stock", width=110, anchor="center")
        self.tree_stock.pack(fill="x")

        right_column = tk.Frame(tables_frame, bg="#f4f6f9")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        lbl_ultimas = tk.Label(right_column, text="🕒 Últimas Ventas Registradas", font=("Helvetica", 11, "bold"), bg="#f4f6f9", fg="#2c3e50")
        lbl_ultimas.pack(anchor="w", pady=(0, 5))

        self.tree_ventas = ttk.Treeview(right_column, columns=("factura", "fecha", "cliente", "total"), show="headings", height=10)
        self.tree_ventas.heading("factura", text="N° Factura")
        self.tree_ventas.heading("fecha", text="Fecha")
        self.tree_ventas.heading("cliente", text="Cliente")
        self.tree_ventas.heading("total", text="Total ($)")
        
        self.tree_ventas.column("factura", width=90, anchor="center")
        self.tree_ventas.column("fecha", width=110, anchor="center")
        self.tree_ventas.column("cliente", width=130)
        self.tree_ventas.column("total", width=80, anchor="e")
        self.tree_ventas.pack(fill="both", expand=True)

    def _crear_tarjeta(self, parent, titulo, valor_inicial, color_borde):
        frame = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        lbl_tit = tk.Label(frame, text=titulo, font=("Helvetica", 9, "bold"), fg="#7f8c8d", bg="#ffffff")
        lbl_tit.pack(anchor="w")
        lbl_val = tk.Label(frame, text=valor_inicial, font=("Helvetica", 16, "bold"), fg=color_borde, bg="#ffffff")
        lbl_val.pack(anchor="w", pady=(5, 0))
        frame.lbl_val = lbl_val
        return frame

    def cargar_datos(self):
        m = self.controller.obtener_metricas()

        self.card_ventas.lbl_val.config(text=f"$ {m['total_ventas']:,.2f}")
        self.card_facturas.lbl_val.config(text=str(m['total_facturas']))
        self.card_productos.lbl_val.config(text=str(m['total_productos']))
        self.card_clientes.lbl_val.config(text=str(m['total_clientes']))

        for item in self.tree_top.get_children():
            self.tree_top.delete(item)
        for p in m['top_productos']:
            self.tree_top.insert("", "end", values=(p[0], p[1]))

        for item in self.tree_stock.get_children():
            self.tree_stock.delete(item)
        for p in m['alertas_stock']:
            self.tree_stock.insert("", "end", values=(p[0], p[1]))

        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        for v in m['ultimas_ventas']:
            fecha_str = str(v[2]) if v[2] else ""
            self.tree_ventas.insert("", "end", values=(v[1], fecha_str, v[4], f"${float(v[3]):.2f}"))
