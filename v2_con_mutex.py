"""
Version 2 - CON MUTEX (threading.Lock)
Simulador de inscripcion de materias.
"""
import threading
import time
import random

CUPOS_INICIALES = 5
NUM_ESTUDIANTES = 10

cupos = CUPOS_INICIALES
inscritos = []
mutex = threading.Lock()
barrera = threading.Barrier(NUM_ESTUDIANTES)


def estudiante(id_estudiante):
    global cupos
    barrera.wait()

    # ---- SECCION CRITICA protegida por mutex ----
    # verificar y modificar deben ser UNA sola operacion indivisible
    with mutex:
        if cupos > 0:
            time.sleep(random.uniform(0.001, 0.01))  # mismo retardo que v1
            cupos -= 1
            inscritos.append(id_estudiante)
            print(f"Estudiante {id_estudiante:2d}: INSCRITO")
        else:
            print(f"Estudiante {id_estudiante:2d}: sin cupo")
    # ---- FIN SECCION CRITICA ----


def main():
    hilos = [threading.Thread(target=estudiante, args=(i,))
             for i in range(1, NUM_ESTUDIANTES + 1)]

    inicio = time.perf_counter()
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    duracion = time.perf_counter() - inicio

    print("\n--- RESULTADO (mutex) ---")
    print(f"Cupos iniciales : {CUPOS_INICIALES}")
    print(f"Estudiantes     : {NUM_ESTUDIANTES}")
    print(f"Inscritos       : {len(inscritos)}")
    print(f"Cupos finales   : {cupos}")
    print(f"Tiempo          : {duracion:.4f} s")
    assert len(inscritos) == CUPOS_INICIALES and cupos == 0


if __name__ == "__main__":
    main()