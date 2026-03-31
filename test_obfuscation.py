import ast
from astshield.transformer import Obfuscator
from astshield.formatter import generate_code_from_ast

def ejecutar_prueba_completa():
    # 1. Definimos un código fuente de ejemplo altamente legible y vulnerable
    codigo_original = """
def conectar_servidor(usuario, contraseña):
    direccion_ip = "192.168.1.100"
    puerto = "8080"
    
    print("Iniciando conexión al servidor...")
    
    if contraseña == "Admin_Secreto_2026!":
        print("Acceso concedido. Bienvenido, " + usuario)
        return True
    else:
        print("Error: Credenciales inválidas.")
        return False

# Simulamos la ejecución
conexion_exitosa = conectar_servidor("admin_root", "Admin_Secreto_2026!")
"""

    print("==================================================")
    print("               CÓDIGO ORIGINAL                    ")
    print("==================================================")
    print(codigo_original)

    # 2. Pasamos el código por nuestro motor de ofuscación
    arbol = ast.parse(codigo_original)
    ofuscador = Obfuscator()
    arbol_ofuscado = ofuscador.visit(arbol)
    
    # 3. Reconstruimos el texto
    codigo_ofuscado = generate_code_from_ast(arbol_ofuscado)

    print("\n==================================================")
    print("               CÓDIGO OFUSCADO                    ")
    print("==================================================")
    print(codigo_ofuscado)
    print("\n==================================================")
    
    # 4. Prueba de fuego: ¿Sigue funcionando la lógica original?
    print("[*] Ejecutando el código ofuscado en la memoria de Python...\n")
    try:
        # Usamos exec() para correr el código basura generado y ver si imprime lo correcto
        exec(codigo_ofuscado, {})
        print("\n[+] ¡Éxito! El código ofuscado se ejecutó sin errores.")
    except Exception as e:
        print(f"\n[-] Error crítico durante la ejecución: {e}")

if __name__ == "__main__":
    ejecutar_prueba_completa()