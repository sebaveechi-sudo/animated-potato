class Pasajero:
    def __init__(self, id_p, origen_id, destino_id, hora_llegada_estacion):
        self.id = id_p
        self.origen_id = origen_id
        self.destino_id = destino_id
        self.hora_llegada_estacion = hora_llegada_estacion
        self.esperando_desde = hora_llegada_estacion

class Estacion:
    def __init__(self, id_est, nombre, km_ubicacion):
        self.id = id_est
        self.nombre = nombre
        self.km = km_ubicacion  
        self.cola_pasajeros = [] 

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "km": self.km,
            "pasajeros_esperando": len(self.cola_pasajeros)
        }

class Tren:
    def __init__(self, id_tren, modelo, capacidad, velocidad_max, km_actual=0):
        self.id = id_tren
        self.modelo = modelo
        self.capacidad = capacidad
        self.velocidad_max = velocidad_max
        self.km_actual = km_actual 
        self.direccion = 1  
        self.estado = "EN_ESTACION" 
        self.pasajeros = []
        self.proxima_estacion_id = None

    def to_dict(self):
        return {
            "id": self.id,
            "modelo": self.modelo,
            "km_actual": self.km_actual,
            "direccion": self.direccion,
            "ocupacion": len(self.pasajeros),
            "capacidad": self.capacidad
        }
