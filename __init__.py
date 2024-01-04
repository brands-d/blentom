from subprocess import call
from sys import executable

from . import auto_load
from .src import *

bl_info = {
    "name": "blentom",
    "author": "Dominik Brandstetter",
    "description": "",
    "blender": (4, 0, 0),
    "version": (0, 1, 0),
    "category": "Import-Export",
}


def register():
    pass


def unregister():
    pass


def install_dependencies():
    # On Windows Blender needs to run in Admin Mode
    py_exec = executable
    call([str(py_exec), "-m", "ensurepip", "--user"])
    call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
    call([str(py_exec), "-m", "pip", "install", "--user", "scikit-image"])
    call([str(py_exec), "-m", "pip", "install", "--user", "ase"])


if __name__ == "__main__":
    auto_load.init()
    install_dependencies()
