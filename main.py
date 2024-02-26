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

args = parser.parse_args()

set_up_logging_configuration(logging.DEBUG if args.verbose else logging.INFO)

try:
    bot.run()
except KeyboardInterrupt:
    print("")
    print("Exiting program...")
