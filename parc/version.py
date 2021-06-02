import os

__version__ = {
    "type": "bleeding-edge",
    "number": "0.1.0"
}


def version():
    print(f"parc {__version__['number']} ({__version__['type']})")
    exit(0)
