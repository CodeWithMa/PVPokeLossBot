# PVPokeLossBot

## Summary

This project is a bot for the mobile game Pokemon Go, specifically for the PVP mode.
The bot uses computer vision to analyze screenshots of the game and make decisions on which actions to perform, such as sending `adb tap` commands to the game.
The bot also has a timer to forfeit the game after a certain amount of time has passed.

## Usage

``` bash
pip install -r requirements.txt
```

## Add new images

The bot uses computer vision to analyze screenshots of the game, by comparing the screenshot with a set of template images stored in the image directory.
When the bot finds a match of the screenshot with one of the template images, it will click on the middle of the found image on the screenshot.

To add new images to be used as templates, you can simply place them inside the image directory and convert them to greyscale using the script `convert-to-greyscale.py`.
Just call it:

``` bash
python convert-to-greyscale.py
```

## The Secret to Farming Stardust in Pokemon Go: PVPokeLossBot's Elo Drop Strategy

"Elo" is a ranking system used in competitive games such as Pokemon Go PVP to match players of similar skill levels against each other.
By using PVPokeLossBot, the bot will forfeit the game on purpose, which will cause the user's Elo to drop lower and lower.
As a result, the user will only play against other players who also have a low Elo, most likely because they also use loss bot, thus the user will play against players who also forfeit the game, which can make it easier to farm stardust.
