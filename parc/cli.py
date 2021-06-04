import multicommand
from parc import parsers
from parc.version import __version__


def cli():
    parser = multicommand.create_parser(parsers)
    parser.add_argument("-v", "--version", help="display version and exit", action="store_true")
    args = parser.parse_args()
    if args.version:
        print(f"parc {__version__['number']} {__version__['type']}")
        return
    if hasattr(args, "handler"):
        args.handler(args)
        return
    parser.print_help()


if __name__ == "__main__":
    exit(cli())
