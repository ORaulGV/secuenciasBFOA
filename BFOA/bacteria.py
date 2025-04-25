from fastaReader import fastaReader
import random
import numpy
import copy
from evaluadorBlosum import evaluadorBlosum

# ✅ Diccionario global para caché de evaluaciones
evaluaciones_cache = {}

class bacteria():

    def __init__(self, path):
        self.matrix = fastaReader(path)
        self.blosumScore = 0
        self.fitness = 0
        self.interaction = 0
        self.NFE = 0

    def showGenome(self):
        for seq in self.matrix.seqs:
            print(seq)

    def clonar(self, path):
        newBacteria = bacteria(path)
        newBacteria.matrix.seqs = numpy.array(copy.deepcopy(self.matrix.seqs))
        return newBacteria

    def tumboNado(self, numGaps):
        self.cuadra()
        matrixCopy = copy.deepcopy(self.matrix.seqs)
        matrixCopy = matrixCopy.tolist()
        gapRandomNumber = random.randint(0, numGaps)
        for i in range(gapRandomNumber):
            seqnum = random.randint(0, len(matrixCopy) - 1)
            pos = random.randint(0, len(matrixCopy[seqnum]))
            part1 = matrixCopy[seqnum][:pos]
            part2 = matrixCopy[seqnum][pos:]
            temp = "-".join([part1, part2])
            matrixCopy[seqnum] = temp
        matrixCopy = numpy.array(matrixCopy)
        self.matrix.seqs = matrixCopy

        self.cuadra()
        self.limpiaColumnas()

    def cuadra(self):
        seq = self.matrix.seqs
        maxLen = len(max(seq, key=len))
        for i in range(len(seq)):
            if len(seq[i]) < maxLen:
                seq[i] = seq[i] + "-" * (maxLen - len(seq[i]))
        self.matrix.seqs = numpy.array(seq)

    def gapColumn(self, col):
        return all(self.matrix.seqs[i][col] == "-" for i in range(len(self.matrix.seqs)))

    def limpiaColumnas(self):
        i = 0
        while i < len(self.matrix.seqs[0]):
            if self.gapColumn(i):
                self.deleteCulmn(i)
            else:
                i += 1

    def deleteCulmn(self, pos):
        for i in range(len(self.matrix.seqs)):
            self.matrix.seqs[i] = self.matrix.seqs[i][:pos] + self.matrix.seqs[i][pos + 1:]

    def getColumn(self, col):
        return [self.matrix.seqs[i][col] for i in range(len(self.matrix.seqs))]

    def autoEvalua(self):
        # ✅ Uso de caché para evitar reevaluaciones redundantes
        clave = tuple(map(tuple, self.matrix.seqs))
        if clave in evaluaciones_cache:
            self.blosumScore = evaluaciones_cache[clave]
        else:
            evaluador = evaluadorBlosum()
            score = 0
            for i in range(len(self.matrix.seqs[0])):
                column = self.getColumn(i)
                gapCount = column.count("-")
                column = [x for x in column if x != "-"]
                pares = self.obtener_pares_unicos(column)
                for par in pares:
                    score += evaluador.getScore(par[0], par[1])
                score -= gapCount * 2
            self.blosumScore = score
            evaluaciones_cache[clave] = score
        self.NFE += 1

    def obtener_pares_unicos(self, columna):
        pares_unicos = set()
        for i in range(len(columna)):
            for j in range(i + 1, len(columna)):
                par = tuple(sorted([columna[i], columna[j]]))
                pares_unicos.add(par)
        return list(pares_unicos)
