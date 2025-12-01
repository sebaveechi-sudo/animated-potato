import json
import os
import random
from datetime import datetime, timedelta
from config import settings
from logic import datos_anexo
from models.entidades import Pasajero, Tren, Estacion, Vagon
from tkinter import messagebox

class SimulationState:
    def __init__(self):
        self.hora_actual = datetime(2015, 3, 1, 7, 0, 0)
        self.estaciones = datos_anexo.cargar_estaciones_base()
        self.trenes = datos_anexo.crear_flota_inicial()
        self._inicializar_vias()
        self.historial_eventos = [] 
        self.registrar_evento("Inicio de simulación", "SISTEMA")
        self.factor_demanda = 0.002 

        if not os.path.exists(settings.DATA_DIR):
            os.makedirs(settings.DATA_DIR)

    def _inicializar_vias(self):
        for tren in self.trenes:
            est = self._get_estacion_en_km(tren.km_actual)
            if est:
                est.ocupar_via(tren, tren.direccion)

    def registrar_evento(self, descripcion, tipo="INFO"):
        evento = {"hora": self.hora_actual.strftime("%H:%M:%S"), "descripcion": descripcion, "tipo": tipo}
        self.historial_eventos.append(evento)

    def avanzar_al_siguiente_evento(self):
        evento_encontrado = False
        ticks_max = 1440 
        ticks = 0

        while not evento_encontrado and ticks < ticks_max:
            self.hora_actual += timedelta(minutes=1)
            ticks += 1
            if 7 <= self.hora_actual.hour < 20:
                self._generar_pasajeros_poblacion()
            for tren in self.trenes:
                hubo_evento = self._procesar_tren(tren)
                if hubo_evento:
                    evento_encontrado = True
        return evento_encontrado

    def _procesar_tren(self, tren):
        if tren.estado == "ROTANDO":
            tren.tiempo_proceso += 1
            if tren.tiempo_proceso >= 10:
                tren.estado = "EN_ROTACION_ESPERA"
                tren.direccion *= -1
                tren.tiempo_proceso = 0
                est = self._get_estacion_en_km(tren.km_actual)
                self.registrar_evento(f"{tren.nombre} terminó giro en {est.nombre}", "TREN")
                if est.ocupar_via(tren, tren.direccion):
                    est.liberar_rotacion()
                    tren.estado = "EN_ESTACION"
                    self.registrar_evento(f"{tren.nombre} ingresó a vía regular", "TREN")
                return True
            return False

        if tren.estado == "EN_ROTACION_ESPERA":
            est = self._get_estacion_en_km(tren.km_actual)
            if est.ocupar_via(tren, tren.direccion):
                est.liberar_rotacion()
                tren.estado = "EN_ESTACION"
                self.registrar_evento(f"{tren.nombre} ingresó a vía regular", "TREN")
                return True
            return False

        if tren.estado == "EN_ESTACION":
            if 7 <= self.hora_actual.hour < 20:
                siguiente_est = self._get_siguiente_estacion(tren)
                puede_salir = False
                if siguiente_est:
                    if siguiente_est.hay_via_disponible(tren.direccion):
                        puede_salir = True
                else:
                    puede_salir = True 
                if puede_salir:
                    tren.estado = "EN_TRANSITO"
                    est_actual = self._get_estacion_en_km(tren.km_actual)
                    if est_actual: est_actual.liberar_via(tren, tren.direccion)
            return False

        if tren.estado == "EN_TRANSITO":
            velocidad_km_min = tren.velocidad_max / 60
            desplazamiento = velocidad_km_min * tren.direccion
            nuevo_km = tren.km_actual + desplazamiento

            for estacion in self.estaciones:
                distancia = abs(nuevo_km - estacion.km)
                if distancia < 2.0: 
                    es_extremo = (estacion.id == self.estaciones[0].id and tren.direccion == -1) or \
                                 (estacion.id == self.estaciones[-1].id and tren.direccion == 1)
                    if es_extremo:
                        if estacion.ocupar_rotacion(tren):
                            tren.km_actual = estacion.km
                            tren.estado = "ROTANDO"
                            tren.tiempo_proceso = 0
                            bajan, _ = self._manejar_carga_descarga(tren, estacion, solo_baja=True)
                            self.registrar_evento(f"{tren.nombre} inicia giro en {estacion.nombre}. Bajan {bajan}", "TREN")
                            return True
                        else:
                            return False 
                    if estacion.ocupar_via(tren, tren.direccion):
                        tren.km_actual = estacion.km
                        tren.estado = "EN_ESTACION"
                        bajan, suben = self._manejar_carga_descarga(tren, estacion)
                        self.registrar_evento(f"{tren.nombre} llegó a {estacion.nombre}. Bajan:{bajan} Suben:{suben}", "TREN")
                        return True
                    else:
                        return False

            tren.km_actual = nuevo_km
            if tren.km_actual < 0: tren.km_actual = 0
            if tren.km_actual > 467: tren.km_actual = 467
            return False
        return False

    def _get_estacion_en_km(self, km):
        for est in self.estaciones:
            if abs(est.km - km) < 0.1: return est
        return None
    
    def _get_siguiente_estacion(self, tren):
        est_actual = self._get_estacion_en_km(tren.km_actual)
        if not est_actual: return None
        idx = -1
        for i, e in enumerate(self.estaciones):
            if e.id == est_actual.id: idx = i; break
        sig_idx = idx + (1 if tren.direccion == 1 else -1)
        if 0 <= sig_idx < len(self.estaciones): return self.estaciones[sig_idx]
        return None

    def _manejar_carga_descarga(self, tren, estacion, solo_baja=False):
        bajan_total = 0
        for vagon in tren.vagones:
            bajan = int(len(vagon.pasajeros) * 0.3)
            bajan_total += bajan
            vagon.pasajeros = vagon.pasajeros[bajan:]
        suben_total = 0
        if not solo_baja:
            pasajeros_restantes = []
            for p in estacion.cola_pasajeros:
                es_sur = p.destino_id > p.origen_id
                tren_sur = tren.direccion == 1
                if es_sur == tren_sur:
                    subido = False
                    for vagon in tren.vagones:
                        if len(vagon.pasajeros) < vagon.capacidad:
                            vagon.pasajeros.append(p)
                            subido = True
                            suben_total += 1
                            break
                    if not subido: pasajeros_restantes.append(p)
                else:
                    pasajeros_restantes.append(p)
            estacion.cola_pasajeros = pasajeros_restantes
        return bajan_total, suben_total

    def _generar_pasajeros_poblacion(self):
        for estacion in self.estaciones:
            demanda_diaria = estacion.poblacion * 0.20
            mins_operacion = 13 * 60
            pax_minuto = (demanda_diaria / mins_operacion) * self.factor_demanda
            seed = int(self.hora_actual.timestamp()) + int(estacion.id.split('-')[1])
            rng = random.Random(seed)
            cantidad = int(pax_minuto)
            if rng.random() < (pax_minuto - cantidad): cantidad += 1
            if cantidad == 0 and rng.random() < 0.1: cantidad = 1
            if cantidad > 60: cantidad = 60 
            for _ in range(cantidad):
                pid = int(self.hora_actual.timestamp() * 1000) + rng.randint(0, 9999)
                destinos = [e for e in self.estaciones if e.id != estacion.id]
                if not destinos: continue
                destino = rng.choice(destinos)
                p = Pasajero(pid, estacion.id, destino.id, self.hora_actual)
                estacion.cola_pasajeros.append(p)

    def guardar_partida(self):
        data = {
            "hora": self.hora_actual.strftime("%Y-%m-%d %H:%M:%S"),
            "historial": self.historial_eventos,
            "trenes": [t.to_dict() for t in self.trenes],
            "estaciones": [e.to_dict() for e in self.estaciones],
            "factor_demanda": self.factor_demanda
        }
        path = os.path.join(settings.DATA_DIR, "partida_guardada.json")
        with open(path, "w") as f: json.dump(data, f, indent=4)
        print(f"Partida guardada en {path}")
        self.registrar_evento("Partida Guardada", "SISTEMA")

    def cargar_partida(self):
        path = os.path.join(settings.DATA_DIR, "partida_guardada.json")
        if not os.path.exists(path):
            messagebox.showwarning("Aviso", "No hay partida guardada.")
            return
        try:
            with open(path, "r") as f: data = json.load(f)
            self.hora_actual = datetime.strptime(data["hora"], "%Y-%m-%d %H:%M:%S")
            self.historial_eventos = data.get("historial", [])
            self.factor_demanda = data.get("factor_demanda", 0.002)
            self.trenes = []
            for t_data in data["trenes"]:
                tren = Tren(t_data["id"], t_data["nombre"], 0, km_actual=t_data["km_actual"])
                tren.direccion = t_data["direccion"]
                tren.estado = t_data["estado"]
                if "BMU" in tren.nombre: tren.velocidad_max = 160
                else: tren.velocidad_max = 120
                tren.vagones = []
                for v_data in t_data["vagones"]:
                    vagon = Vagon(v_data["capacidad"])
                    for _ in range(v_data["ocupacion"]):
                        vagon.pasajeros.append(Pasajero(0, "X", "X", self.hora_actual))
                    tren.vagones.append(vagon)
                self.trenes.append(tren)
            self.estaciones = []
            base_ests = datos_anexo.cargar_estaciones_base()
            for i, e_data in enumerate(data["estaciones"]):
                base = base_ests[i]
                est = Estacion(base.id, base.nombre, base.km, base.poblacion)
                for _ in range(e_data["pasajeros_esperando"]):
                    est.cola_pasajeros.append(Pasajero(0, "X", "X", self.hora_actual))
                self.estaciones.append(est)
            self._inicializar_vias()
            messagebox.showinfo("Carga", f"Cargado: {self.hora_actual}")
            self.registrar_evento("Partida Cargada", "SISTEMA")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar: {e}")
