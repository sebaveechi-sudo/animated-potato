# ui/menu_window.py
import tkinter as tk
from config import settings

class MenuWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white") 

        label = tk.Label(self, text="Simulador de Tráfico Ferroviario EFE", font=("Arial", 24))
        label.pack(pady=50)

        btn_nueva = tk.Button(self, text="Nueva Simulación", command=lambda: controller.show_frame("SimulationWindow"), width=20, height=2)
        btn_nueva.pack(pady=10)

        btn_cargar = tk.Button(self, text="Cargar Simulación", width=20, height=2)
        btn_cargar.pack(pady=10)

        btn_salir = tk.Button(self, text="Salir", command=parent.quit, width=20, height=2)
        btn_salir.pack(pady=10)
