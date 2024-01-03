from pathlib import Path
from blentom import *

reset()


dir_ = Path(".") / "demo"

atom = Atoms.read(dir_ / "data" / "CHGCAR")
density = ChargeDensity.read(dir_ / "CHGCAR")  # does not work yet
