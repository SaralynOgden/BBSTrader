"""json import"""
import json
import os

import mt5_lib as trader

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "../settings.json"


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

    # Prevents imported invocations of main().
    if __name__ != "__main__":
        raise RuntimeError(f"main() should only be invoked in: {__file__}")

    # Deserialize MetaTrader settings
    json_settings = get_trader_settings(ACCOUNT_SETTINGS_PATH)

    # Establish connection to MetaTrader. trader.connect() throws a
    # ConnectionError if a connection cannot be established
    trader.connect(json_settings)

    # Get symbols array from settings.json
    symbols_arr = json_settings["mt5"]["symbols"]

    # Initialize all symbols
    for symbol in symbols_arr:
        try:
            is_initialized = trader.initialize_symbol(symbol)
        except Exception as e:
            print(e)
        

    # Get candlesticks for every initialized symbol
    for symbol in symbols_arr:
        candlesticks = trader.get_candlesticks(
            symbol=symbol,
            timeframe=json_settings["mt5"]["timeframe"],
            num_candlesticks=50000
        )
        
        print(candlesticks)


if __name__ == '__main__':
    main()