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
        self.inside_fstring = False
        self.current_level = 3

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
        node = self.generic_visit(node)
        decrypt_code = f"""
def {self.decrypt_func_name}(c, k):
    _o, _c, _l = ord, chr, len
    return "".join(_c(_o(c[i]) ^ _o(k[i % _l(k)])) for i in range(_l(c)))
"""
        decrypt_ast = ast.parse(decrypt_code)
        node.body = decrypt_ast.body + node.body

        return node
    
    def visit_Import(self, node):
        """
        Atrapa las declaraciones 'import X'. 
        Protege el nombre del módulo para que no sea ofuscado más adelante.
        """
        for alias in node.names:
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
        Visita constantes y cifra cadenas de texto si el nivel de protección lo permite.

        Parameters
        ----------
        node : ast.Constant
            El nodo constante a evaluar dentro del AST.

        Returns
        -------
        ast.AST
            El nodo original si el nivel es 0 o no es un string. Un nodo modificado 
            (con la llamada de descifrado o el FormattedValue) si se aplica el cifrado.
        """
        if self.current_level == 0:
            return self.generic_visit(node)

        if isinstance(node.value, str):
            texto_original = node.value
            
            clave = generate_random_key()
            texto_cifrado_hex = xor_encrypt_string(texto_original, clave)
            nodo_cifrado = ast.parse(f'"{texto_cifrado_hex}"').body[0].value
            
            llamada_descifrado = ast.Call(
                func=ast.Name(id=self.decrypt_func_name, ctx=ast.Load()),
                args=[
                    nodo_cifrado,
                    ast.Constant(value=clave)
                ],
                keywords=[]
            )
            
            if getattr(self, 'inside_fstring', False):
                nodo_formateado = ast.FormattedValue(
                    value=llamada_descifrado,
                    conversion=-1,
                    format_spec=None
                )
                return ast.copy_location(nodo_formateado, node)
            
            return ast.copy_location(llamada_descifrado, node)

        return self.generic_visit(node)

    def visit_Name(self, node):
        node.id = self._get_obfuscated_name(node.id)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """
        Procesa las definiciones de funciones aplicando ofuscación selectiva por capas.

        Busca y procesa el decorador `@protect` para determinar el nivel de seguridad.
        Elimina la marca del decorador del AST y aplica las transformaciones
        jerárquicas (renombrado, aplanamiento, predicados) en función del nivel extraído.

        Parameters
        ----------
        node : ast.FunctionDef
            El nodo que representa la definición de la función.

        Returns
        -------
        ast.FunctionDef
            El nodo de la función modificada con las capas de ofuscación pertinentes,
            o el nodo original si el nivel de protección es 0.
        """
        nivel_proteccion = 3
        decoradores_finales = []
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name) and dec.func.id == 'protect':
                for kw in dec.keywords:
                    if kw.arg == 'level' and isinstance(kw.value, ast.Constant):
                        nivel_proteccion = kw.value.value
            else:
                decoradores_finales.append(dec)
                
        node.decorator_list = decoradores_finales

        if nivel_proteccion == 0:
            return node

        if nivel_proteccion >= 1:
            node.name = self._get_obfuscated_name(node.name)

        nivel_anterior = self.current_level
        self.current_level = nivel_proteccion

        node = self.generic_visit(node)
        
        self.current_level = nivel_anterior

        docstring = []
        cuerpo_real = node.body
        
        if (len(node.body) > 0 and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str)):
            docstring = [node.body[0]]
            cuerpo_real = node.body[1:]
            
        if not cuerpo_real:
            return node

        if nivel_proteccion >= 3:
            cuerpo_real = self._flatten_control_flow(cuerpo_real)

        if nivel_proteccion >= 2:
            setup_nodes, equation_node = generate_opaque_predicate()
            nombre_falso = generate_random_name()
            string_falso = generate_random_name(length=30)
            nodo_codigo_muerto = ast.Assign(
                targets=[ast.Name(id=nombre_falso, ctx=ast.Store())],
                value=ast.Constant(value=string_falso)
            )
            
            bloque_if = ast.If(test=equation_node, body=cuerpo_real, orelse=[nodo_codigo_muerto])
            node.body = docstring + setup_nodes + [bloque_if]
        else:
            node.body = docstring + cuerpo_real

        return node

    def visit_arg(self, node):
        node.arg = self._get_obfuscated_name(node.arg)
        return self.generic_visit(node)
    
    def _flatten_control_flow(self, body_nodes):
        """
        Aplica Aplanamiento de Flujo de Control (Capa 3) a una secuencia de nodos.

        Transforma una lista lineal de instrucciones en una máquina de estados 
        gobernada por un bucle `while` infinito. El orden físico de los bloques 
        se aleatoriza, pero el orden lógico de ejecución se mantiene mediante 
        transiciones de estado, destruyendo el Grafo de Flujo de Control (CFG) original.

        Parameters
        ----------
        body_nodes : list of ast.stmt
            Lista de nodos AST que representan el cuerpo lineal de una función o bloque.

        Returns
        -------
        list of ast.stmt
            Una nueva lista de nodos AST que contiene la asignación del estado inicial 
            seguida del bucle `while` infinito que implementa la máquina de estados. 
            Si la lista de entrada tiene 1 o 0 nodos, se devuelve sin modificaciones.
        """
        import random
        
        if len(body_nodes) <= 1:
            return body_nodes

        var_estado = generate_random_name()
        estados = random.sample(range(10000, 99999), len(body_nodes) + 1)
        estado_salida = estados[-1]

        transiciones = []
        for i, nodo in enumerate(body_nodes):
            estado_actual = estados[i]
            estado_siguiente = estados[i + 1]
            transiciones.append((estado_actual, [nodo], estado_siguiente))

        transiciones.append((estado_salida, [ast.Break()], None))

        random.shuffle(transiciones)
        cadena_if = []
        
        for estado_val, sentencias, sig_estado in reversed(transiciones):
            cuerpo_bloque = sentencias.copy()

            if sig_estado is not None:
                actualizacion_estado = ast.Assign(
                    targets=[ast.Name(id=var_estado, ctx=ast.Store())],
                    value=ast.Constant(value=sig_estado)
                )
                cuerpo_bloque.append(actualizacion_estado)

            condicion = ast.Compare(
                left=ast.Name(id=var_estado, ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=estado_val)]
            )

            nuevo_if = ast.If(test=condicion, body=cuerpo_bloque, orelse=cadena_if)
            cadena_if = [nuevo_if]

        bucle_infinito = ast.While(
            test=ast.Constant(value=True),
            body=cadena_if,
            orelse=[]
        )

        asignacion_inicial = ast.Assign(
            targets=[ast.Name(id=var_estado, ctx=ast.Store())],
            value=ast.Constant(value=estados[0])
        )

        return [asignacion_inicial, bucle_infinito]