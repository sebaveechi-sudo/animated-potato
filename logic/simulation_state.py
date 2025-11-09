# logic/simulation_state.py
from datetime import datetime

class SimulationState:
    def __init__(self):
        # Fecha y hora inicial por defecto (puede ser sobreescrita al cargar)
        self.hora_actual = datetime(2025, 1, 1, 8, 0, 0)
        self.trenes_activos = []
        self.estaciones_activas = []
        self.simulacion_corriendo = False

    def avanzar_tiempo(self, minutos=1):
        # Lógica futura para avanzar el reloj
        pass
