import argparse
import logging

from src import bot


def set_up_logging_configuration(log_level):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

parser = argparse.ArgumentParser(description="PVPokeLossBot is a bot designed for the PVP mode of the mobile game Pokemon Go.")
parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
parser.add_argument('--skip-adb-check', action='store_true', help='Skip ADB connectivity check at startup (advanced users only)')

args = parser.parse_args()

set_up_logging_configuration(logging.DEBUG if args.verbose else logging.INFO)

try:
    bot.run(skip_adb_check=args.skip_adb_check)
except KeyboardInterrupt:
    print("")
    print("Exiting program...")
