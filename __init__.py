from subprocess import call
from sys import executable

import bpy

from . import auto_load

bl_info = {
    "name": "Blentom",
    "author": "Dominik Brandstetter",
    "description": "",
    "blender": (4, 0, 0),
    "version": (0, 0, 1),
    "category": "Import-Export",
}


def register():
    auto_load.register()


def unregister():
    auto_load.unregister()


def install_dependencies():
    # On Windows Blender needs to run in Admin Mode
    py_exec = executable
    # call([str(py_exec), "-m", "ensurepip", "--user"])
    # call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
    # call([str(py_exec), "-m", "pip", "install", "--user", "scikit-image"])
    # call([str(py_exec), "-m", "pip", "install", "--user", "ase"])


auto_load.init()
install_dependencies()
