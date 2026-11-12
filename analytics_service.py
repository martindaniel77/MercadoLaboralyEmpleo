"""
Capa de consultas del análisis multidimensional (Etapa 5).

Fachada de compatibilidad: la lógica se desestructuró en el paquete `services`
(uno por vista, más `common` y `operaciones`). Este módulo reexporta la misma
interfaz pública para no alterar las importaciones existentes en la aplicación.
"""

from services.vista1 import get_vista1, get_vista1_opciones_paises
from services.vista2 import get_vista2
from services.vista3 import get_vista3
from services.vista4 import get_vista4

__all__ = [
    'get_vista1',
    'get_vista1_opciones_paises',
    'get_vista2',
    'get_vista3',
    'get_vista4',
]
