from subprocess import call
from sys import executable


def install_dependencies():
    call([str(executable), "-m", "ensurepip", "--user"])
    call([str(executable), "-m", "pip", "install", "--upgrade", "pip"])
    call([str(executable), "-m", "pip", "install", "--user", "scikit-image"])
    call([str(executable), "-m", "pip", "install", "--user", "ase"])
