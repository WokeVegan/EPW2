# Emuparadise Workaround 2

This is a complete rewrite of my old [Emuparadise Workaround](https://github.com/WokeVegan/Emuparadise-Workaround)
script. The old project has a bad foundation and a collection of bad habits. The idea for this one is to make it more
efficient and easier to work with.

Usage
===

### Requirements

- Requires Python 3.6+
  - colorama
  - requests
  - tqdm
  - python-magic-bin
  - py7zr

### Searching

You can search for games in the database files with the following commands.

```sh
# Searches for castlevania in every platform.
python epw.py search castlevania

# Output ...
Searching: 100%|██████████████████████████████| 60/60 [00:00<00:00, 242.27it/s]

Showing 64 results for castlevania...
[92824] Castlevania (1990)(Konami) Abandonware
[70374] Castlevania (U) Commodore 64 Preservation Project
[43269] Castlevania - Circle of the Moon (E)(Eurasia) Game Boy Advance
...
```

You can narrow the results by specifying a platform.

```sh
# Only search the ps1 database.
python epw.py search castlevania --platform "Sony Playstation"

# Output ...
Showing 5 results for castlevania...
[36662] Castlevania - Chronicles [U] Sony Playstation
[36663] Castlevania - Symphony of the Night [plus Music CD] [U] Sony Playstation
[51896] Castlevania Chronicles (E) Sony Playstation
...
```

### Downloading

You can download the game by using the id provided from the search function on the far left in brackets. If you have
`python-magic-bin` installed, you can extract `.zip` files after downloading. You can also extract `.7z` files if you
`pyunpack` installed.

```sh
# Downloads the game with the id that search provided for us.

python epw.py download 46806  # This uses the default dir found in the settings.cfg
python epw.py download 46806 -d "some/other/dir"  # override the default directory for this download

Downloading '0735 - Castlevania - Portrait of Ruin (U)(XenoPhobia).7z'
100%|█████████████████████████████████████| 22.6M/22.6M [00:03<00:00, 6.10MB/s]
File saved to 'some/other/dir/0735 - Castlevania - Portrait of Ruin (U)(XenoPhobia).7z'.

# If magic is found, you'll be asked if you want to extract the file.
Would you like to extract the files? (Y/n): y
Files extracted to 'some/other/dir/0735 - Castlevania - Portrait of Ruin (U)(XenoPhobia)'.
```

### Settings

When you run the script for the first time, if `settings.cfg` isn't found, the script will automatically regenerate one.
If you want to restore the file to its default values, or create a new file, you can use the command
`python epw.py settings -r`.

To edit these settings you can type `python epw.py settings -o`. This will attempt to open `settings.cfg` in a text
editor. In the `directory` section you will see the `default` option, along with an option for every platform. All
platforms without a value will use `default`. You can leave these blank if you don't wish to orverride them.

In the `general` section, there is an option called `auto_extract`. You can set this to `true` or `false`. If this is
set to `true`, then you will no longer get prompts to confirm file extraction.
