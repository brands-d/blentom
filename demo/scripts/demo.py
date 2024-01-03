from pathlib import Path
from blentom import Atoms, Light, Camera, Wavefunction, Plane, reset, Material

reset()

dir_ = Path(".") / "demo"
atom = Atoms.read(dir_ / "data" / "benzene_HOMO-6.cube")
# atom.periodic((2,3,4))
wf = Wavefunction.read(dir_ / "data" / "benzene_HOMO-6.cube")
# wf.periodic((2,3,4))
Light()
background = Plane()
background = Plane()
background.material = Material("Background", {"Base Color": (0, 0, 0, 1)})
camera = Camera((0, -5, 10), (25, 0, 0))
# camera.render(dir_ / "demo.png")
