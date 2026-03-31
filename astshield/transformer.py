import ast
import builtins
from astshield.generators import generate_random_name, generate_random_key, xor_encrypt_string

class Obfuscator(ast.NodeTransformer):
    """
    Transformador de Árbol de Sintaxis Abstracta (AST) para ofuscar código Python.
    Renombra identificadores e implementa cifrado XOR polimórfico para strings.
    """

    def __init__(self):
        self.mapping = {}
        self.builtins_names = set(dir(builtins))
        self.decrypt_func_name = generate_random_name()
        # PROTEGER NUESTRA PROPIA FUNCIÓN
        self.builtins_names.add(self.decrypt_func_name)

    def _get_obfuscated_name(self, original_name):
        """Obtiene o genera el nombre ofuscado para un identificador dado."""
        if original_name in self.builtins_names:
            return original_name
        
        if original_name not in self.mapping:
            self.mapping[original_name] = generate_random_name()
            
        return self.mapping[original_name]

    def visit_Module(self, node):
        """
        Visita el nodo raíz del script. Primero ofusca todo el código original,
        y al final inyecta la función de descifrado para evitar que el ofuscador
        se ataque a sí mismo.
        """
        # 1. PRIMERO ofuscamos el código original (dejamos que las otras funciones visit_ actúen)
        node = self.generic_visit(node)

        # 2. LUEGO construimos la función de descifrado intacta
        decrypt_code = f"""
def {self.decrypt_func_name}(c, k):
    _o, _c, _l = ord, chr, len
    return "".join(_c(_o(c[i]) ^ _o(k[i % _l(k)])) for i in range(_l(c)))
"""
        decrypt_ast = ast.parse(decrypt_code)

        # 3. Pegamos la función al principio del árbol YA ofuscado
        node.body = decrypt_ast.body + node.body

        return node

    def visit_Constant(self, node):
        """
        Visita los nodos de valores constantes. Si detecta un string, lo cifra 
        y lo reemplaza por una llamada a la función de descifrado en tiempo real.
        """
        # Verificamos si el valor de la constante es una cadena de texto
        if isinstance(node.value, str):
            texto_original = node.value
            
            # Generamos una clave única solo para esta palabra (Polimorfismo)
            clave = generate_random_key()
            texto_cifrado_hex = xor_encrypt_string(texto_original, clave)
            
            # TRUCO AST: Convertimos el string hexadecimal escapado en un nodo constante
            # evaluándolo como si Python lo leyera directamente de un archivo.
            nodo_cifrado = ast.parse(f'"{texto_cifrado_hex}"').body[0].value
            
            # Construimos la llamada a la función: descifrador(texto_cifrado, clave)
            llamada_descifrado = ast.Call(
                func=ast.Name(id=self.decrypt_func_name, ctx=ast.Load()),
                args=[
                    nodo_cifrado,
                    ast.Constant(value=clave)
                ],
                keywords=[]
            )
            
            # Copiamos las coordenadas (línea/columna) del nodo original al nuevo
            return ast.copy_location(llamada_descifrado, node)

        return self.generic_visit(node)

    def visit_Name(self, node):
        node.id = self._get_obfuscated_name(node.id)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        node.name = self._get_obfuscated_name(node.name)
        return self.generic_visit(node)

    def visit_arg(self, node):
        node.arg = self._get_obfuscated_name(node.arg)
        return self.generic_visit(node)