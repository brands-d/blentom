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
atom = Atoms.read(dir_ / "6y76.cube")
# atom.periodic((2,3,4))
# wf = Wavefunction.read(dir_ / "benzene_HOMO-6.cube")
# wf.periodic((2,3,4))
# Light()
# background = Plane()
# background = Plane()
# background.material = Material("Background",{"Base Color": (0,0,0,1)})
# camera = Camera((0,-5,10),(25,0,0))
# camera.render(dir_ / "demo.png")
