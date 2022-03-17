import os
import urllib.parse

import requests
import tqdm

from src import database
from src import extractor
from src import matching
from src import settings


def download(gid: int, chunk_size: int = 1024 * 2, override=None):
    """
    Downloads game based on gid.
    """

    plt = database.get_platform_by_gid(int(gid))

    url = plt.get_url(gid)

    # Send a get request to the download url. Set referer to the url of the download, so it gets accepted.
    # By setting stream to True, it doesn't hang the program. This way we can use progress bars.
    response = requests.get(url, headers={"referer": url}, stream=True)

    # Extract the filename from the url.
    filename = urllib.parse.unquote(response.url).split('/')[-1]

    # Get the file size and make it more readable.
    total_size = int(response.headers['Content-length'])
    formatted_size = matching.get_size_label(int(total_size))

    # Set the path depending on the override value
    if override:
        target_directory = override  # Path to directory of file
        file_destination = os.path.join(override, filename)  # Full path to file
    else:
        platform_path = settings.get_platform_path(plt)
        target_directory = platform_path  # Path to directory of file
        file_destination = os.path.join(platform_path, filename)  # Full path to file

    # If the target directory doesn't exist, create it.
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # If the file exists already, choose to overwrite it
    if os.path.exists(file_destination):
        overwrite = input(f"'{file_destination}' already exists. Are you sure you want to overwrite it? (Y/n): ")
        if overwrite.lower() != 'y':
            exit()

    # Use tqdm to make a progress bar.
    print(f"Downloading '{filename}'")
    progress_bar = tqdm.tqdm(total=total_size, colour='green', unit_scale=True, unit='B',
                             unit_divisor=1024)

    # Iterate over the data and write it to the file.
    with open(file_destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size):
            progress_bar.update(len(chunk))
            f.write(chunk)

    progress_bar.close()  # Close progress bar before the next print to prevent the progress bar messing up.

    print(f"File saved to '{file_destination}'.")

    # Decide what to do with the file.
    if extractor.ALLOW_EXTRACTION:
        if not settings.get_auto_extract():
            download_option = input(f"Would you like to extract the files? (Y/n): ")

            # Quit if CANCEL is chosen
            if download_option.lower() == "y":
                extractor.extract_file(file_destination)
        else:
            extractor.extract_file(file_destination)
