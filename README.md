# PVPokeLossBot

This only works on android. It uses [adb](https://developer.android.com/tools/adb) to connect to your phone.

## Summary

PVPokeLossBot is a bot designed for the PVP mode of the mobile game Pokemon Go.
Using computer vision, the bot analyzes screenshots of the game and makes decisions on which actions to perform, such as sending `adb tap` commands to the game.
The bot also has a built-in timer that automatically forfeits the game after a certain period of time.

![pvp leagues](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic0.gamerantimages.com%2Fwordpress%2Fwp-content%2Fuploads%2F2020%2F07%2Fpokemon-go-battle-league-season-3-e1595952020123.jpg&f=1&nofb=1&ipt=a981ff5cbef41827663812e2a15e2ece03ec8a5505f8915cdf5f5d356843d09a&ipo=images)

## Installation

To use PVPokeLossBot, you will first need to install the required dependencies:

``` bash
pip install -r requirements.txt
```

## Usage

To run the bot, you can use the following command:

``` bash
python main.py
```

You can also configure the bot's settings by editing the `bot.py` file.
For example, you can adjust the time the bot will stay in the game before forfeiting.

### Example Output

PVPokeLossBot will output information about its actions and the results of the image matching.
Below is an example of the output you may see while the bot is running:

``` bash
2023-01-20 09:45:10 Image start_button_text2.en.png matches with 99.99927282333374%
2023-01-20 09:45:15 Image welcome_to_gbl_button_text.en.png matches with 100.0%
2023-01-20 09:45:19 Image select_super_league.png matches with 100.0%
2023-01-20 09:45:24 Image confirm_party_search_button.en.png matches with 99.99873638153076%
2023-01-20 09:46:43 Image ingame_opponent_3_pokemon_left.png matches with 99.86531138420105%
2023-01-20 09:46:48 Image ingame_opponent_2_pokemon_left.png matches with 99.82503652572632%
2023-01-20 09:46:51 Timer has run out. Forfeit the game.
```

Each line of output shows the date and time of the action, the image file name that was matched, and the match value as a percentage.
The bot will also output a message when the timer runs out and it forfeits the game.

## Adding New Images

PVPokeLossBot uses a set of template images to compare with screenshots of the game.
When a match is found, the bot will click on the middle of the found image.

To add new images to be used as templates, place them in the "images" directory and convert them to greyscale using the script `convert-to-greyscale.py`:

``` bash
python convert-to-greyscale.py
```

If you are using the bot in a different language than the one provided in the template images, you can contribute by adding new images for different languages.
You can create a pull request with the new images and the corresponding language identifier in the file name, for example, `start_button_text2.fr.png` for French.

## Known Issues

The bot may get stuck on the forfeit the game screen.
Pokemon Go has to be restarted manually.

## The Secret to Farming Stardust in Pokemon Go: PVPokeLossBot's Elo Drop Strategy

"Elo" is a ranking system used in competitive games such as Pokemon Go PVP to match players of similar skill levels against each other.
By using PVPokeLossBot, the bot will forfeit the game on purpose, which will cause the user's Elo to drop lower and lower.
As a result, the user will only play against other players who also have a low Elo, most likely because they also use loss bot, thus the user will play against players who also forfeit the game, which can make it easier to farm stardust.

## Warning

Please be aware that using such a bot can be against the terms of service of the game, use it at your own risk.
