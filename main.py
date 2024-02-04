import logging

from src import bot


def set_up_logging_configuration():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


set_up_logging_configuration()

try:
    bot.run()
except KeyboardInterrupt:
    print("")
    print("Exiting program...")
