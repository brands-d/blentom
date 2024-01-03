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
