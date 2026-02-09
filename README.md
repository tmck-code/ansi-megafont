# ansi-megafont

A single font for displaying ANSI images that combines several Amiga & IBM fonts.

- [ansi-megafont](#ansi-megafont)
  - [Get the font](#get-the-font)
  - [Installation](#installation)
  - [Credits](#credits)
  - [Font Codepage Mappings](#font-codepage-mappings)

---

## Get the font

Download the font file from the [latest release](https://github.com/tmck-code/ansi-megafont/releases/latest).

## Installation

To install:
- download the [`latest release`](https://github.com/tmck-code/ansi-megafont)
- install it on your system via your regular font installer
- and ensure that your terminal emulator is configured to use it._

<details>
<summary>
Alternatively, you can install using one of these commands:
</summary>

> [!NOTE]
> _You will still need to configure your terminal to use the font_

```shell
# osx
curl -sOL --output-dir ~/Library/Fonts/ https://github.com/tmck-code/ansi-megafont/releases/download/v0.1.1/ANSICombined.ttf \
  && fc-cache -f ~/Library/Fonts/ \
  && fc-list | grep "ANSICombined"

# linux
curl -sOL --output-dir ~/.fonts/ https://github.com/tmck-code/ansi-megafont/releases/download/v0.1.1/ANSICombined.ttf \
  && fc-cache -f ~/.fonts/ \
  && fc-list | grep "ANSICombined"
```

</details>

## Credits

Fonts are from:

- <https://int10h.org/oldschool-pc-fonts/download/>
- <https://github.com/rewtnull/amigafonts#>

## Font Codepage Mappings

Each font contains 256 characters (0x00-0xFF) mapped to Unicode Private Use Area positions.

| Font Name                                    | Offset   |
|----------------------------------------------|----------|
| [Topaz A500](docs/Topaz_A500.md)             | `U+E000` |
| [Topaz Plus A500](docs/Topaz_Plus_A500.md)   | `U+E100` |
| [Topaz A1200](docs/Topaz_A1200.md)           | `U+E200` |
| [Topaz Plus A1200](docs/Topaz_Plus_A1200.md) | `U+E300` |
| [MicroKnight](docs/MicroKnight.md)           | `U+E400` |
| [MicroKnight Plus](docs/MicroKnight_Plus.md) | `U+E500` |
| [mO'sOul](docs/mOsOul.md)                    | `U+E600` |
| [P0T-NOoDLE](docs/P0T_NOoDLE.md)             | `U+E700` |
| [IBM VGA 9x16](docs/IBM_VGA_9x16.md)         | `U+E800` |
