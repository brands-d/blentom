from pathlib import Path
from blentom.atom import Atoms
from blentom.light import Light
from blentom.camera import Camera
from blentom.wavefunction import Wavefunction
from blentom.plane import Plane
from blentom.base import reset

reset()

dir_ = Path("/Users/dominik/Desktop/blentom/demo")
atom = Atoms.read(dir_ / "benzene_HOMO-6.cube")
wf = Wavefunction.read(dir_ / "benzene_HOMO-6.cube")
Light()
background = Plane()
camera = Camera((0,-5,10),(25,0,0))
camera.render(dir_ / "demo.png")