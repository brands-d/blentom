from pathlib import Path
from src.atom import Atoms
from src.light import Light
from src.camera import Camera
from src.wavefunction import Wavefunction
from src.plane import Plane
from src.base import reset
from src.material import Material

reset()

dir_ = Path("/Users/dominik/Desktop/blentom/demo")
atom = Atoms.read(dir_ / "POSCAR")
atom.periodic((5, 5, 2))
Light()
background = Plane()
background.material = Material("Background", {"Base Color": (0, 0, 0, 1)})
camera = Camera((0, -8, 25), (50, 0, -25))
camera.focuslength = 53
camera.resolution = (1080, 608)
camera.render(dir_ / "demo2.png")
