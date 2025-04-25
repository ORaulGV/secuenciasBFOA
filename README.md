Mejora del Algoritmo BFOA para Alineamiento de Secuencias

Se mejoró el algoritmo BFOA (Bacterial Foraging Optimization Algorithm), que alinea múltiples secuencias
biológicas. La versión original era funcional pero básica. En esta versión se agregaron varias mejoras importantes:

1. Quimiotaxis bacteriana
Se implementó una clase quimiotaxis.py, que permite que las bacterias interactúen entre sí
por medio de atracción y repulsión. Esto mejora la exploración y evita soluciones poco óptimas.

      Antes: Las bacterias actuaban solas.

      Ahora: Se consideran los efectos del grupo (quimiotaxis).

2. Paralelización

Ahora la evaluación de bacterias se hace en paralelo usando multiprocessing, lo que acelera el algoritmo.

3. Caché de evaluaciones

Se guarda el resultado de bacterias ya evaluadas, evitando cálculos repetidos y mejorando el rendimiento.

4. Parámetros adaptativos

Los parámetros del algoritmo se ajustan automáticamente en cada iteración, facilitando la convergencia.

5. Registro en CSV

Cada iteración se guarda en un archivo .csv con datos como fitness, interacción, tiempo de ejecución, etc.

6. Validación final

Se verifica que las secuencias finales mantengan la información original, sin errores por los gaps.


Conclusión

La nueva versión del algoritmo es más rápida, inteligente y robusta. Las bacterias ahora trabajan en grupo,
se evitan repeticiones, se guarda todo el progreso y se validan las secuencias finales. Esto mejora tanto el
rendimiento como la calidad de los alineamientos.

