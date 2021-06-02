from colorama import Fore, Back, Style, Cursor
from parc.version import __version__


def install(args):
    if args.package:
        if args.verbose:
            print(f"{Style.BRIGHT}parc v{__version__['number']}")
        print(f"{Style.RESET_ALL}{Fore.LIGHTRED_EX}TODO!")
        # TODO: Make the installation code
        reset_color()


def reset_color():
    return print(Style.RESET_ALL, end="\r")
