# main.py
import tkinter as tk
from config import settings
from ui.menu_window import MenuWindow
from ui.simulation_window import SimulationWindow
from logic.simulation_state import SimulationState

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador EFE - Grupo CP")
        self.geometry(f"{settings.ANCHO_VENTANA}x{settings.ALTO_VENTANA}")
        
        # Inicializar estado
        self.estado_simulacion = SimulationState()

        # Contenedor principal para las vistas
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Inicializar todas las ventanas
        for F in (MenuWindow, SimulationWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuWindow")

    def show_frame(self, page_name):
        '''Muestra una ventana por su nombre'''
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
