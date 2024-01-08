from subprocess import call
from sys import executable
from .src import __directory__


def install_dependencies():
    call([str(executable), "-m", "ensurepip", "--user"])
    call([str(executable), "-m", "pip", "install", "--upgrade", "pip"])
    call([str(executable), "-m", "pip", "install", "--user", "-r", "requirements.txt"])
