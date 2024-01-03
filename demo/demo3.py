from pathlib import Path
from blentom.atom import Atoms
from blentom.light import Light
from blentom.camera import Camera
from blentom.wavefunction import Wavefunction
from blentom.plane import Plane
from blentom.base import reset
from blentom.material import Material
from blentom.chargedensity import ChargeDensity

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
