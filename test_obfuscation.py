import ast
import io
import contextlib
from astshield.transformer import Obfuscator
from astshield.formatter import generate_code_from_ast

def ejecutar_prueba_completa():
    # 1. Leemos el archivo real
    print("[*] Leyendo archivo objetivo: boveda.py...")
    try:
        with open("boveda.py", "r", encoding="utf-8") as f:
            codigo_original = f.read()
    except FileNotFoundError:
        print("[-] Error: No se encontró boveda.py en este directorio.")
        return

    # 2. Ofuscamos el código
    print("[*] Ofuscando el código...")
    arbol = ast.parse(codigo_original)
    ofuscador = Obfuscator()
    arbol_ofuscado = ofuscador.visit(arbol)
    codigo_ofuscado = generate_code_from_ast(arbol_ofuscado)

    # 3. Capturamos la salida del código ORIGINAL
    print("[*] Ejecutando código ORIGINAL de forma invisible...")
    salida_original = io.StringIO()
    with contextlib.redirect_stdout(salida_original):
        # INYECTAMOS __name__ AQUÍ
        exec(codigo_original, {"__name__": "__main__"})
    texto_original = salida_original.getvalue()

    # 4. Capturamos la salida del código OFUSCADO
    print("[*] Ejecutando código OFUSCADO de forma invisible...")
    salida_ofuscada = io.StringIO()
    try:
        with contextlib.redirect_stdout(salida_ofuscada):
            # INYECTAMOS __name__ AQUÍ TAMBIÉN
            exec(codigo_ofuscado, {"__name__": "__main__"})
        texto_ofuscado = salida_ofuscada.getvalue()
    except Exception as e:
        print(f"\n[-] Error crítico durante la ejecución del código ofuscado: {e}")
        return

    # 5. Imprimimos el veredicto y la comparación visual
    print("\n==================================================")
    print("            COMPARACIÓN DE RESULTADOS             ")
    print("==================================================")
    
    print("\n--- LO QUE IMPRIMIÓ EL CÓDIGO ORIGINAL ---")
    print(texto_original)
    
    print("--- LO QUE IMPRIMIÓ EL CÓDIGO OFUSCADO ---")
    print(texto_ofuscado)
    print("==================================================\n")

    # Prueba matemática estricta
    if texto_original == texto_ofuscado:
        print("[+] VEREDICTO: ¡Éxito absoluto! Las salidas de la terminal son byte por byte idénticas.")
        print("[+] La lógica matemática del programa sobrevivió intacta a la ofuscación.")
    else:
        print("[-] VEREDICTO: Peligro. Las salidas no coinciden. La ofuscación rompió el programa.")

if __name__ == "__main__":
    ejecutar_prueba_completa()

