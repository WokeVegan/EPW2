import configparser
import os
import pathlib
import platform

import colorama

from src import database


def get_path() -> str:
    """
    Returns the path to the config file.
    """

    this_file = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(this_file.parent.absolute(), 'settings.cfg')


def get_default_directory() -> str:
    """
    Returns the path to the default download directory.
    This is set to the ROMs folder located in the directory of epw.py
    """

    this_file = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(this_file.parent.absolute(), 'ROMs')


def open_in_editor():
    """
    Attempts to call the config file. On Windows, this will open the file in the default editor.
    """

    if platform.system() == 'Windows':
        os.system(get_path())
    else:
        print(colorama.Fore.RED, end="")
        print(f"This feature is only supported on Windows. Try manually opening '{get_path()}'")
        print(colorama.Fore.RESET)


def create_template(restore=False):
    """
    Generates a config file if one doesn't already exist.
    If restore is set to True then this will recreate the file.
    """

    # If restore is False and the config file already exists, return.
    if not restore:
        if os.path.exists(get_path()):
            return

    if restore:
        answer = input("Restore the settings to default? (Y/n):")
        if answer.lower() != 'y':
            return

    if not os.path.exists(get_default_directory()):
        os.makedirs(get_default_directory())

    dir_template = {'default': get_default_directory()}

    for p in database.iter_platforms():
        dir_template[p.title] = ""

    config = configparser.ConfigParser()
    config['directory'] = dir_template
    config['general'] = {'auto_extract': "false"}
    with open(get_path(), 'w') as f:
        config.write(f)

    if restore:
        print('Settings restored to default.')


def get_platform_path(plt: database.Platform):
    """
    Returns path to download folder for specific ROM type.
    If no directory was set then returns `get_default_directory()`
    """
    config = configparser.ConfigParser()
    config.read(get_path())
    platform_dir = config.get('directory', plt.title)

    if platform_dir:
        directory = platform_dir
    else:
        directory = config.get('directory', 'default')

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def get_auto_extract():
    config = configparser.ConfigParser()
    config.read(get_path())
    return config.getboolean('general', 'auto_extract')
