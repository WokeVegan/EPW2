from __future__ import annotations

import enum
import json
import os
import pathlib
import urllib
from typing import Generator

DATABASE_PATH: str = os.path.join(
    pathlib.Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute(),
    "database",
)


def iter_platforms() -> Generator[Platform]:
    for item in PlatformID:
        yield PLATFORM_OBJECTS[item]


def get_platform_by_gid(gid: int) -> Platform | None:
    for plt in iter_platforms():
        plt.load()
        if str(gid) in plt:
            return plt
    return None


def get_all() -> Generator[str]:
    for platform in PLATFORM_OBJECTS.values():
        yield platform.title


class Platform:
    def __init__(self, title: str, filename: str, *aliases: str):
        self.title = title  # only for display
        self.filename = filename
        self.table = {}
        self.loaded = False
        self.aliases = aliases

    def load(self) -> None:
        if not self.loaded:
            self.table = json.load(open(os.path.join(DATABASE_PATH, self.filename)))
            self.loaded = True

    def get_title(self, gid: str) -> str:
        return self.table.get(gid)

    def get_aliases(self) -> tuple[str, ...]:
        return self.aliases

    def get_url(self, gid) -> str:
        return f"https://www.emuparadise.me/roms/get-download.php?gid={gid}&test=true"

    def items(self) -> (int, str):
        for key, value in self.table.items():
            yield key, value

    def __contains__(self, item) -> bool:
        return item in self.table.keys()


class Dreamcast(Platform):

    def get_url(self, gid):
        title = self.get_title(str(gid))
        print(title)
        label = urllib.parse.quote(title)
        return f"http://162.210.194.49/happyUUKAm8913lJJnckLiePutyNak/Dreamcast/{label}.zip"


class PlatformID(enum.Enum):
    ABANDONWARE = 0
    ACORN_ARCHIMEDES = 1
    ACORN_BBC_MICRO = 2
    ACORN_ELECTRON = 3
    AMIGA_CD = 4
    AMIGA_CD32 = 5
    AMSTRAD_CPC = 6
    APPLE_II = 7
    ATARI_2600 = 8
    ATARI_5200 = 9
    ATARI_7800 = 10
    ATARI_8BIT_FAMILY = 11
    ATARI_JAGUAR = 12
    ATARI_LYNX = 13
    BANDAI_PLAYDIA = 14
    BANDAI_WONDERSWAN_COLOR = 15
    BANDAI_WONDERSWAN = 16
    CAPCOM_PLAY_SYSTEM_1 = 17
    CAPCOM_PLAY_SYSTEM_2 = 18
    CAPCOM_PLAY_SYSTEM_3 = 19
    COMMODORE_64_TAPES = 20
    COMMODORE_64_PRESERVATION_PROJECT = 21
    COMPLETE_ROM_SETS = 22
    DREAMCAST = 23
    GAME_BOY_ADVANCE = 24
    GAME_BOY_COLOR = 25
    GAME_BOY = 26
    GAMECUBE = 27
    MAME = 28
    NEO_GEO_POCKET_NEO_GEO_POCKET_COLOR_NGPX = 29
    NEO_GEO = 30
    NINTENDO_64 = 31
    NINTENDO_DS = 32
    NINTENDO_ENTERTAINMENT_SYSTEM = 33
    NINTENDO_FAMICOM_DISK_SYSTEM = 34
    NOKIA_NGAGE = 35
    PANASONIC_3DO_3DO_INTERACTIVE_MULTIPLAYER = 36
    PC_ENGINE_TURBOGRAFX16 = 37
    PC_ENGINE_CD_TURBO_DUO_TURBOGRAFX_CD = 38
    PCFX = 39
    PHILIPS_CDI = 40
    PSX_ON_PSP = 41
    SCUMMVM = 42
    SEGA_32X = 43
    SEGA_CD = 44
    SEGA_GAME_GEAR = 45
    SEGA_GENESIS_SEGA_MEGADRIVE = 46
    SEGA_MASTER_SYSTEM = 47
    SEGA_NAOMI = 48
    SEGA_SATURN = 49
    SHARP_X68000 = 50
    SONY_PLAYSTATION_DEMOS = 51
    SONY_PLAYSTATION_2 = 52
    SONY_PLAYSTATION = 53
    SONY_POCKETSTATION = 54
    SONY_PSP = 55
    SUPER_NINTENDO_ENTERTAINMENT_SYSTEM = 56
    VIRTUAL_BOY = 57
    ZX_SPECTRUM_TAPES = 58
    ZX_SPECTRUM_Z80 = 59


