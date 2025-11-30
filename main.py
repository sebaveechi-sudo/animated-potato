import tkinter as tk
from config import settings
from logic.simulation_state import SimulationState
from ui.menu_window import MenuWindow
from ui.simulation_window import SimulationWindow

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Ferroviario EFE - Grupo CP")
        self.geometry(f"{settings.ANCHO_VENTANA}x{settings.ALTO_VENTANA}")
        
        self.estado_simulacion = SimulationState()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MenuWindow, SimulationWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuWindow")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    app = MainApp()
    app.mainloop()
