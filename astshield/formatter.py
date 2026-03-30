import ast

def generate_code_from_ast(tree):
    """
    Convierte un Árbol de Sintaxis Abstracta (AST) de vuelta a código fuente Python.

    Antes de realizar la conversión, esta función repara las ubicaciones espaciales
    (números de línea y columna) de los nodos del árbol. Esto es estrictamente
    necesario porque las transformaciones previas pueden haber alterado la 
    estructura, dejando nodos sin coordenadas válidas.

    Parameters
    ----------
    tree : ast.AST
        El nodo raíz del Árbol de Sintaxis Abstracta que se desea convertir.

    Returns
    -------
    str
        Una cadena de texto que contiene el código fuente de Python válido y
        ejecutable correspondiente al árbol proporcionado.
    """
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def save_code_to_file(code_string, output_path):
    """
    Guarda una cadena de texto (el código ofuscado) en un archivo físico.

    Utiliza codificación UTF-8 para garantizar que cualquier carácter especial
    (incluyendo acentos en comentarios o strings) se conserve correctamente
    sin importar el sistema operativo en el que se ejecute la librería.

    Parameters
    ----------
    code_string : str
        El código fuente en formato de texto que se desea guardar.
    output_path : str
        La ruta completa o relativa y el nombre del archivo de destino 
        (ej. 'salida/script_ofuscado.py').

    Returns
    -------
    None
    """
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(code_string)