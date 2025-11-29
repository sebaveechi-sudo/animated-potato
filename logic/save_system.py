import json
import os

class SaveSystem:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def guardar_simulacion(self, estado_simulacion, nombre_archivo="partida_guardada.json"):
        """
        Guarda el estado actual de la simulación en un archivo JSON.
        """
        ruta_completa = os.path.join(self.data_dir, nombre_archivo)
        print(f"Guardando simulación en {ruta_completa}...")
        pass

    def cargar_simulacion(self, nombre_archivo):
        """
        Carga un estado de simulación desde un archivo JSON.
        """
        ruta_completa = os.path.join(self.data_dir, nombre_archivo)
        print(f"Cargando simulación desde {ruta_completa}...")
        pass
