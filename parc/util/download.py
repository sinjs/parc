import requests
from tqdm import tqdm


def download(url: str, fname: str, desc: str, verbose: bool):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=desc,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            if verbose:
                print(f"{Fore.LIGHTBLACK_EX}verbose: writing 1024 bytes ({bar.n}){Style.RESET_ALL}")
            bar.update(size)