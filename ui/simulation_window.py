import tkinter as tk
from config import settings

class SimulationWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.sim_state = controller.estado_simulacion

        self.top_bar = tk.Frame(self, bg=settings.COLOR_BARRA_SUPERIOR, height=60)
        self.top_bar.pack(side="top", fill="x")
        
        self.lbl_hora = tk.Label(self.top_bar, text="--:--", bg=settings.COLOR_BARRA_SUPERIOR, fg="white", font=("Arial", 16))
        self.lbl_hora.pack(side="left", padx=20)

        btn_guardar = tk.Button(self.top_bar, text="Guardar", command=self.sim_state.guardar_partida)
        btn_guardar.pack(side="right", padx=5, pady=10)
        
        btn_pausa = tk.Button(self.top_bar, text="Iniciar/Pausar", command=self.sim_state.iniciar_pausar)
        btn_pausa.pack(side="right", padx=5, pady=10)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.panel_lateral = tk.Frame(self, width=250, bg=settings.COLOR_FONDO)
        self.panel_lateral.pack(side="right", fill="y", padx=5)
        
        tk.Label(self.panel_lateral, text="Indicadores", font=("Arial", 14, "bold")).pack(pady=10)
        self.lbl_ocupacion = tk.Label(self.panel_lateral, text="Ocupación Global: 0%")
        self.lbl_ocupacion.pack(pady=5)
        
        self.lbl_espera = tk.Label(self.panel_lateral, text="Gente Esperando: 0")
        self.lbl_espera.pack(pady=5)

        tk.Button(self.panel_lateral, text="Volver al Menú", command=lambda: controller.show_frame("MenuWindow")).pack(side="bottom", pady=20)

        self.actualizar_gui()

    def dibujar_mapa(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        margen_x = 50
        largo_linea = w - 100
        y_pos = h / 2

        self.canvas.create_line(margen_x, y_pos, w - margen_x, y_pos, width=4, fill=settings.COLOR_VIA)

        factor_escala = largo_linea / 400 

        for est in self.sim_state.estaciones:
            x = margen_x + (est.km * factor_escala)
            self.canvas.create_oval(x-5, y_pos-5, x+5, y_pos+5, fill=settings.COLOR_ESTACION)
            self.canvas.create_text(x, y_pos + 20, text=est.nombre, font=("Arial", 8), angle=45, anchor="nw")
            if len(est.cola_pasajeros) > 0:
                 self.canvas.create_text(x, y_pos - 20, text=f"👤{len(est.cola_pasajeros)}", fill="blue", font=("Arial", 8))

        for tren in self.sim_state.trenes:
            x = margen_x + (tren.km_actual * factor_escala)
            color = settings.COLOR_TREN_IDA if tren.direccion == 1 else settings.COLOR_TREN_VUELTA

            self.canvas.create_rectangle(x-10, y_pos-15, x+10, y_pos-5, fill=color)
            self.canvas.create_text(x, y_pos-25, text=f"{tren.id}\n({len(tren.pasajeros)} pax)", font=("Arial", 7))

    def actualizar_gui(self):
        self.sim_state.update()

        hora_str = self.sim_state.hora_actual.strftime("%H:%M")
        self.lbl_hora.config(text=f"Hora: {hora_str}")

        total_pax = sum([len(t.pasajeros) for t in self.sim_state.trenes])
        total_cap = sum([t.capacidad for t in self.sim_state.trenes])
        ocupacion = (total_pax / total_cap * 100) if total_cap > 0 else 0
        
        total_espera = sum([len(e.cola_pasajeros) for e in self.sim_state.estaciones])

        self.lbl_ocupacion.config(text=f"Ocupación Trenes: {int(ocupacion)}%")
        self.lbl_espera.config(text=f"Gente Esperando: {total_espera}")

        if self.winfo_viewable():
            self.dibujar_mapa()

        self.after(100, self.actualizar_gui)
