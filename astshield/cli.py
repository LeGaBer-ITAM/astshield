import argparse
import ast
import sys
import os
from astshield.transformer import Obfuscator
from astshield.formatter import generate_code_from_ast, save_code_to_file

def build_parser():
    """
    Construye y configura el analizador de argumentos de la línea de comandos.

    Returns
    -------
    argparse.ArgumentParser
        El objeto configurado listo para procesar los comandos del usuario.
    """
    parser = argparse.ArgumentParser(
        description="AstShield: Un ofuscador de código Python basado en AST."
    )
    
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Ruta del archivo Python original que deseas ofuscar."
    )
    
    parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="Ruta donde se guardará el archivo Python ofuscado."
    )
    
    return parser

def main():
    """
    Punto de entrada principal de la aplicación CLI.

    Coordina el flujo de ejecución: lee el archivo de entrada, lo convierte
    en un árbol AST, aplica la transformación de ofuscación, formatea el 
    árbol de regreso a texto y lo guarda en el disco duro.

    Returns
    -------
    None
    """
    parser = build_parser()
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: El archivo de entrada '{args.input}' no existe.")
        sys.exit(1)

    print(f"[*] Leyendo '{args.input}'...")
    with open(args.input, "r", encoding="utf-8") as file:
        source_code = file.read()

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        print(f"Error de sintaxis en el archivo original: {e}")
        sys.exit(1)

    print("[*] Ofuscando código (Manipulando AST)...")
    obfuscator = Obfuscator()
    obfuscated_tree = obfuscator.visit(tree)

    print("[*] Generando código fuente final...")
    obfuscated_code = generate_code_from_ast(obfuscated_tree)

    save_code_to_file(obfuscated_code, args.output)
    print(f"[+] ¡Éxito! Archivo ofuscado guardado en '{args.output}'")

if __name__ == "__main__":
    main()