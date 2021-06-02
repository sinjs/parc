import argparse

from parc.version import version as arg_version
from parc.install import install as arg_install


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    install_group = subparsers.add_parser("install")
    install_group.add_argument("package", help="install the package")
    install_group.add_argument("--verbose", help="increase output verbosity", action="store_true")

    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-v", "--version", help="display version and exit", action="store_true")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        parser.exit(1)
    if args.version:
        arg_version()
    arg_install(args)


if __name__ == "__main__":
    main()
