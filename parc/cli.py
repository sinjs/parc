import multicommand
from parc import parsers
from parc.version import version


def cli():
    parser = multicommand.create_parser(parsers)
    parser.add_argument("-v", "--version", help="display version and exit", action="store_true")
    args = parser.parse_args()
    if args.version:
        return version()
    if hasattr(args, "handler"):
        args.handler(args)
        return
    parser.print_help()


if __name__ == "__main__":
    exit(cli())
