from pathlib import Path
from blentom.atom import Atoms
from blentom.light import Light
from blentom.camera import Camera
from blentom.wavefunction import Wavefunction
from blentom.plane import Plane
from blentom.base import reset
from blentom.material import Material

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
