import random
import string
import ast

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
        char_val = ord(text[i])
        key_val = ord(key[i % len(key)])
        xor_val = char_val ^ key_val
        encrypted_chars.append(f"\\x{xor_val:02x}")

    return "".join(encrypted_chars)

def generate_opaque_predicate():
    """
    Genera un predicado opaco utilizando la estrategia de 'Alias de Memoria'.
    Crea referencias cruzadas en el Heap (listas) para evadir la propagación
    de constantes de los analizadores estáticos.

    Returns
    -------
    list
        Una lista de nodos AST para la configuración inicial (creación del alias).
    ast.AST
        El nodo AST que representa la condición que siempre evalúa a True.
    """
    var_original = generate_random_name(length=6)
    var_alias = generate_random_name(length=6)
    val_inicial = random.randint(1, 50)
    val_final = random.randint(51, 100)
    setup_code = f"""
{var_original} = [{val_inicial}]
{var_alias} = {var_original}
{var_alias}[0] = {val_final}
"""
    equation_code = f"{var_original}[0] == {val_final}"
    setup_nodes = ast.parse(setup_code.strip()).body 
    equation_node = ast.parse(equation_code.strip()).body[0].value
    
    return setup_nodes, equation_node