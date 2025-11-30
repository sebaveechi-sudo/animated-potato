import json
import os
import random
from datetime import datetime, timedelta
from config import settings
from logic import datos_anexo
from models.entidades import Pasajero

class SimulationState:
    def __init__(self):
        self.hora_actual = datetime(2025, 11, 3, 6, 0, 0)
        self.estaciones = datos_anexo.cargar_estaciones_base()
        self.trenes = datos_anexo.crear_flota_inicial()
        self.simulacion_activa = False
        self.velocidad_simulacion = 1

        if not os.path.exists(settings.DATA_DIR):
            os.makedirs(settings.DATA_DIR)

    def iniciar_pausar(self):
        self.simulacion_activa = not self.simulacion_activa

    def update(self):
        """Actualiza la lógica 1 'tick' de tiempo"""
        if not self.simulacion_activa:
            return

        self.hora_actual += timedelta(minutes=1)

        if self.hora_actual.minute % 20 == 0:
            self._generar_pasajeros_random()

        for tren in self.trenes:
            self._procesar_tren(tren)

    def _procesar_tren(self, tren):
        velocidad_km_min = tren.velocidad_max / 60
        desplazamiento = velocidad_km_min * tren.direccion

        tren.km_actual += desplazamiento

        for estacion in self.estaciones:
            distancia = abs(tren.km_actual - estacion.km)
            if distancia < 1.5: 
                self._manejar_parada(tren, estacion)

        if tren.km_actual <= 0:
            tren.direccion = 1
            tren.km_actual = 0
        elif tren.km_actual >= 398:
            tren.direccion = -1
            tren.km_actual = 398

    def _manejar_parada(self, tren, estacion):
        bajan = int(len(tren.pasajeros) * 0.3)
        tren.pasajeros = tren.pasajeros[bajan:]

        cupos = tren.capacidad - len(tren.pasajeros)
        if cupos > 0 and estacion.cola_pasajeros:
            suben = estacion.cola_pasajeros[:cupos]
            estacion.cola_pasajeros = estacion.cola_pasajeros[cupos:]
            tren.pasajeros.extend(suben)

    def _generar_pasajeros_random(self):
        estacion = random.choice(self.estaciones)
        cantidad = random.randint(5, 20)
        for _ in range(cantidad):
            p = Pasajero(id(object), estacion.id, "DESTINO_X", self.hora_actual)
            estacion.cola_pasajeros.append(p)

    def guardar_partida(self):
        data = {
            "hora": self.hora_actual.strftime("%Y-%m-%d %H:%M:%S"),
            "trenes": [t.to_dict() for t in self.trenes],
            "estaciones": [e.to_dict() for e in self.estaciones]
        }
        path = os.path.join(settings.DATA_DIR, "partida_guardada.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Partida guardada en {path}")

    def cargar_partida(self):
        path = os.path.join(settings.DATA_DIR, "partida_guardada.json")
        
        if not os.path.exists(path):
            print("AVISO: No existe archivo de guardado para cargar.")
            return 

        try:
            with open(path, "r") as f:
                data = json.load(f)
                self.hora_actual = datetime.strptime(data["hora"], "%Y-%m-%d %H:%M:%S")
            print("Partida cargada exitosamente.")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
