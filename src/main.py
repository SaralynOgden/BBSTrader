import json
import os
import time
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

def run_strategy(json_settings):
    """
    Function to execute the stategy in main
    :param json_settings: json of project settings
    :param credentials: json of user credentials
    :return: Boolean. True if strategy ran successfully with no errors. Else False.
    """
    # Get symbols array from settings.json
    symbols_arr = json_settings["mt5"]["symbols"]

    # Get timeframe from settings.json
    timeframe=json_settings["mt5"]["timeframe"]

    # Strategy Risk Management
    # Get a list of open orders
    orders = trader.get_all_open_orders()
    # Iterate through the open orders and cancel
    for order in orders:
        trader.cancel_order(order)

    # Initialize all symbols
    for symbol in symbols_arr:
        try:
            trader.initialize_symbol(symbol)
        except Exception as e:
            print(e)
    
    # Get a table of ema calculations for every initialized symbol
    for symbol in symbols_arr:

        # Strategy Risk Management
        # Generate the comment string
        comment_string = f"EMA_Cross_strategy_{symbol}"

        # Cancel orders related to the symbol and strategy
        trader.cancel_filtered_orders(symbol, comment_string)

        # Boolean from the strategy
        ema_x_strategy_table = strats.ema_cross_strategy(symbol, timeframe, 1, 2, 10000, 0.03)

        # Console output
        if (ema_x_strategy_table):
            print(f"Trade made on {symbol}.")
        else:
            print(f"No trade for {symbol}.")

    return True

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
    connected = trader.connect(json_settings, credentials)

    # Shows all columns
    pandas.set_option('display.max_columns', None)

    if connected:
        current_time = 0
        previous_time = 0

        # Get timeframe from settings.json
        timeframe=json_settings["mt5"]["timeframe"]
        while True:
            # Get new candle
            new_candle = trader.get_candlesticks("BCHUSD",timeframe,1)

            current_time = new_candle['time'][0]

            if(current_time != previous_time):
                # Discovered a new candle
                print("New candlestick. Time to trade!")

                # Update previous time
                previous_time = current_time

                strategy = run_strategy(json_settings)

            else:
                # No new candles
                print("No new candles. Sleeping.")
                time.sleep(1)

if __name__ == '__main__':
    main()