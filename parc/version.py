__version__ = {
    "type": "alpha",
    "number": "0.2.1"
}


def version():
    print(f"parc {__version__['number']} ({__version__['type']})")
    exit(0)
