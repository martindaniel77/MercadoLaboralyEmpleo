"""
Paquete de servicios del análisis multidimensional (Etapa 5).

Reexporta la interfaz pública de los servicios por vista y de la documentación
de operaciones OLAP para que puedan importarse desde un único punto:

    from services import get_vista1, get_vista2, get_vista3, get_vista4, get_operaciones
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
