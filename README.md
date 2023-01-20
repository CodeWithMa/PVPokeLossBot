# PVPokeLossBot

## Summary

PVPokeLossBot is a bot designed for the PVP mode of the mobile game Pokemon Go.
Using computer vision, the bot analyzes screenshots of the game and makes decisions on which actions to perform, such as sending `adb tap` commands to the game.
The bot also has a built-in timer that automatically forfeits the game after a certain period of time.

## Installation

To use PVPokeLossBot, you will first need to install the required dependencies:

``` bash
pip install -r requirements.txt
```

## Usage

TODO

## Adding New Images

PVPokeLossBot uses a set of template images to compare with screenshots of the game.
When a match is found, the bot will click on the middle of the found image.

To add new images to be used as templates, place them in the "images" directory and convert them to greyscale using the script `convert-to-greyscale.py`:

``` bash
python convert-to-greyscale.py
```

## The Secret to Farming Stardust in Pokemon Go: PVPokeLossBot's Elo Drop Strategy

"Elo" is a ranking system used in competitive games such as Pokemon Go PVP to match players of similar skill levels against each other.
By using PVPokeLossBot, the bot will forfeit the game on purpose, which will cause the user's Elo to drop lower and lower.
As a result, the user will only play against other players who also have a low Elo, most likely because they also use loss bot, thus the user will play against players who also forfeit the game, which can make it easier to farm stardust.

## Warning

Please be aware that using such a bot can be against the terms of service of the game, use it at your own risk.
