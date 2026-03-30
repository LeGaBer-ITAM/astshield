import ast
import builtins
from astshield.generators import generate_random_name

class Obfuscator(ast.NodeTransformer):
    """
    Transformador de Árbol de Sintaxis Abstracta (AST) para ofuscar código Python.

    Esta clase recorre los nodos de un script de Python y renombra identificadores
    (variables, argumentos y nombres de funciones) por cadenas alfanuméricas
    aleatorias, manteniendo intacta la lógica de ejecución del programa.

    Attributes
    ----------
    mapping : dict
        Un diccionario que almacena el estado de la ofuscación. Mapea los nombres
        originales de las variables (claves) a sus nuevos nombres ofuscados (valores)
        para asegurar consistencia en todo el script.
    builtins_names : set
        Un conjunto que contiene los nombres de las funciones y variables nativas
        de Python (ej. 'print', 'len', 'range') para evitar ofuscarlas y romper
        el código.
    """

    def __init__(self):
        """Inicializa el ofuscador con un mapa vacío y la lista de funciones nativas."""
        self.mapping = {}
        self.builtins_names = set(dir(builtins))

    def _get_obfuscated_name(self, original_name):
        """
        Obtiene o genera el nombre ofuscado para un identificador dado.

        Parameters
        ----------
        original_name : str
            El nombre original de la variable o función extraído del nodo AST.

        Returns
        -------
        str
            El nombre ofuscado correspondiente. Si el nombre original es una
            función nativa de Python, devuelve el nombre original sin cambios.
        """
        if original_name in self.builtins_names:
            return original_name
        
        if original_name not in self.mapping:
            self.mapping[original_name] = generate_random_name()
            
        return self.mapping[original_name]

    def visit_Name(self, node):
        """
        Visita y modifica los nodos que representan el uso de variables.

        Parameters
        ----------
        node : ast.Name
            El nodo del árbol que representa un identificador.

        Returns
        -------
        ast.Name
            El nodo modificado con el nombre ofuscado, procesado recursivamente.
        """
        node.id = self._get_obfuscated_name(node.id)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """
        Visita y modifica los nodos que representan definiciones de funciones.

        Parameters
        ----------
        node : ast.FunctionDef
            El nodo del árbol que representa la declaración de una función (def).

        Returns
        -------
        ast.FunctionDef
            El nodo de la función modificado, procesado recursivamente.
        """
        node.name = self._get_obfuscated_name(node.name)
        return self.generic_visit(node)

    def visit_arg(self, node):
        """
        Visita y modifica los nodos que representan argumentos de funciones.

        Parameters
        ----------
        node : ast.arg
            El nodo del árbol que representa un parámetro dentro de una función.

        Returns
        -------
        ast.arg
            El nodo del argumento modificado, procesado recursivamente.
        """
        node.arg = self._get_obfuscated_name(node.arg)
        return self.generic_visit(node)