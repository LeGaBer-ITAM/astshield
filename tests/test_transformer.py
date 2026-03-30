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