"""MetaTrader5 API import"""
import MetaTrader5 as mt5

import pandas


def connect(json_settings: dict) -> bool:
    """
    Attempts to initialize and log into MetaTrader5.

    :param json_settings: A dict containing MetaTrader5
    login details.
    :returns bool: True if initialization and login succeeds.
    Otherwise, false.
    """
    try:
        pathway = json_settings["mt5"]["terminal_pathway"]
        login = json_settings["mt5"]["login"]
        password = json_settings["mt5"]["password"]
        server = json_settings["mt5"]["server"]
        timeout = json_settings["mt5"]["timeout"]

        initialized = mt5.initialize(
            pathway, login=login, password=password, server=server, timeout=timeout
        )
<<<<<<< HEAD
        if initialized:
            print("Trading bot initialized!")
=======
>>>>>>> bb7d06cf9f09feb1fc6d1100ddfe38bed3c74e76
        if not initialized:
            raise ConnectionError

        # Safe to login here. Returns true if login succeeds. Otherwise, returns false.
<<<<<<< HEAD
        logged_in = mt5.login(
            login=login, password=password, server=server, timeout=timeout
        )

        if logged_in:
            print("Trading bot login successful!")
        if not logged_in:
            raise PermissionError
=======
        return mt5.login(login=login, password=password, server=server, timeout=timeout)
>>>>>>> bb7d06cf9f09feb1fc6d1100ddfe38bed3c74e76

    except KeyError as e:
        print(f"The queried dictionary key does not exist: {e.args}")
        raise e
    except ConnectionError as e:
        print(f"Could not connect to MetaTrader5: {e.args}")
        raise e
<<<<<<< HEAD
    except PermissionError as e:
        print(f"Login failed to connect to MetaTrader 5: {e.args}")
        raise e
=======

>>>>>>> bb7d06cf9f09feb1fc6d1100ddfe38bed3c74e76

def initialize_symbol(symbol) -> bool:
    """
    Initializes a MetaTrader 5 symbol.
    :param symbol: The MetaTrader 5 symbol.
    :return Boolean: True if initialized. Otherwise, false
    """

    #Get all MT5 symbols
    symbols = mt5.symbols_get()

    #Store the symbol names in a list
    symbol_names = []

    #Populate list
    for current_symbol in symbols:
        symbol_names.append(current_symbol.name)

    #Check if the given symbol name is in our list
    if symbol in symbol_names:
        try:
            mt5.symbol_select(symbol, True)
            return True
        except Exception as e:
            print(f"Error enabling {symbol}. Error: {e}")
            return False
    else:
        print(f"Symbol {symbol} does not exist.")
        return False

def get_candlesticks(symbol, timeframe: int, num_candlesticks: int):
    """
    Retrieves `num_candlesticks` candlesticks for symbol `symbol` from MetaTrader 5.
    :param `symbol`: The symbol to retrieve candlesticks for.
    :param `timeframe`: The timeframe to retrieve from.
    :param `num_candlesticks`: The number of candlesticks to retrieve.
    """

    #Get MT5-Readable timeframe
    mt5_timeframe = get_mt5_timeframe(timeframe=timeframe)

    #Get candles
    candles = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 1, num_candlesticks)

    #return a pandas dataframe
    return pandas.DataFrame(candles)



def get_mt5_timeframe(timeframe):
    """
    Converts `timeframe` to a MetaTrader 5-readable timeframe.
    :param `timeframe` The string to be converted to a MetaTrader 5 timeframe (int)
    """
    match timeframe:
        case "M1":
            return mt5.TIMEFRAME_M1
        case "M2":
            return mt5.TIMEFRAME_M2
        case "M3":
            return mt5.TIMEFRAME_M3
        case "M4":
            return mt5.TIMEFRAME_M4
        case "M5":
            return mt5.TIMEFRAME_M5
        case "M6":
            return mt5.TIMEFRAME_M6
        case "M10":
            return mt5.TIMEFRAME_M10
        case "M12":
            return mt5.TIMEFRAME_M12
        case "M15":
            return mt5.TIMEFRAME_M15
        case "M20":
            return mt5.TIMEFRAME_M20
        case "M30":
            return mt5.TIMEFRAME_M30
        case "MN1":
            return mt5.TIMEFRAME_MN1
        case "H1":
            return mt5.TIMEFRAME_H1
        case "H2":
            return mt5.TIMEFRAME_H2
        case "H3":
            return mt5.TIMEFRAME_H3
        case "H4":
            return mt5.TIMEFRAME_H4
        case "H6":
            return mt5.TIMEFRAME_H6
        case "H8":
            return mt5.TIMEFRAME_H8
        case "D1":
            return mt5.TIMEFRAME_D1
        case _:
            raise ValueError(f"{timeframe} is not a valid timeframe.")
        
