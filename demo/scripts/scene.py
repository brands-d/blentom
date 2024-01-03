from pathlib import Path
from blentom import *

reset()

dir_ = Path(".") / "demo"
atom = Atoms.read(dir_ / "data" / "benzene_HOMO-6.cube")
wf = Wavefunction.read(dir_ / "data" / "benzene_HOMO-6.cube")

Light()
background = Plane()
background.material = Material("Background", {"Base Color": (0, 0, 0, 1)})

camera = Camera((0, -8, 25), (50, 0, -25))
camera.focuslength = 53
camera.resolution = (1080, 608)

#camera.render(dir_ / "output" / "demo2.png")
