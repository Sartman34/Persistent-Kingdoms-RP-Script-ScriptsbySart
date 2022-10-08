from setuptools import setup, find_packages
import py2exe

setup(
    console = [
        "ana script.py",
        "açlık scripti.py",
        "autosave.py",
        "script attack viewer.py",
        "send command.py",
    ],
    windows = [
        "Server Owner Panel v1.3.3 x64.pyw"
    ],
    options = {
        "py2exe" : {
            "dist_dir": "../TCP Server",
        }
    },
    packages = find_packages(),
)
