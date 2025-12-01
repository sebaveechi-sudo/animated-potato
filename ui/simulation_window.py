import tkinter as tk
from tkinter import simpledialog
from config import settings

class SimulationWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sim_state = controller.estado_simulacion
        self.configure(bg=settings.COLOR_FONDO)

        main_layout = tk.Frame(self, bg=settings.COLOR_FONDO)
        main_layout.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(main_layout, bg="white", width=800)
        self.canvas.pack(side="left", fill="both", expand=True)

        control_panel = tk.Frame(main_layout, bg=settings.COLOR_BARRA_SUPERIOR, width=280)
        control_panel.pack(side="right", fill="y", padx=(10, 0))

        tk.Label(control_panel, text="Sistema EFE", bg=settings.COLOR_BARRA_SUPERIOR, fg="white", font=("Arial", 16, "bold")).pack(pady=20)

        self.lbl_hora = tk.Label(control_panel, text="--:--", bg=settings.COLOR_BARRA_SUPERIOR, fg="#f1c40f", font=("Arial", 24, "bold"))
        self.lbl_hora.pack(pady=10)

        self.lbl_ocupacion = tk.Label(control_panel, text="Ocupación: 0%", bg=settings.COLOR_BARRA_SUPERIOR, fg="white")
        self.lbl_ocupacion.pack(pady=5)
        self.lbl_espera = tk.Label(control_panel, text="Esperando: 0", bg=settings.COLOR_BARRA_SUPERIOR, fg="white")
        self.lbl_espera.pack(pady=5)
        self.btn_continuar = tk.Button(control_panel, text="CONTINUAR", 
                                       command=self.avanzar_turno, 
                                       bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), height=3)
        self.btn_continuar.pack(fill="x", padx=15, pady=30)

        tk.Button(control_panel, text="Guardar Estado", command=self.sim_state.guardar_partida).pack(fill="x", padx=15, pady=5)
        tk.Button(control_panel, text="Cargar Estado", command=self.sim_state.cargar_partida).pack(fill="x", padx=15, pady=5)
        tk.Button(control_panel, text="Configuración", command=self.abrir_configuracion).pack(fill="x", padx=15, pady=5)
        tk.Button(control_panel, text="Volver al Menú", command=lambda: controller.show_frame("MenuWindow"), bg="#e74c3c", fg="white").pack(fill="x", padx=15, pady=40)

        bottom_frame = tk.LabelFrame(self, text="Registro de Eventos", bg=settings.COLOR_FONDO, height=180)
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        scrollbar = tk.Scrollbar(bottom_frame)
        scrollbar.pack(side="right", fill="y")
        self.list_eventos = tk.Listbox(bottom_frame, yscrollcommand=scrollbar.set, font=("Consolas", 10), height=8)
        self.list_eventos.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.list_eventos.yview)

        self.last_event_count = 0
        self.actualizar_info()

    def avanzar_turno(self):
        self.btn_continuar.config(state="disabled", text="Procesando...", bg="#95a5a6")
        self.update_idletasks()
        
        self.sim_state.avanzar_al_siguiente_evento()
        
        self.btn_continuar.config(state="normal", text="CONTINUAR", bg="#2ecc71")
        self.actualizar_info()

    def abrir_configuracion(self):
        win = tk.Toplevel(self)
        win.title("Configuración")
        win.geometry("300x200")
        tk.Label(win, text="Modificar Velocidad").pack(pady=10)
        
        for tren in self.sim_state.trenes:
            f = tk.Frame(win)
            f.pack(fill="x", padx=10, pady=5)
            tk.Label(f, text=tren.nombre).pack(side="left")
            
            def set_vel(t=tren):
                limit = 120
                if "BMU" in t.nombre: limit = 160
                
                v = simpledialog.askinteger("Velocidad", f"Km/h para {t.nombre}\n(Max {limit}):", parent=win, minvalue=1, maxvalue=limit)
                if v: t.velocidad_max = v
            
            limite_texto = "160" if "BMU" in tren.nombre else "120"
            tk.Button(f, text=f"Cambiar (Max {limite_texto})", command=set_vel).pack(side="right")

    def dibujar_mapa(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        margen = 50
        y = h / 2
        largo = w - 100
        factor = largo / 467.0 
        
        self.canvas.create_line(margen, y, w - margen, y, width=4, fill=settings.COLOR_VIA)

        for est in self.sim_state.estaciones:
            x = margen + (est.km * factor)
            self.canvas.create_oval(x-12, y-12, x+12, y+12, fill=settings.COLOR_ESTACION)
            self.canvas.create_text(x, y + 30, text=est.nombre, font=("Arial", 9, "bold"))
            
            if len(est.cola_pasajeros) > 0:
                self.canvas.create_text(x, y - 30, text=f"👤{len(est.cola_pasajeros)} p", fill="blue")

        for tren in self.sim_state.trenes:
            x = margen + (tren.km_actual * factor)
            color = settings.COLOR_TREN_IDA if tren.direccion == 1 else settings.COLOR_TREN_VUELTA
            
            if tren.estado == "ROTANDO": color = "orange"
            if tren.estado == "EN_ROTACION_ESPERA": color = "#d35400"
            
            self.canvas.create_rectangle(x-15, y-15, x+15, y, fill=color)
            
            n_vag = len(tren.vagones)
            ocup = tren.get_ocupacion_total()
            self.canvas.create_text(x, y-40, text=f"{tren.nombre}\n{n_vag} vag\n({ocup} p)", font=("Arial", 7, "bold"))

    def actualizar_info(self):
        self.lbl_hora.config(text=self.sim_state.hora_actual.strftime("%H:%M"))

        curr = len(self.sim_state.historial_eventos)
        if curr > self.last_event_count:
            for i in range(self.last_event_count, curr):
                ev = self.sim_state.historial_eventos[i]
                self.list_eventos.insert(0, f"[{ev['hora']}] {ev['descripcion']}")
            self.last_event_count = curr

        tot_pax = sum(t.get_ocupacion_total() for t in self.sim_state.trenes)
        tot_esp = sum(len(e.cola_pasajeros) for e in self.sim_state.estaciones)
        self.lbl_ocupacion.config(text=f"Ocupación: {tot_pax}")
        self.lbl_espera.config(text=f"Esperando: {tot_esp}")
        
        self.dibujar_mapa()
