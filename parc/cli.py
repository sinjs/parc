import multicommand
from parc import parsers


def cli():
    parser = multicommand.create_parser(parsers)
    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
        return
    parser.print_help()


if __name__ == "__main__":
    exit(cli())
