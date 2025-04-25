from bacteria import bacteria
from chemiotaxis import chemiotaxis
import numpy
from multiprocessing import Pool
import copy
import time

# Clonación de la mejor bacteria
def clonarBest(veryBest, best):    
    veryBest.matrix.seqs = numpy.array(copy.deepcopy(best.matrix.seqs))
    veryBest.blosumScore = best.blosumScore
    veryBest.fitness = best.fitness
    veryBest.interaction = best.interaction

# Validación de secuencias
# Se comparan las secuencias originales con las generadas por el algoritmo
def validarSecuencias(path, veryBest):
    tempBacteria = bacteria(path)
    tempBacteria.matrix.seqs = numpy.array(veryBest.matrix.seqs)
    for i in range(len(tempBacteria.matrix.seqs)):
        tempBacteria.matrix.seqs[i] = tempBacteria.matrix.seqs[i].replace("-", "")
    for i in range(len(tempBacteria.matrix.seqs)):
        if tempBacteria.matrix.seqs[i] != original.matrix.seqs[i]:
            print("*****************Secuencias no coinciden********************")
            return

# Limpieza de argumentos innecesarios
def evaluar_bacteria(args):
    bacteria, tumbo = args
    bacteria.tumboNado(tumbo)
    bacteria.autoEvalua()
    return bacteria

if __name__ == '__main__':
    # Configuración inicial
    poblacion = []
    path = "C:\\secuenciasBFOA\\multifasta.fasta"
    numeroDeBacterias = 15
    numRandomBacteria = 3
    iteraciones = 30
    tumbo = 1
    dAttr = 0.1
    wAttr = 0.2
    hRep = dAttr
    wRep = 10
    chemio = chemiotaxis()
    veryBest = bacteria(path)
    original = bacteria(path)
    globalNFE = 0



    # Inicializar la población de bacterias
    for i in range(numeroDeBacterias):
        poblacion.append(bacteria(path))

    # Evaluar la población inicial
    for iteracion in range(iteraciones):
        factor = iteracion / iteraciones
        dAttr_iter = dAttr * (1 - factor)
        wAttr_iter = wAttr * (1 - factor)
        hRep_iter = hRep * (1 + factor)
        wRep_iter = wRep * (1 + factor)

        # Evaluar la población de bacterias en paralelo
        args = [(b, tumbo) for b in poblacion]

        # Usar Pool para evaluar las bacterias en paralelo
        with Pool() as pool:
            poblacion = pool.map(evaluar_bacteria, args)

        # Actualizar la población con los resultados de la evaluación
        chemio.doChemioTaxis(poblacion, dAttr_iter, wAttr_iter, hRep_iter, wRep_iter)
        globalNFE += chemio.parcialNFE
        best = max(poblacion, key=lambda x: x.fitness)

        # Actualizar el mejor individuo encontrado hasta ahora
        if best.fitness > veryBest.fitness:
            clonarBest(veryBest, best)
        
        # Imprimir información de la iteración
        print(f"Iteración {iteracion} | BEST: {poblacion.index(best)} | "
            f"Fitness: {best.fitness:.4f} | Blosum: {best.blosumScore} | "
            f"Interacción: {best.interaction:.4f} | NFE: {globalNFE}")

                
        # Clonación y eliminación de bacterias
        eliminar_porcentaje = 0.5 - (0.3 * factor)
        chemio.eliminarClonar(path, poblacion)
        chemio.insertRamdomBacterias(path, numRandomBacteria, poblacion)

        print("Población:", len(poblacion))
        

    
    veryBest.showGenome()
    validarSecuencias(path, veryBest)

