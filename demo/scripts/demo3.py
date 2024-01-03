from pathlib import Path
from src.atom import Atoms
from src.light import Light
from src.camera import Camera
from src.wavefunction import Wavefunction
from src.plane import Plane
from src.base import reset
from src.material import Material
from src.chargedensity import ChargeDensity

reset()

dir_ = Path("/Users/dominik/Desktop/blentom/demo")
atom = Atoms.read(dir_ / "CHGCAR")
density = ChargeDensity.read(dir_/"CHGCAR")
# atom.periodic((5, 5, 2))
Light()
background = Plane()
background.material = Material("Background", {"Base Color": (0, 0, 0, 1)})
camera = Camera((0, -5, 3), (25, 0, 0))
camera.focuslength = 10
# camera.render(dir_ / "demo2.png")
