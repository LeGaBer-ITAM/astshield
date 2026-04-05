# astshield/api.py

def protect(level=3):
    """
    Decorador API para AstShield.
    Sirve como marca estática para el compilador. En tiempo de ejecución estándar,
    devuelve la función intacta sin añadir sobrecostos.
    
    Niveles:
    0: Sin ofuscación (Ignorar función).
    1: Capa 1: Ofuscación de funciones y cadenas. No genera sobrecosto computacional.
    2: Capa 2: Predicados opacos. Genera una cantidad de sobrecosto negligible.
    3: Capa 3: Aplanamiento del Flujo de Control. Genera una cantidad de sobrecosto elevada.
    """
    def decorator(func):
        return func
    return decorator