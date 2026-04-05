# AstShield

AstShield es un motor de ofuscación estructural y criptográfica para Python. Opera directamente sobre el Árbol de Sintaxis Abstracta y transforma el código fuente a un formato ilegible para humanos y herramientas de ingeniería inversa, garantizando al mismo tiempo la funcionalidad.

---

## ¿Qué es la Ofuscación y por qué usarla?

La ofuscación la técnica de transformar un programa en una versión equivalente que es computacionalmente compleja de analizar, modificar o revertir. El código ofuscado es código nativo que el procesador ejecuta directamente, pero cuya arquitectura lógica y semántica ha sido destruida deliberadamente.

### Casos de Uso
* **Protección de Propiedad Intelectual:** Evita que competidores copien algoritmos propietarios críticos.

* **Ciberseguridad y Bóvedas:** Dificulta la extracción de lógicas de validación de licencias, firmas de red o mecanismos de generación de claves.

* **Prevención de Manipulación:** Hace inviable que actores maliciosos modifiquen el código para saltarse restricciones o inyectar código no autorizado.

---

## Niveles de Protección

Dado que las técnicas más avanzadas introducen sobrecostos computacionales, Astshield permite configurar diferentes niveles de ofuscación bloque por bloque.

* **Nivel 0:** La función se ignora por completo. Diseñado para bloques de código que requieren rendimiento absoluto en tiempo real.
* **Nivel 1:** * *Impacto en rendimiento:* Muy Bajo.
  * *Técnicas:* Renombra todas las variables y funciones con cadenas alfanuméricas aleatorias. Cifra todos los strings en memoria mediante algoritmos XOR dinámicos.
* **Nivel 2:** * *Impacto en rendimiento:* Medio.
  * *Técnicas:* Inyecta el código real dentro de trampas lógicas utilizando alias de memoria en el Heap. Esto burla la técnica de Propagación de Constantes de los analizadores estáticos automáticos y genera "código muerto" para confundir a los desensambladores.
* **Nivel 3:** * *Impacto en rendimiento:* Alto.
  * *Técnicas:* Destruye el Grafo de Flujo de Control (CFG) original. Toma el código lineal y lo fragmenta dentro de una máquina de estados masiva gobernada por un bucle `while True`. El código salta en completo desorden físico, haciendo casi imposible trazar el flujo lógico del algoritmo.

---

## Interfaz y Funciones Principales

AstShield se integra en tu flujo de trabajo a través de dos componentes principales: la API de etiquetado y el motor compilador.

### astshield.api.protect(level)
Un **decorador fantasma** que se importa en tu código fuente. Funciona como un metadato visual para indicarle al compilador qué nivel de ofuscación aplicar a cada función. Durante el proceso de compilación, AstShield lee este nivel, aplica la transformación correspondiente y luego elimina el decorador del código resultante para no dejar rastro.

**Ejemplo de uso:**
```python
from astshield.api import protect

@protect(level=1)
def funcion_rapida():
    pass # Solo ofuscación ligera

@protect(level=3)
def algoritmo_critico():
    pass # Aplanamiento de flujo completo
```

### astshield.obfuscate_file(input_path, output_path, default_level=3)
La función principal que actúa como el motor de compilación. Lee el script original de tu disco, parsea el AST, aplica las mutaciones basándose en las etiquetas `@protect` (o en el nivel por defecto) y exporta un nuevo binario ofuscado e independiente.

**Ejemplo de uso:**
```python
from astshield import obfuscate_file

exito = obfuscate_file(
    input_path="app_secreta.py", 
    output_path="app_distribucion.py", 
    default_level=2
)
```

---

## Guía de Inicio Rápido

1. **Etiqueta tu código:** Escribe tu aplicación en Python e importa `@protect` para definir los niveles de seguridad en tus funciones sensibles.
2. **Crea el compilador:** Escribe un pequeño script de construcción (build script) que llame a `obfuscate_file()`.
3. **Compila:** Ejecuta tu script de construcción. AstShield generará tu archivo ofuscado.
4. **Distribuye:** Entrega el archivo ofuscado a tus clientes o servidores. El binario resultante es **100% autónomo** y no requiere que el paquete AstShield esté instalado en el entorno de destino.

---

**Advertencia de Rendimiento:** El Nivel 3 desactiva intencionadamente la predicción de ramas del procesador e incrementa severamente la complejidad ciclomática del archivo. Se recomienda utilizar el Nivel 3 de forma exclusiva en las funciones que manejen secretos criptográficos, licencias o propiedad intelectual crítica.