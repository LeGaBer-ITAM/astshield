import unittest
import ast
import io
import contextlib
from astshield.transformer import Obfuscator
from astshield.formatter import generate_code_from_ast

class TestProtectionLevels(unittest.TestCase):
    """
    Suite de pruebas unitarias para validar los niveles de protección de AstShield.

    Esta clase contiene pruebas que verifican la aplicación correcta de las capas
    de ofuscación 1, 2 y 3, así como la integridad del resultado funcional
    comparando la salida del código original frente al ofuscado.
    """

    def setUp(self):
        """
        Configura el entorno de prueba antes de cada método.
        """
        self.sample_code = """
def calcular_area(radio):
    import math
    pi_local = math.pi
    resultado = pi_local * (radio ** 2)
    print(f"El area es: {resultado}")
    return resultado

calcular_area(5)
"""
        self.ofuscador = Obfuscator()

    def _obfuscate(self, code, level):
        """
        Helper para ofuscar un string de código a un nivel específico.

        Parameters
        ----------
        code : str
            Código fuente original.
        level : int
            Nivel de protección deseado.

        Returns
        -------
        str
            Código resultante tras la transformación.
        """
        tree = ast.parse(code)
        self.ofuscador.current_level = level
        transformed_tree = self.ofuscador.visit(tree)
        return generate_code_from_ast(transformed_tree)

    def _get_output(self, code):
        """
        Captura la salida de la terminal de un fragmento de código ejecutado.

        Parameters
        ----------
        code : str
            Código a ejecutar mediante exec().

        Returns
        -------
        str
            Texto capturado de la salida estándar.
        """
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                exec(code, {"__name__": "__main__"})
            except Exception as e:
                return f"ERROR: {e}"
        return f.getvalue()

    def test_level_1_integrity(self):
        """
        Verifica que el Nivel 1 oculte strings y cambie nombres.
        """
        ofuscado = self._obfuscate(self.sample_code, level=1)
        
        self.assertNotIn("calcular_area", ofuscado)
        self.assertNotIn("pi_local", ofuscado)
        self.assertNotIn("El area es:", ofuscado)
        self.assertEqual(self._get_output(self.sample_code), self._get_output(ofuscado))

    def test_level_2_integrity(self):
        """
        Verifica que el Nivel 2 incluya la estructura de predicados opacos.
        """
        ofuscado = self._obfuscate(self.sample_code, level=2)
        tree = ast.parse(ofuscado)
        
        has_if = any(isinstance(node, ast.If) for node in ast.walk(tree))
        self.assertTrue(has_if, "El nivel 2 debería contener al menos un nodo If de control")
        self.assertEqual(self._get_output(self.sample_code), self._get_output(ofuscado))

    def test_level_3_integrity(self):
        """
        Verifica que el Nivel 3 aplique el aplanamiento de flujo (while loops).
        """
        ofuscado = self._obfuscate(self.sample_code, level=3)
        tree = ast.parse(ofuscado)
        
        has_while = any(isinstance(node, ast.While) for node in ast.walk(tree))
        self.assertTrue(has_while, "El nivel 3 debería contener un bucle While infinito")
        self.assertEqual(self._get_output(self.sample_code), self._get_output(ofuscado))

if __name__ == "__main__":
    unittest.main()