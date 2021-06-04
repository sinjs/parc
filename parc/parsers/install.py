from colorama import Fore, Style
from parc.util.download_silent import download_silent
from parc.version import __version__
from parc.util.timer import Timer
from parc.util.reset_color import reset_color
from parc.util.download import download
from parc.util.extract_all import extract_all
from parc.util.copytree import copytree
import argparse
import requests
import re
import secrets
import os


def handler(args):
    t = Timer()
    t.start()
    if args.verbose:
        print(f"{Style.BRIGHT}parc v{__version__['number']}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}info{Style.RESET_ALL}: fetching package information")
    package_info = requests.get(f"https://parc.sinjs.cf/packages/{args.package}/package.json")
    if package_info.status_code == 404:
        print(f"{Fore.RED}error{Style.RESET_ALL}: failed to download package {args.package}")
        print(f"{Fore.RED}error{Style.RESET_ALL}: The server returned {package_info.status_code} "
              f"{package_info.reason}{Style.RESET_ALL}")
        if args.verbose:
            print(f"{Fore.LIGHTBLACK_EX}verbose: dumping server response")
            print(f"{Fore.LIGHTBLACK_EX}verbose: HTTP/1.1 {package_info.status_code} {package_info.reason}")
            for header in package_info.headers:
                print(f"{Fore.LIGHTBLACK_EX}verbose: {header}: {package_info.headers[header]}")
            print("verbose:")
            for line in package_info.text.splitlines():
                print(f"{Fore.LIGHTBLACK_EX}verbose: {line}")
        print(f"{Fore.BLUE}info{Style.RESET_ALL}: requested uri is {package_info.request.url}")
    if package_info.status_code == 200:
        if args.verbose:
            print(f"{Fore.LIGHTBLACK_EX}verbose: dumping server response")
            print(f"{Fore.LIGHTBLACK_EX}verbose: {package_info.json()}")
        print(f"{Fore.LIGHTBLUE_EX}question{Style.RESET_ALL}: do you want to install "
              f"{package_info.json()['name']}, version {package_info.json()['version']}? [Y/n]",
              end=" ")
        install_package_prompt_result = input()
        matches_the_thing = re.search("^(y)|(Y)$", install_package_prompt_result)
        if len(install_package_prompt_result) == 0 or matches_the_thing:
            print(f"{Fore.BLUE}info{Style.RESET_ALL}: downloading tarball")
        else:
            print(f"{Fore.YELLOW}warn{Style.RESET_ALL}: exiting with code 1")
            exit(1)
        downloaded_path = f"/tmp/{args.package}-{package_info.json()['version']}-{secrets.token_hex(8)}.tar.gz"
        extracted_path = f"/tmp/{args.package}-{package_info.json()['version']}-{secrets.token_hex(8)}"
        script_path = f"/tmp/{args.package}-{package_info.json()['version']}-postscript--" \
                      f"{secrets.token_urlsafe(14)}.sh"
        if args.verbose:
            print(f"{Fore.LIGHTBLACK_EX}verbose: downloading file to {downloaded_path} from"
                  f"https://parc.sinjs.cf/packages/{args.package}/{args.package}-{package_info.json()['version']}"
                  f".tar.gz{Style.RESET_ALL}")
        try:
            download(f"https://parc.sinjs.cf/packages/{args.package}/"
                     f"{args.package}-{package_info.json()['version']}.tar.gz",
                     downloaded_path, args.package, args.verbose)
            print(f"{Fore.BLUE}info{Style.RESET_ALL}: extracting tarball")
            extract_all([downloaded_path], extracted_path)
        except KeyboardInterrupt:
            raise Exception(f"Traceback printed, now exiting.\n"
                            f"{Fore.RED}error{Style.RESET_ALL}: failed to download package {args.package}\n"
                            f"{Fore.RED}error{Style.RESET_ALL}: CTRL+C pressed (KeyboardInterrupt)\n"
                            f"{Fore.YELLOW}important{Style.RESET_ALL}: THIS IS NOT A BUG, DO NOT OPEN AN ISSUE")
        if os.path.isdir(f"{extracted_path}/bin"):
            copytree(f"{extracted_path}/bin", "/usr/bin")
        if os.path.isdir(f"{extracted_path}/local"):
            copytree(f"{extracted_path}/local", "/usr/local")
        if os.path.isdir(f"{extracted_path}/include"):
            copytree(f"{extracted_path}/include", "/usr/include")
        if os.path.isdir(f"{extracted_path}/lib"):
            copytree(f"{extracted_path}/lib", "/usr/lib")
        if os.path.isdir(f"{extracted_path}/man"):
            copytree(f"{extracted_path}/man", "/usr/share/man")
        print(f"{Fore.BLUE}info{Style.RESET_ALL}: running post-install script")
        try:
            download_silent(f"https://parc.sinjs.cf/packages/{args.package}/setup.sh",
                            script_path)
            os.chmod(script_path, 0o755)
            os.system(script_path)
        except KeyboardInterrupt:
            raise Exception(f"Traceback printed, now exiting.\n"
                            f"{Fore.RED}error{Style.RESET_ALL}: failed to download package {args.package}\n"
                            f"{Fore.RED}error{Style.RESET_ALL}: CTRL+C pressed (KeyboardInterrupt)\n"
                            f"{Fore.YELLOW}important{Style.RESET_ALL}: THIS IS NOT A BUG, DO NOT OPEN AN ISSUE")
        print(f"{Fore.GREEN}success{Style.RESET_ALL}: installed {args.package}, took {t.stop(False):0.3f}s")

    reset_color()


parser = argparse.ArgumentParser(
    description="install a package from the repository",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument("package", help="the package to install")
parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
parser.set_defaults(handler=handler)
