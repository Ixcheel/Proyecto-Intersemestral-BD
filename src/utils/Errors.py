import random, time
from sqlalchemy.exc import OperationalError

def reintentos(funcion, max_intentos=3):
    for intento in range(max_intentos):
        try:
            return funcion()
        except OperationalError as error:
            mensaje = str(error)
            if "40P01" in mensaje or "40001" in mensaje:
                if intento == max_intentos - 1:
                    raise error

                print("Reintentando")
                tiempo = 0.5 * (intento + 1)
                time.sleep(tiempo)
            else:
                raise error