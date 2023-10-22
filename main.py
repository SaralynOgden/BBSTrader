"""json import"""
import json
import os

import mt5_lib as trader

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "settings.json"


def get_trader_settings(file_path: str) -> dict:
    """
    Attempts to deserialize the data in ACCOUNT_SETTINGS_PATH
    into a json array.

    :param file_path: The file path to deserialize from.
    :returns dict: A dictionary mirroring the json format.
    """

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf8") as file:
            # Convert to json object
            json_settings = json.load(file)
            return json_settings

    raise FileExistsError(f"Could not locate resource: {file_path}")


def main():
    """
    Business logic entry point.
    """

    print("Main")

    # Prevents imported invocations of main().
    if __name__ != "__main__":
        raise RuntimeError(f"main() should only be invoked in: {__file__}")

    # Deserialize MetaTrader settings
    json_settings = get_trader_settings(ACCOUNT_SETTINGS_PATH)

    # Establish connection to MetaTrader. trader.connect() throws a
    # ConnectionError if a connection cannot be established
    trader.connect(json_settings)

    # Until further logic is implemented, the terminal will close immediately
    # after the previous statement executes. This is the expected behavior.


main()
