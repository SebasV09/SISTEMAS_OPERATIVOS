"""
Version 1 - SIN PROTECCION (sin mutex ni semaforo)
Simulador de inscripcion de materias: muestra la condicion de carrera.
"""
import threading
import time
import random

CUPOS_INICIALES = 5
NUM_ESTUDIANTES = 10

cupos = CUPOS_INICIALES      # recurso compartido
inscritos = []               # estudiantes que lograron "inscribirse"

# Barrera: hace que los 10 hilos arranquen el intento al mismo tiempo
barrera = threading.Barrier(NUM_ESTUDIANTES)


def estudiante(id_estudiante):
    global cupos
    barrera.wait()  # todos le dan clic al mismo tiempo

    # ---- SECCION CRITICA (sin proteger) ----
    if cupos > 0:                                 # 1) verificar
        # En Python, la GIL esconde la carrera si el codigo es muy corto.
        # Este retardo simula el tiempo real de procesar la inscripcion
        # (consultar BD, validar prerrequisitos, etc.) y deja ver el problema.
        time.sleep(random.uniform(0.001, 0.01))
        cupos -= 1                                # 2) modificar
        inscritos.append(id_estudiante)
        print(f"Estudiante {id_estudiante:2d}: INSCRITO")
    # ---- FIN SECCION CRITICA ----
    else:
        print(f"Estudiante {id_estudiante:2d}: sin cupo")


def main():
    hilos = [threading.Thread(target=estudiante, args=(i,))
             for i in range(1, NUM_ESTUDIANTES + 1)]

    inicio = time.perf_counter()
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    duracion = time.perf_counter() - inicio

    print("\n--- RESULTADO (sin proteccion) ---")
    print(f"Cupos iniciales : {CUPOS_INICIALES}")
    print(f"Estudiantes     : {NUM_ESTUDIANTES}")
    print(f"Inscritos       : {len(inscritos)}")
    print(f"Cupos finales   : {cupos}")
    print(f"Tiempo          : {duracion:.4f} s")
    if len(inscritos) > CUPOS_INICIALES:
        print(f"ERROR: se inscribieron {len(inscritos) - CUPOS_INICIALES} "
              f"estudiantes de mas (condicion de carrera)")
    else:
        print("Esta vez no se vio el error; vuelve a correrlo.")


if __name__ == "__main__":
    main()