import requests
from tqdm import tqdm
import zipfile
import os


def download_file(url, filename):
    response = requests.get(url, stream=True)

    # Get the total file size
    file_size = int(response.headers.get('Content-Length', 0))

    # Initialize the progress bar
    progress = tqdm(response.iter_content(1024), f'Downloading {filename}', total=file_size, unit='B', unit_scale=True,
                    unit_divisor=1024, colour="blue")

    with open(filename, 'wb') as file:
        for data in progress.iterable:
            # Write data read to the file
            file.write(data)
            # Update the progress bar manually
            progress.update(len(data))


def extract_file(filename, directory):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(directory)

    os.remove(filename)


url = 'https://github.com/official-stockfish/Stockfish/releases/download/sf_17.1/stockfish-windows-x86-64-avx2.zip'

filename = 'downloaded_file.zip'
directory = 'stockfish_download'

download_file(url, filename)
extract_file(filename, directory)
