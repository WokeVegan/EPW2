import os
import urllib.parse

import requests
import tqdm

from src import database
from src import extractor
from src import settings


def download(gid: int, chunk_size: int = 1024 * 2, override=None):
    """
    Downloads game based on gid.
    """

    plt = database.get_platform_by_gid(int(gid))
    url = plt.get_url(gid)
    response = requests.get(url, headers={"referer": url}, stream=True)
    filename = urllib.parse.unquote(response.url).split("/")[-1]
    total_size = int(response.headers["Content-length"])

    if override:
        target_directory = override
        file_destination = os.path.join(override, filename)
    else:
        platform_path = settings.get_platform_path(plt)
        target_directory = platform_path
        file_destination = os.path.join(platform_path, filename)

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    if os.path.exists(file_destination):
        overwrite = input(
            f"'{file_destination}' already exists. Are you sure you want to overwrite it? (Y/n): "
        )
        if overwrite.lower() != "y":
            exit()

    print(f"Downloading '{filename}'")
    progress_bar = tqdm.tqdm(
        total=total_size, colour="green", unit_scale=True, unit="B", unit_divisor=1024
    )

    with open(file_destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            progress_bar.update(len(chunk))
            f.write(chunk)

    progress_bar.close()

    print(f"File saved to '{file_destination}'.")

    if extractor.ALLOW_EXTRACTION:
        if not settings.get_auto_extract():
            download_option = input(f"Would you like to extract the files? (Y/n): ")

            if download_option.lower() == "y":
                extractor.extract_file(file_destination)
        else:
            extractor.extract_file(file_destination)
