# Blentom

Blentom is a Blender addon to allow for simple import, scene setup and rendering of files common in the electronic structure simulation community. Currently it supports molecule-like atomic structures in all ASE supported files (e.g. `.cube`, `POSCAR`, `.xyz`, `.pdb`, etc.). Furthermore wavefunction densities can additionally be loaded from `.cube` files and charge densities from `CHGCAR` files.

![Ag-NiTCNB2](https://github.com/brands-d/blentom/blob/main/demo/output/Ag-NiTCNB2.png?raw=true)

## Installation

1. **Download the Addon**: Download the `blentom.zip` file from the [GitHub Page](https://github.com/brands-d/blentom/tree/v1.0.0b).
2. **Install in Blender**: Open Blender and navigate to `Edit > Preferences > Add-ons > Install...`, then select the `blentom.zip` file[^1].
3. **Enable the Addon**: Search for 'Blentom' in the Add-ons tab and enable it[^2].


[^1]: On Windows Blender has to be executed in administrator mode.
[^2]: The activation takes some time because external dependencies are installed.

## Usage

**Navigate to the `Scripting` page inside Blender. There you find a console or you can load `.py` scripts or create new ones.**

### Quickstart

```python
from blentom import Atoms, Camera

Atoms.read("path/to/input")
camera = Camera()
camera.render("path/to/output.png")
```

### Import

If you just want to import common files use the appropriate entry under `File > Import`.

### Demo Files
Inside the `blentom/demo/scripts` you can find a couple of demo scripts that highlight certain features.
