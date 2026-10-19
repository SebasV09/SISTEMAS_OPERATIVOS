"""
Version 3 - CON SEMAFORO (threading.Semaphore)
Simulador de inscripcion de materias.

Idea: el semaforo ES el contador de cupos. Arranca en 5 y cada
estudiante que logra "tomar" (acquire) un permiso queda inscrito.
Cuando el semaforo llega a 0, los demas no pueden tomar ninguno.
"""
import threading
import time
import random

CUPOS_INICIALES = 5
NUM_ESTUDIANTES = 10

inscritos = []
semaforo_cupos = threading.Semaphore(CUPOS_INICIALES)  # 5 permisos = 5 cupos
barrera = threading.Barrier(NUM_ESTUDIANTES)


def estudiante(id_estudiante):
    barrera.wait()  # todos le dan clic al mismo tiempo

    # SECCION CRITICA protegida por el semaforo
    if semaforo_cupos.acquire(blocking=False):
        time.sleep(random.uniform(0.001, 0.01))  # mismo retardo que v1 y v2
        inscritos.append(id_estudiante)
        print(f"Estudiante {id_estudiante:2d}: INSCRITO")
    else:
        print(f"Estudiante {id_estudiante:2d}: sin cupo")
    # FIN SECCION CRITICA
    # No se hace release(): el cupo queda ocupado por el estudiante inscrito.


def main():
    hilos = [threading.Thread(target=estudiante, args=(i,))
             for i in range(1, NUM_ESTUDIANTES + 1)]

    inicio = time.perf_counter()
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    duracion = time.perf_counter() - inicio

    cupos_finales = CUPOS_INICIALES - len(inscritos)

    print("\n--- RESULTADO (semaforo) ---")
    print(f"Cupos iniciales : {CUPOS_INICIALES}")
    print(f"Estudiantes     : {NUM_ESTUDIANTES}")
    print(f"Inscritos       : {len(inscritos)}")
    print(f"Cupos finales   : {cupos_finales}")
    print(f"Tiempo          : {duracion:.4f} s")
    if len(inscritos) == CUPOS_INICIALES:
        print("OK: se respetaron los cupos")
    else:
        print("ERROR: no se respetaron los cupos")


if __name__ == "__main__":
    main()
