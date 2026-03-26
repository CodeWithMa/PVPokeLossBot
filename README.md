# PVPokeLossBot

This only works on android. It uses [adb](https://developer.android.com/tools/adb) to connect to your phone.


## Summary

PVPokeLossBot is a bot designed for the PVP mode of the mobile game Pokemon Go.
Using computer vision, the bot analyzes screenshots of the game and makes decisions on which actions to perform, such as sending `adb tap` commands to the game.
The bot also has a built-in timer that automatically forfeits the game after a certain period of time.

![pvp leagues](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic0.gamerantimages.com%2Fwordpress%2Fwp-content%2Fuploads%2F2020%2F07%2Fpokemon-go-battle-league-season-3-e1595952020123.jpg&f=1&nofb=1&ipt=a981ff5cbef41827663812e2a15e2ece03ec8a5505f8915cdf5f5d356843d09a&ipo=images)

## Installation

To use PVPokeLossBot, you will first need to install the required dependencies.

### Create and Activate a Virtual Environment

Using [venv](https://docs.python.org/3/library/venv.html), create a virtual environment to manage dependencies:

``` bash
python -m venv venv
venv/scripts/activate
```

### Install dependencies

``` bash
pip install -r requirements.txt
```
## Add ADB to Your System PATH

Locate the adb folder in the extracted folder (platform-tools).
Copy the path to the folder (e.g., C:\Users\<YourUser>\Downloads\PVPokeLossBot-dev\platform-tools).

On Windows:

Search “Edit the system environment variables” → Open “Environment Variables”.
Under “System variables”, find and select Path, then click “Edit”.
Click “New” and paste the path to your platform-tools folder.
Click OK to save and restart your terminal.

## Usage

Make sure you are in your venv if you used one.

``` bash
venv/scripts/activate
```

The bot automatically checks that ADB (Android Debug Bridge) is properly installed and can connect to your device before starting. Ensure your Android device is connected via USB with USB debugging enabled.

To run the bot, you can use the following command:

``` bash
python main.py
```

Run it with `--verbose` to get more output.

``` bash
python main.py --verbose
```

For advanced users, you can skip the automatic ADB connectivity check with:

``` bash
python main.py --skip-adb-check
```

**Note**: Only use `--skip-adb-check` if you're sure ADB is working properly, as the bot will fail if ADB commands don't work.

You can also configure the bot's settings by editing the `bot.py` file.
For example, you can adjust the time the bot will stay in the game before forfeiting.

### Example Output

PVPokeLossBot will output information about its actions and the results of the image matching.
Below is an example of the output you may see while the bot is running:

``` bash
2025-09-03 12:18:06 Screenshot saved to screenshots\screenshot.png
2025-09-03 12:18:06 Screenshot hash: 5bccc269456fe924d0f50932dd13e472
2025-09-03 12:18:06 Running image matching...
2025-09-03 12:18:07 Template 'claim_rewards_button_text.en.png': match confidence 0.4624
2025-09-03 12:18:07 Template 'claim_rewards_button_text.png': match confidence 0.3119
2025-09-03 12:18:07 Template 'claim_rewards_button_text2.png': match confidence 0.4475
2025-09-03 12:18:07 Template 'confirm_game_result_all_games_played_button.png': match confidence 0.3542
2025-09-03 12:18:07 Template 'confirm_party_search_button.en.png': match confidence 0.9743
2025-09-03 12:18:07 Template 'confirm_party_search_button.png': match confidence 0.6756
2025-09-03 12:18:07 Template 'enemy_charge_attack.png': match confidence 0.2437
2025-09-03 12:18:07 Template 'forfeit.png': match confidence 0.9981
2025-09-03 12:18:07 Template 'forfeit_1.png': match confidence 0.5382
2025-09-03 12:18:07 Template 'max_number_of_games_played_text.en.png': match confidence 0.4017
2025-09-03 12:18:07 Template 'max_number_of_games_played_text.png': match confidence 0.2709
2025-09-03 12:18:07 Template 'max_number_of_games_played_text2.en.png': match confidence 0.2987
2025-09-03 12:18:07 Template 'reward_1_2_icon.png': match confidence 0.7334
2025-09-03 12:18:08 Template 'reward_1_icon.png': match confidence 0.5478
2025-09-03 12:18:08 Template 'reward_2_icon.png': match confidence 0.4625
2025-09-03 12:18:08 Template 'reward_3_icon.png': match confidence 0.3415
2025-09-03 12:18:08 Template 'reward_4_icon.png': match confidence 0.5072
2025-09-03 12:18:08 Template 'search_next_game_button_text.en.png': match confidence 0.4627
2025-09-03 12:18:08 Template 'search_next_game_button_text.png': match confidence 0.4302
2025-09-03 12:18:08 Template 'select_hypa_league.png': match confidence 0.3831
2025-09-03 12:18:08 Template 'select_master_league.png': match confidence 0.4631
2025-09-03 12:18:08 Template 'select_super_league.png': match confidence 0.4494
2025-09-03 12:18:08 Template 'start_button_text.en.png': match confidence 0.5020
2025-09-03 12:18:08 Template 'start_button_text.png': match confidence 0.5858
2025-09-03 12:18:08 Template 'start_button_text2.en.png': match confidence 0.7802
2025-09-03 12:18:09 Template 'start_button_text2.png': match confidence 0.6799
2025-09-03 12:18:09 Template 'start_button_text3.en.png': match confidence 0.6981
2025-09-03 12:18:09 Template 'start_button_text4.en.png': match confidence 0.7718
2025-09-03 12:18:09 Template 'start_button_text5.en.png': match confidence 0.7266
2025-09-03 12:18:09 Template 'start_button_yes.png': match confidence 0.6609
2025-09-03 12:18:09 Template 'welcome_to_gbl_button_text.en.png': match confidence 0.4897
2025-09-03 12:18:09 Template 'welcome_to_gbl_button_text.png': match confidence 0.4706
2025-09-03 12:18:09 Found images over threshold: [('forfeit.png', FindImageResult(val=0.9980706572532654, coords=(114, 228))), ('confirm_party_search_button.en.png', FindImageResult(val=0.9742874503135681, coords=(541, 2143)))]
2025-09-03 12:18:09 Tapping confirm_party_search_button.en.png at (541, 2143) (confidence 97.43%)
2025-09-03 12:18:09 ADB tap sent to coordinates (541, 2143)
```

Each line of output shows the date and time of the action, the image file name that was matched, and the match value as a percentage.

## Adding New Images

PVPokeLossBot uses a set of template images to compare with screenshots of the game.
When a match is found, the bot will click on the middle of the found image.

To add new images to be used as templates, place them in the "images" directory and convert them to greyscale using the script `convert-to-greyscale.py`:

``` bash
python convert-to-greyscale.py
```

If you are using the bot in a different language than the one provided in the template images, you can contribute by adding new images for different languages.
You can create a pull request with the new images and the corresponding language identifier in the file name, for example, `start_button_text2.fr.png` for French.

## Adjust Forfeit Delay
Find this part in analyze_results_and_return_action (or wherever you handle the forfeit template):

``` bash
if image_file.startswith("forfeit"):  # or your specific template name
    return GameAction(
        action=GameActions.tap_position,
        position=find_image_result.coords,
        delay_before_tap=3.0  # <--- CHANGE THIS VALUE
    )
```
To change the delay:
Change 3.0 to any number of seconds you want (e.g., 5.0 for 5 seconds, 1.5 for 1.5 seconds).

## Known Issues

Stuck after claiming Encounter reward since the bot is not made to catch pokemon

## The Secret to Farming Stardust in Pokemon Go: PVPokeLossBot's Elo Drop Strategy

"Elo" is a ranking system used in competitive games such as Pokemon Go PVP to match players of similar skill levels against each other.
By using PVPokeLossBot, the bot will forfeit the game on purpose, which will cause the user's Elo to drop lower and lower.
As a result, the user will only play against other players who also have a low Elo, most likely because they also use loss bot, thus the user will play against players who also forfeit the game, which can make it easier to farm stardust.

## Warning

Please be aware that using such a bot can be against the terms of service of the game, use it at your own risk.
