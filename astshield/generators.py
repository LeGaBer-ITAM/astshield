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

def generate_random_key(length=8):
    """
    Genera una clave criptográfica aleatoria para el cifrado XOR.

    Parameters
    ----------
    length : int, optional
        La longitud de la clave en caracteres. El valor por defecto es 8.

    Returns
    -------
    str
        Una cadena alfanumérica aleatoria que se usará como clave simétrica.
    """
    pool_of_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(pool_of_chars) for _ in range(length))

def xor_encrypt_string(text, key):
    """
    Cifra una cadena de texto utilizando la operación lógica XOR.

    Itera sobre cada carácter del texto original y de la clave. Convierte ambos
    a sus valores enteros (ASCII/Unicode), aplica la operación XOR (^) y 
    convierte el resultado a su representación hexadecimal.

    Parameters
    ----------
    text : str
        El texto en claro que se desea ocultar.
    key : str
        La clave criptográfica generada previamente.

    Returns
    -------
    str
        Una cadena hexadecimal que representa los bytes cifrados 
        (ej. '\\x1a\\x0b\\x4f...').
    """
    encrypted_chars = []
    
    for i in range(len(text)):
        # Obtener el valor entero del carácter del texto
        char_val = ord(text[i])
        
        # Obtener el valor entero del carácter de la clave correspondiente
        # Usamos el operador módulo (%) para que la clave se repita si el 
        # texto es más largo que la clave.
        key_val = ord(key[i % len(key)])
        
        # Aplicar XOR bit a bit
        xor_val = char_val ^ key_val
        
        # Formatear como un byte hexadecimal de dos dígitos (ej. \x0a)
        encrypted_chars.append(f"\\x{xor_val:02x}")
        
    return "".join(encrypted_chars)