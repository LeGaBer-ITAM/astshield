import ast
from astshield.generators import generate_random_key, xor_encrypt_string

def probar_cifrado():
    # 1. Definir nuestro mensaje de prueba
    texto_original = "SuperSecreto_123!"
    print(f"[*] Texto Original: '{texto_original}'")

    # 2. Generar una clave dinámica
    clave = generate_random_key(length=8)
    print(f"[*] Clave Generada: '{clave}'")

    # 3. Cifrar el texto
    texto_cifrado_literal = xor_encrypt_string(texto_original, clave)
    print(f"[+] Texto Cifrado (Lo que se escribirá en el código): '{texto_cifrado_literal}'")

    # 4. SIMULACIÓN: Cómo lo leerá y descifrará el código inyectado
    # ast.literal_eval simula lo que hace Python cuando lee una cadena con \x
    texto_interpretado_por_python = ast.literal_eval(f'"{texto_cifrado_literal}"')

    # Recreamos la lógica exacta de descifrado XOR que inyectaremos en el script final
    caracteres_descifrados = []
    for i in range(len(texto_interpretado_por_python)):
        char_cifrado = ord(texto_interpretado_por_python[i])
        key_val = ord(clave[i % len(clave)])
        
        # XOR (^) nuevamente revierte el proceso matemático
        char_original = chr(char_cifrado ^ key_val) 
        caracteres_descifrados.append(char_original)
        
    texto_descifrado = "".join(caracteres_descifrados)
    print(f"[+] Texto Descifrado: '{texto_descifrado}'")

    # 5. Prueba de fuego (Assert)
    assert texto_original == texto_descifrado
    print("\n[ÉXITO] La matemática criptográfica XOR funciona a la perfección y es reversible.")

if __name__ == "__main__":
    probar_cifrado()