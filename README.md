# INFO081-CP-ProyectoTrenes

## Resumen de la Propuesta
Este proyecto implementa el "Sistema de Simulación de Tráfico Ferroviario" para la Empresa de Ferrocarriles del Estado (EFE). El sistema permite a un "Operario" gestionar trenes, estaciones y rutas en una simulación basada en turnos y eventos. El objetivo principal es proveer una herramienta para la toma de decisiones que optimice el flujo de pasajeros y mejore la eficiencia de la red ferroviaria.

## Integrantes del Equipo
* Cristóbal Aguilar
* Agustín Aravena
* José Castillo
* Sebastián Veechi
* Ignasio Vergara

## Indicadores de Interfaz [RF07]
La interfaz principal incluirá dos indicadores clave para el monitoreo del sistema:
1.  **Tasa de Ocupación Global:** Una barra de progreso que muestra visualmente el porcentaje promedio de ocupación de todos los trenes activos en la red.
2.  **Tiempo de Espera Promedio:** Un indicador numérico (acompañado de un ícono de reloj de arena) que muestra el tiempo promedio actual que los pasajeros han estado esperando en las estaciones.

## Persistencia de Datos
El sistema utilizará archivos **JSON** para la persistencia de datos debido a su capacidad para manejar estructuras anidadas y su legibilidad. Los datos se guardarán en una carpeta local (por defecto `data/`) organizados de la siguiente manera:
* `inicio_base.json`: Configuración inicial de estaciones y trenes base.
* `linea_temporal_X.json`: Registro de eventos pasados y futuros.
* `partida_guardada_Y.json`: Estado completo de una simulación en un momento específico (hora actual, estados de trenes y estaciones).

## Cómo ejecutar el proyecto
Para correr el simulador, asegúrate de tener Python 3 instalado.

1.  Abre una terminal o línea de comandos.
2.  Navega hasta la carpeta raíz del proyecto:
    ```bash
    cd ruta/a/INFO081-CP-ProyectoTrenes
    ```
3.  Ejecuta el archivo principal:
    ```bash
    python main.py
    ```
