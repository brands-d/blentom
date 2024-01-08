from pathlib import Path

from .atom import Atom, Atoms
from .base import reset
from .camera import Camera
from .chargedensity import ChargeDensity
from .light import Light
from .material import Material
from .plane import Plane
from .wavefunction import Wavefunction
from .imports import *

__directory__ = Path(__file__)
__version__ = (1, 0)
__blend_version__ = (4, 0, 0)
__name__ = "blentom"
__author__ = "Dominik Brandstetter"
__email__ = "dominik.brandstetter@uni-graz.at"
__url__ = "https://github.com/brands-d/blentom/tree/main"
__license__ = "MIT"
__description__ = "Import of common electronic structure files."
__tracker__ = "https://github.com/brands-d/blentom/issues"
__category__ = "Import-Export"

bl_info = {
    "name": __name__,
    "author": __author__,
    "version": __version__,
    "blender": __blend_version__,
    "description": __description__,
    "doc_url": __url__,
    "tracker_url": __tracker__,
    "category": __category__,
}
