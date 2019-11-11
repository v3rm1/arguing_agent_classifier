from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
import zipfile
import io
import os
import progressbar

RAW_URL = "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip"
ZIP_NAME = "./cats_vs_dogs.zip"
EXTRACT_DIR = "./data/raw"


class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def download(url=RAW_URL, zip_name=ZIP_NAME):
    pbar = MyProgressBar()
    try:
        print(f"Downloading data from {url}")
        urlretrieve(url, filename=zip_name, reporthook=pbar)
        print(f"Data has been downloaded to {zip_name}")
    except HTTPError as e:
        print('Error code: ', e.code)
    except URLError as e:
        print('Reason: ', e.reason)
    return

def extract(zip_name=ZIP_NAME, dest_directory=EXTRACT_DIR):
    with zipfile.ZipFile(zip_name) as zip_extractor:
        file_names = zip_extractor.namelist()
        for file in file_names:
            if file.endswith('.zip'):
                print(file)
                with zipfile.ZipFile(file) as sub_extractor:
                    sub_extractor.extractall(dest_directory)
                sub_extractor.close()
    zip_extractor.close()
    return

if __name__ == "__main__":
    download()
    extract()