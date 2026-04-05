import ast
import io
import contextlib
from astshield.transformer import Obfuscator
from astshield.formatter import generate_code_from_ast

def test_execution_equivalence():
    """
    Prueba que el código ofuscado produce exactamente el mismo resultado 
    matemático y de salida (stdout) que el código original.
    """
    # 1. Definir el código de prueba
    source_code = """
def calcular_area(base, altura):
    area = (base * altura) / 2
    return area

resultado = calcular_area(10, 5)
print(resultado)
"""

    # 2. Ofuscar el código
    tree = ast.parse(source_code)
    obfuscator = Obfuscator()
    obfuscated_tree = obfuscator.visit(tree)
    obfuscated_code = generate_code_from_ast(obfuscated_tree)

    # 3. Capturar la salida del código original
    original_output = io.StringIO()
    with contextlib.redirect_stdout(original_output):
        exec(source_code, {})

    # 4. Capturar la salida del código ofuscado
    obfuscated_output = io.StringIO()
    with contextlib.redirect_stdout(obfuscated_output):
        exec(obfuscated_code, {})

    # 5. Afirmar (Assert) que las salidas son idénticas
    assert original_output.getvalue() == obfuscated_output.getvalue()
    
    # 6. Afirmar que el código realmente cambió (no son el mismo texto)
    assert source_code.strip() != obfuscated_code.strip()

def test_string_encryption_equivalence():
    """
    Prueba que el cifrado polimórfico de cadenas (XOR) se aplique correctamente
    y que el código ofuscado sea capaz de descifrar las cadenas en tiempo 
    de ejecución sin alterar la lógica del programa.
    """
    # 1. Definir un código rico en cadenas de texto (strings)
    source_code = """
def generar_saludo(nombre):
    prefijo = "Mensaje confidencial: "
    saludo = "Bienvenido al sistema, "
    return prefijo + saludo + nombre

resultado = generar_saludo("Administrador")
print(resultado)
"""

    # 2. Ofuscar el código
    tree = ast.parse(source_code)
    obfuscator = Obfuscator()
    obfuscated_tree = obfuscator.visit(tree)
    obfuscated_code = generate_code_from_ast(obfuscated_tree)

    # 3. Capturar la salida original
    original_output = io.StringIO()
    with contextlib.redirect_stdout(original_output):
        exec(source_code, {})

    # 4. Capturar la salida ofuscada
    obfuscated_output = io.StringIO()
    with contextlib.redirect_stdout(obfuscated_output):
        exec(obfuscated_code, {})

    # 5. Afirmación de Ejecución: ¿Imprimen lo mismo?
    assert original_output.getvalue() == obfuscated_output.getvalue()

    # 6. Afirmación de Criptografía: ¿Desaparecieron las cadenas originales?
    cadenas_prohibidas = [
        "Mensaje confidencial: ", 
        "Bienvenido al sistema, ", 
        "Administrador"
    ]
    for cadena in cadenas_prohibidas:
        assert cadena not in obfuscated_code, f"Fallo de seguridad: La cadena '{cadena}' sobrevivió a la ofuscación en texto plano."
    
    # 7. Afirmación Estructural: ¿Se inyectó la función de descifrado?
    # Comprobamos que el motor de descifrado esté presente buscando operadores típicos (XOR)
    assert "^" in obfuscated_code or "chr" in obfuscated_code