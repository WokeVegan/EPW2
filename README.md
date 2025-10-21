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
    - rich
    - patool
    - py7zr
    - fuzzywuzzy

### Searching

You can search for games in the database files with the following commands.

```sh
# Searches for castlevania in every platform.
> python epw.py search golden sun
[43409] Golden Sun (U)(Mode7) Game Boy Advance
[43542] Golden Sun (F)(Moleia) Game Boy Advance
[43605] Golden Sun (G)(Koma) Game Boy Advance
...
```

You can narrow the results by specifying a platform.

```sh
> python epw.py search golden sun --platform gba
[43409] Golden Sun (U)(Mode7) Game Boy Advance
[43542] Golden Sun (F)(Moleia) Game Boy Advance
[43605] Golden Sun (G)(Koma) Game Boy Advance
...
```

Search results are found by using fuzzy partial ratio. If results aren't showing, you can try lowering the ratio.
The default ratio is 85. Lowering this value will result in much more matches being found.

```sh
> python epw.py search golden sun --ratio 75
```

### Downloading

You can download the game by using the id provided from the search function on the far left in brackets. If you have
`patool` and `py7zr` installed, you will be prompted to extract files after downloading. You can auto extract files by
setting `auto_extract` to `true` in the `settings.cfg` file.

```sh
# Downloads the game with the id that search provided for us.
> python epw.py download 44178
Starting download 1 of 1
Downloading 0940 - Golden Sun 2 - The Lost Age (U)(Megaroms).zip 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:00:27 13.1/13.1 MB 302.1 kB/s
File saved to 'C:\some\directory\0940 - Golden Sun 2 - The Lost Age (U)(Megaroms).zip'.
Attempting to extract 0940 - Golden Sun 2 - The Lost Age (U)(Megaroms)...
Files extracted to 'C:\some\directory'.
```

You can download multiple files at once by providing multiple ids...

```sh
> python epw.py download 44178 44179
Starting download 1 of 2
...
```

### Settings

When you run the script for the first time, if `settings.cfg` isn't found, the script will automatically create one.
If you want to restore the file to its default values, or create a new file, you can use the command
`python epw.py settings -r`.

To edit these settings you can type `python epw.py settings -o`. This will attempt to open `settings.cfg` in a text
editor. In the `directory` section you will see the `default` option, along with an option for every platform. All
platforms without a value will use `default`. You can leave these blank if you don't wish to orverride them.

In the `general` section, there is an option called `auto_extract`. You can set this to `true` or `false`. If this is
set to `true`, then you will no longer get prompts to confirm file extraction.

If your shell doesn't support colors. You can disable them by setting `color_enabled` to `false` in `settings.cfg`.