PLATFORM_OBJECTS: [PlatformID, Platform] = {
    PlatformID.ABANDONWARE: Platform("Abandonware", "abandonware.json"),
    PlatformID.ACORN_ARCHIMEDES: Platform("Acorn Archimedes", "acorn_archimedes.json"),
    PlatformID.ACORN_BBC_MICRO: Platform("Acorn Bbc Micro", "acorn_bbc_micro.json"),
    PlatformID.ACORN_ELECTRON: Platform("Acorn Electron", "acorn_electron.json"),
    PlatformID.AMIGA_CD: Platform("Amiga Cd", "amiga_cd.json"),
    PlatformID.AMIGA_CD32: Platform("Amiga Cd32", "amiga_cd32.json"),
    PlatformID.AMSTRAD_CPC: Platform("Amstrad Cpc", "amstrad_cpc.json"),
    PlatformID.APPLE_II: Platform("Apple Ii", "apple_ii.json"),
    PlatformID.ATARI_2600: Platform("Atari 2600", "atari_2600.json"),
    PlatformID.ATARI_5200: Platform("Atari 5200", "atari_5200.json"),
    PlatformID.ATARI_7800: Platform("Atari 7800", "atari_7800.json"),
    PlatformID.ATARI_8BIT_FAMILY: Platform(
        "Atari 8Bit Family", "atari_8bit_family.json"
    ),
    PlatformID.ATARI_JAGUAR: Platform("Atari Jaguar", "atari_jaguar.json"),
    PlatformID.ATARI_LYNX: Platform("Atari Lynx", "atari_lynx.json"),
    PlatformID.BANDAI_PLAYDIA: Platform("Bandai Playdia", "bandai_playdia.json"),
    PlatformID.BANDAI_WONDERSWAN: Platform(
        "Bandai Wonderswan", "bandai_wonderswan.json"
    ),
    PlatformID.BANDAI_WONDERSWAN_COLOR: Platform(
        "Bandai Wonderswan Color", "bandai_wonderswan_color.json"
    ),
    PlatformID.CAPCOM_PLAY_SYSTEM_1: Platform(
        "Capcom Play System 1", "capcom_play_system_1.json"
    ),
    PlatformID.CAPCOM_PLAY_SYSTEM_2: Platform(
        "Capcom Play System 2", "capcom_play_system_2.json"
    ),
    PlatformID.CAPCOM_PLAY_SYSTEM_3: Platform(
        "Capcom Play System 3", "capcom_play_system_3.json"
    ),
    PlatformID.COMMODORE_64_PRESERVATION_PROJECT: Platform(
        "Commodore 64 Preservation Project", "commodore_64_preservation_project.json"
    ),
    PlatformID.COMMODORE_64_TAPES: Platform(
        "Commodore 64 Tapes", "commodore_64_tapes.json"
    ),
    PlatformID.COMPLETE_ROM_SETS: Platform(
        "Complete Rom Sets", "complete_rom_sets.json"
    ),
    PlatformID.DREAMCAST: Dreamcast("Dreamcast", "dreamcast.json", "dc"),
    PlatformID.GAMECUBE: Platform("Gamecube", "gamecube.json", "gc"),
    PlatformID.GAME_BOY: Platform("Game Boy", "game_boy.json", "gb", "gameboy"),
    PlatformID.GAME_BOY_ADVANCE: Platform(
        "Game Boy Advance", "game_boy_advance.json", "gba", "gameboy_advance"
    ),
    PlatformID.GAME_BOY_COLOR: Platform("Game Boy Color", "game_boy_color.json", "gbc"),
    PlatformID.MAME: Platform("Mame", "mame.json"),
    PlatformID.NEO_GEO: Platform("Neo Geo", "neo_geo.json"),
    PlatformID.NEO_GEO_POCKET_NEO_GEO_POCKET_COLOR_NGPX: Platform(
        "Neo Geo Pocket Neo Geo Pocket Color Ngpx",
        "neo_geo_pocket_neo_geo_pocket_color_ngpx.json",
    ),
    PlatformID.NINTENDO_64: Platform("Nintendo 64", "nintendo_64.json", "n64"),
    PlatformID.NINTENDO_DS: Platform("Nintendo DS", "nintendo_ds.json", "nds"),
    PlatformID.NINTENDO_ENTERTAINMENT_SYSTEM: Platform(
        "Nintendo Entertainment System", "nintendo_entertainment_system.json", "nes"
    ),
    PlatformID.NINTENDO_FAMICOM_DISK_SYSTEM: Platform(
        "Nintendo Famicom Disk System", "nintendo_famicom_disk_system.json"
    ),
    PlatformID.NOKIA_NGAGE: Platform("Nokia Ngage", "nokia_ngage.json"),
    PlatformID.PANASONIC_3DO_3DO_INTERACTIVE_MULTIPLAYER: Platform(
        "Panasonic 3Do 3Do Interactive Multiplayer",
        "panasonic_3do_3do_interactive_multiplayer.json",
    ),
    PlatformID.PCFX: Platform("Pcfx", "pcfx.json"),
    PlatformID.PC_ENGINE_CD_TURBO_DUO_TURBOGRAFX_CD: Platform(
        "Pc Engine Cd Turbo Duo Turbografx Cd",
        "pc_engine_cd_turbo_duo_turbografx_cd.json",
    ),
    PlatformID.PC_ENGINE_TURBOGRAFX16: Platform(
        "Pc Engine Turbografx16", "pc_engine_turbografx16.json"
    ),
    PlatformID.PHILIPS_CDI: Platform("Philips Cdi", "philips_cdi.json"),
    PlatformID.PSX_ON_PSP: Platform("Psx On Psp", "psx_on_psp.json"),
    PlatformID.SCUMMVM: Platform("Scummvm", "scummvm.json"),
    PlatformID.SEGA_32X: Platform("Sega 32X", "sega_32x.json"),
    PlatformID.SEGA_CD: Platform("Sega Cd", "sega_cd.json"),
    PlatformID.SEGA_GAME_GEAR: Platform("Sega Game Gear", "sega_game_gear.json"),
    PlatformID.SEGA_GENESIS_SEGA_MEGADRIVE: Platform(
        "Sega Genesis Sega Megadrive",
        "sega_genesis_sega_megadrive.json",
        "sega genesis",
    ),
    PlatformID.SEGA_MASTER_SYSTEM: Platform(
        "Sega Master System", "sega_master_system.json"
    ),
    PlatformID.SEGA_NAOMI: Platform("Sega Naomi", "sega_naomi.json"),
    PlatformID.SEGA_SATURN: Platform("Sega Saturn", "sega_saturn.json"),
    PlatformID.SHARP_X68000: Platform("Sharp X68000", "sharp_x68000.json"),
    PlatformID.SONY_PLAYSTATION: Platform(
        "Sony Playstation", "sony_playstation.json", "ps1", "ps"
    ),
    PlatformID.SONY_PLAYSTATION_2: Platform(
        "Sony Playstation 2", "sony_playstation_2.json", "ps2"
    ),
    PlatformID.SONY_PLAYSTATION_DEMOS: Platform(
        "Sony Playstation Demos", "sony_playstation_demos.json"
    ),
    PlatformID.SONY_POCKETSTATION: Platform(
        "Sony Pocketstation", "sony_pocketstation.json"
    ),
    PlatformID.SONY_PSP: Platform("Sony Psp", "sony_psp.json", "psp"),
    PlatformID.SUPER_NINTENDO_ENTERTAINMENT_SYSTEM: Platform(
        "Super Nintendo Entertainment System",
        "super_nintendo_entertainment_system.json",
        "snes",
    ),
    PlatformID.VIRTUAL_BOY: Platform("Virtual Boy", "virtual_boy.json", "vb"),
    PlatformID.ZX_SPECTRUM_TAPES: Platform(
        "Zx Spectrum Tapes", "zx_spectrum_tapes.json"
    ),
    PlatformID.ZX_SPECTRUM_Z80: Platform("Zx Spectrum Z80", "zx_spectrum_z80.json"),
}
