import requests


def download_silent(url: str, fname: str):
    resp = requests.get(url, stream=True)
    with open(fname, 'wb') as file:
        for data in resp.iter_content(chunk_size=1024):
            file.write(data)
