from models.entidades import Estacion, Tren

def cargar_estaciones_base():
    datos = [
        ("EST-01", "Estación Central", 0, 8242459),
        ("EST-02", "Rancagua", 87, 274407),
        ("EST-03", "Talca", 287, 242344),
        ("EST-04", "Chillán", 467, 204091)
    ]
    return [Estacion(d[0], d[1], d[2], d[3], vias_por_sentido=2) for d in datos]

def crear_flota_inicial():
    t1 = Tren("T-01", "Tren EMU", 120, km_actual=0)
    t1.direccion = 1 
    t2 = Tren("T-02", "Tren BMU", 160, km_actual=467)
    t2.direccion = -1 
    return [t1, t2]
