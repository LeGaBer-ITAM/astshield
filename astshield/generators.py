import random
import string

def generate_random_name(length=12):
    """
    Genera un nombre de variable aleatorio válido para la sintaxis de Python.

    La función garantiza que el primer carácter sea siempre una letra para evitar 
    errores del tipo SyntaxError, ya que los identificadores en Python no pueden comenzar con números. 
    El resto de los caracteres son una selección aleatoria alfanumérica.

    Parameters
    ----------
    length : int, optional
        La longitud total de la cadena de texto a generar. Debe ser un número 
        entero positivo. El valor por defecto es 12.

    Returns
    -------
    str
        Una cadena de texto alfanumérica generada aleatoriamente que cumple con 
        las reglas de nomenclatura para variables, funciones o clases en Python.
    """
    first_char = random.choice(string.ascii_letters)
    
    pool_of_chars = string.ascii_letters + string.digits
    
    rest_chars = ''.join(random.choice(pool_of_chars) for _ in range(length - 1))
    
    return first_char + rest_chars