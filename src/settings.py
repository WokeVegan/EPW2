import configparser
import os
import pathlib
import platform
import subprocess

from src import database
from src import utils


def get_path() -> str:
    this_file = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(this_file.parent.absolute(), "settings.cfg")


def get_default_directory() -> str:
    this_file = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(this_file.parent.absolute(), "ROMs")


def open_in_editor() -> None:
    if platform.system() == "Windows":
        subprocess.run([get_path()])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", get_path()])


def create_template(restore=False) -> None:
    if not restore:
        if os.path.exists(get_path()):
            return

    if restore:
        if utils.prompt("Restore the settings to default?") == utils.ChoiceResponse.NO:
            return

    if not os.path.exists(get_default_directory()):
        os.makedirs(get_default_directory())

    dir_template = {"default": get_default_directory()}

    for p in database.iter_platforms():
        dir_template[p.title] = ""

    config = configparser.ConfigParser()
    config["directory"] = dir_template
    config["general"] = {"auto_extract": "false"}

    with open(get_path(), "w") as f:
        config.write(f)

    if restore:
        print("Settings restored to default.")


def get_platform_path(plt: database.Platform) -> str:
    config = configparser.ConfigParser()
    config.read(get_path())
    platform_dir = config.get("directory", plt.title)

    if platform_dir:
        directory = platform_dir
    else:
        directory = config.get("directory", "default")

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def get_auto_extract() -> bool:
    config = configparser.ConfigParser()
    config.read(get_path())
    return config.getboolean("general", "auto_extract")
