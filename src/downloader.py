import os
import urllib.parse

import requests
from rich.progress import (
    Progress,
    BarColumn,
    TaskProgressColumn,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeElapsedColumn,
)

from src import database
from src import extractor
from src import settings
from src import utils


def download(gid: int, chunk_size: int = 1024 * 2, override: str = None):
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
        if utils.prompt(
            f"'{file_destination}' already exists. Are you sure you want to overwrite it?",
            utils.ChoiceResponse.NO,
        ):
            utils.log("Skipping...")
            return

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        TaskProgressColumn(),
        BarColumn(),
        TimeElapsedColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
    ) as progress:
        task = progress.add_task(
            f"[red]Downloading [blue]{filename}",
            total=total_size,
        )
        with open(file_destination, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                progress.advance(task, advance=len(chunk))
                f.write(chunk)

    utils.log(f"File saved to '{file_destination}'.")

    if not settings.get_auto_extract():
        if utils.prompt(
            "Would you like to extract the files?", utils.ChoiceResponse.YES
        ):
            extractor.extract_file(file_destination)
    else:
        extractor.extract_file(file_destination)
