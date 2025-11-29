from models.entidades import Estacion, Tren

def cargar_estaciones_base():
    datos = [
        ("EST-01", "Alameda", 0),
        ("EST-02", "San Bernardo", 16),
        ("EST-03", "Rancagua", 82),
        ("EST-04", "San Fernando", 134),
        ("EST-05", "Curicó", 185),
        ("EST-06", "Molina", 205),
        ("EST-07", "Talca", 248),
        ("EST-08", "San Javier", 269),
        ("EST-09", "Linares", 300),
        ("EST-10", "Parral", 340),
        ("EST-11", "San Carlos", 374),
        ("EST-12", "Chillán", 398)
    ]
    return [Estacion(d[0], d[1], d[2]) for d in datos]

def crear_flota_inicial():
    t1 = Tren("T-01", "UTS-444", 302, 140, km_actual=0)
    t2 = Tren("T-02", "UTS-444", 302, 140, km_actual=398) 
    t2.direccion = -1 
    return [t1, t2]
