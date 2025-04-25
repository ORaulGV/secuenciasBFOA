import csv
import os
import time

class RegistroCSV:
    def __init__(self, nombre_archivo="registroSecuenciasBFOA.csv"):
        self.nombre_archivo = nombre_archivo
        self.inicio_tiempo = time.time()

        # Crear archivo y encabezados si no existe
        if not os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Iteración", "BEST", "Fitness", "BlosumScore", "Interacción", "NFE", "TiempoEjec(seg)"])

    def guardar(self, iteracion, best, fitness, blosumScore, interaccion, nfe):
        tiempo = round(time.time() - self.inicio_tiempo, 4)
        with open(self.nombre_archivo, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([iteracion, best, fitness, blosumScore, interaccion, nfe, tiempo])
