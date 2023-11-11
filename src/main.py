import json
import os
import pandas

import mt5_lib as trader
import ema_cross_strategy as strats

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "./settings.json"
CREDENTIALS_FILE_PATH = "./credentials.json"


def get_json_from_file(file_path: str) -> dict:
    """
    Attempts to deserialize the data in the given file path
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
    json_settings = get_json_from_file(ACCOUNT_SETTINGS_PATH)

    # Get user credentials
    credentials = get_json_from_file(CREDENTIALS_FILE_PATH)

    # Establish connection to MetaTrader. trader.connect() throws a
    # ConnectionError if a connection cannot be established
    trader.connect(json_settings, credentials)

    # Get symbols array from settings.json
    symbols_arr = json_settings["mt5"]["symbols"]

    # Initialize all symbols
    for symbol in symbols_arr:
        try:
            trader.initialize_symbol(symbol)
        except Exception as e:
            print(e)
        
    timeframe=json_settings["mt5"]["timeframe"]
    
    # Get a table of ema calculations for every initialized symbol
    for symbol in symbols_arr:
        # Shows all columns
        pandas.set_option('display.max_columns', None)
        ema_x_strategy_table = strats.ema_cross_strategy(symbol, timeframe, 50, 200)
        print(ema_x_strategy_table)

if __name__ == '__main__':
    main()