import ast
import builtins
from astshield.generators import *

class Obfuscator(ast.NodeTransformer):
    """
    Transformador de Árbol de Sintaxis Abstracta (AST) para ofuscar código Python.
    Renombra identificadores e implementa cifrado XOR polimórfico para strings.
    """

    def __init__(self):
        self.mapping = {}
        self.builtins_names = set(dir(builtins))
        self.decrypt_func_name = generate_random_name()
        self.builtins_names.add(self.decrypt_func_name)
        # NUEVO: Bandera de contexto
        self.inside_fstring = False

    def visit_JoinedStr(self, node):
        """
        Atrapa los f-strings. Enciende una bandera temporal para evitar
        que visit_Constant destruya la estructura interna del f-string.
        """
        self.inside_fstring = True
        self.generic_visit(node)
        self.inside_fstring = False
        return node

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
    def visit_Import(self, node):
        """
        Atrapa las declaraciones 'import X'. 
        Protege el nombre del módulo para que no sea ofuscado más adelante.
        """
        for alias in node.names:
            # Si el usuario hace 'import numpy as np', protegemos 'np'
            nombre_a_proteger = alias.asname if alias.asname else alias.name
            self.builtins_names.add(nombre_a_proteger)
            
        return self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """
        Atrapa las declaraciones 'from X import Y'. 
        Protege las funciones o módulos importados.
        """
        for alias in node.names:
            nombre_a_proteger = alias.asname if alias.asname else alias.name
            self.builtins_names.add(nombre_a_proteger)
            
        return self.generic_visit(node)
    def visit_Constant(self, node):
        """
        Visita los nodos de valores constantes. Cifra los strings regulares.
        Si detecta que está dentro de un f-string, envuelve la llamada de 
        descifrado en un FormattedValue (Caballo de Troya) para respetar 
        las reglas estructurales de ast.JoinedStr.
        """
        if isinstance(node.value, str):
            texto_original = node.value
            
            # 1. Cifrado regular
            clave = generate_random_key()
            texto_cifrado_hex = xor_encrypt_string(texto_original, clave)
            nodo_cifrado = ast.parse(f'"{texto_cifrado_hex}"').body[0].value
            
            # 2. Construimos la llamada a la función de descifrado
            llamada_descifrado = ast.Call(
                func=ast.Name(id=self.decrypt_func_name, ctx=ast.Load()),
                args=[
                    nodo_cifrado,
                    ast.Constant(value=clave)
                ],
                keywords=[]
            )
            
            # 3. EL CABALLO DE TROYA: ¿Estamos dentro de un f-string?
            if getattr(self, 'inside_fstring', False):
                # Envolvemos la llamada de descifrado en un nodo FormattedValue ({})
                nodo_formateado = ast.FormattedValue(
                    value=llamada_descifrado,
                    conversion=-1,    # -1 significa sin conversión especial (como !s o !r)
                    format_spec=None  # Sin formato especial (como :.2f)
                )
                return ast.copy_location(nodo_formateado, node)
            
            # Si es un string normal, devolvemos la llamada directamente
            return ast.copy_location(llamada_descifrado, node)

        # Si no es un string (ej. un número), lo dejamos intacto
        return self.generic_visit(node)

    def visit_Name(self, node):
        node.id = self._get_obfuscated_name(node.id)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """
        Visita las definiciones de funciones. Cambia el nombre de la función,
        ofusca su contenido interno y luego envuelve todo su cuerpo lógico 
        dentro de un predicado opaco con código muerto inyectado.
        """
        # 1. Cambiamos el nombre de la función (Nuestra Capa 0 original)
        node.name = self._get_obfuscated_name(node.name)
        
        # 2. ATENCIÓN: Procesamos el interior de la función PRIMERO
        # Esto asegura que las variables y strings originales se ofusquen 
        # antes de que modifiquemos la estructura de la función.
        node = self.generic_visit(node)
        
        # 3. Protección del Docstring (Comentarios de documentación)
        # Si la función empieza con un texto explicativo, debemos separarlo.
        # Si lo metemos dentro del 'if', Python dejará de reconocerlo como docstring.
        docstring = []
        cuerpo_real = node.body
        
        if (len(node.body) > 0 and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and 
            isinstance(node.body[0].value.value, str)):
            
            docstring = [node.body[0]]
            cuerpo_real = node.body[1:]
            
        # Si la función estaba vacía (solo tenía docstring o un 'pass'), la ignoramos
        if not cuerpo_real:
            return node

        # 4. Invocamos nuestra fábrica de matemáticas
        setup_node, equation_node = generate_opaque_predicate()
        
        # 5. Fabricamos el "Código Muerto" (La trampa para el analista)
        # Inyectaremos una variable falsa con un texto basura larguísimo
        nombre_falso = generate_random_name()
        string_falso = generate_random_name(length=30)
        nodo_codigo_muerto = ast.Assign(
            targets=[ast.Name(id=nombre_falso, ctx=ast.Store())],
            value=ast.Constant(value=string_falso)
        )
        
        # 6. Construimos el laberinto estructural: El bloque 'If'
        bloque_if = ast.If(
            test=equation_node,           # La condición que siempre será Verdadera
            body=cuerpo_real,             # El código real del usuario va aquí
            orelse=[nodo_codigo_muerto]   # La trampa basura va aquí
        )
        
        # 7. Reensamblamos el cuerpo de la función
        # Orden: Docstring -> Variable Matemática -> Bloque If gigante
        node.body = docstring + setup_node + [bloque_if]
        
        return node

    def visit_arg(self, node):
        node.arg = self._get_obfuscated_name(node.arg)
        return self.generic_visit(node)