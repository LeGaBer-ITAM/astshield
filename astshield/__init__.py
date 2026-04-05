import ast
from .transformer import Obfuscator
from .formatter import generate_code_from_ast

def obfuscate_file(input_path, output_path, default_level=3):
    """
    Lee un archivo de Python, lo ofusca y guarda el resultado en un nuevo archivo.

    Esta función actúa como el punto de entrada principal para el consumidor final.
    Carga el código fuente, aplica las transformaciones de AstShield respetando
    los niveles de protección definidos mediante decoradores o el nivel por defecto,
    y escribe el código resultante en el destino especificado.

    Parameters
    ----------
    input_path : str
        Ruta al archivo .py original que se desea proteger.
    output_path : str
        Ruta donde se guardará el archivo ofuscado resultante.
    default_level : int, optional
        Nivel de protección global (0-3) que se aplicará a las funciones 
        que no tengan un decorador `@protect` explícito. Por defecto es 3.

    Returns
    -------
    bool
        True si la operación fue exitosa, False en caso contrario.

    Raises
    ------
    FileNotFoundError
        Si el archivo de entrada no existe en la ruta especificada.
    SyntaxError
        Si el código fuente original contiene errores de sintaxis.
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        ofuscador = Obfuscator()
        ofuscador.current_level = default_level
        obfuscated_tree = ofuscador.visit(tree)
        obfuscated_code = generate_code_from_ast(obfuscated_tree)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(obfuscated_code)
            
        return True

    except (FileNotFoundError, SyntaxError, Exception):
        return False