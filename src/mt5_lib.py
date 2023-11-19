from enum import Enum

import pandas
import MetaTrader5 as mt5

def connect(json_settings: dict, credentials: dict) -> bool:
    """
    Attempts to initialize and log into MetaTrader5.

    :param json_settings: A dict containing MetaTrader5
    login details.
    :returns bool: True if initialization and login succeeds.
    Otherwise, false.
    """
    try:
        pathway = credentials["mt5"]["terminal_pathway"]
        login = credentials["mt5"]["login"]
        password = credentials["mt5"]["password"]
        server = credentials["mt5"]["server"]
        timeout = json_settings["mt5"]["timeout"]

        initialized = mt5.initialize(
            pathway, login=login, password=password, server=server, timeout=timeout
        )
        if initialized:
            print("Trading bot initialized!")
        else:
            raise ConnectionError

        # Safe to login here. Returns true if login succeeds. Otherwise, returns false.
        logged_in = mt5.login(
            login=login, password=password, server=server, timeout=timeout
        )

        if logged_in:
            print("Trading bot login successful!")
        else:
            raise PermissionError

    except KeyError as e:
        print(f"The queried dictionary key does not exist: {e.args}")
        raise e
    except ConnectionError as e:
        print(f"Could not connect to MetaTrader5: {e.args}")
        raise e
    except PermissionError as e:
        print(f"Login failed to connect to MetaTrader 5: {e.args}")
        raise e
    
    return True

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

def get_candlesticks(symbol, timeframe, num_candlesticks: int):
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
    Gets a MetaTrader 5-readable timeframe.

    :param timeframe: The to-be located timeframe as a string.
    :return: A MetaTrader 5 timeframe.
    """

    try:
        return Timeframe[timeframe].value
    except KeyError as e:
        print(f"{timeframe} is not a legal timeframe. {e}")
        
def place_order(order_type, symbol, volume, stop_loss, take_profit, comment, stop_price, direct=False):
    """
    :param order_type : String. Options: SELL_STOP, BUY_STOP
    :param symbol     : String. Symbol to trade
    :param volume     : Float. Trade volume
    :param stop_loss  : Float. Stop loss value
    :param take_profit: Float. Take profit value
    :param comment    : String. Comment used to handle multi-algorithmic trading
    :param stop_price : Float. Stop price value
    :param direct     : Boolean. Default is false. When true, bypasses order checking
    :return           : Boolean. True if order placed successfully. Otherwise, false.
    """

    # Ensure proper types and formatting
    volume = round(float(volume), 2)

    stop_loss = round(float(stop_loss), 4)
    
    take_profit = round(float(take_profit), 4)

    stop_price = round(float(stop_price), 4)

    # Request dictionary
    request = {
        "symbol": symbol,
        "volume": volume,
        "sl": stop_loss,
        "tp": take_profit,
        "type_time": mt5.ORDER_TIME_GTC,
        "comment": comment
    }

    # Update request based on order type
    if order_type == "SELL_STOP":
        request['type'] = mt5.ORDER_TYPE_SELL_STOP
        request['action'] = mt5.TRADE_ACTION_PENDING
        request['type_filling'] = mt5.ORDER_FILLING_RETURN
        
        request['price'] = stop_price if stop_price > 0 else ValueError("Stop price must be a non-zero positive value")

    elif order_type == "BUY_STOP":
        request['type'] = mt5.ORDER_TYPE_BUY_STOP
        request['action'] = mt5.TRADE_ACTION_PENDING
        request['type_filling'] = mt5.ORDER_FILLING_RETURN

        request['price'] = stop_price if stop_price > 0 else ValueError("Stop price must be a non-zero positive value")

    else:
        raise ValueError(f"Unsupported order type given: {order_type}")

    # No order checking
    if direct:
        order_result = mt5.order_send(request)
        # Order send status: OK
        if order_result[0] == 10009:
            return order_result[2]
        else:
            raise Exception(f"Error. Order code: {order_result[0]}. Code descriptions: https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes")
    else:
        result = mt5.order_check(request)

        # Order check status: OK
        if result[0] == 0:
            return place_order(order_type, symbol, volume, stop_price, stop_loss, take_profit, comment, True)
        else:
            raise Exception(f"Order Code: {result[0]}. Code descriptions: https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes")

def cancel_order(order_number):
    """
    Function to cancel an order indentified by an order number
    :param order_number: int representing the order number from MT5
    :return: Boolean. Tue = cancelled. False == Not cancelled.
    """
    # Create request
    request = {
        "action": mt5.TRADE_ACTION_REMOVE,
        "order": order_number,
        "comment": "order removed"    
    }
    # Attempt to send the order to MT5
    try: 
        order_result = mt5.order_send(request)
        if order_result[0] == 10009:
            print(f"Order {order_number} successfully cancelled")
            return True
        else:
            print(f"Order {order_number} unable to be cancelled")
            return False
    except Exception as e:
        print(f"Error cancelling order {order_number}. Error {e}")

def get_all_open_orders():
    """
    Function to retrieve all open orders from MetaTrader 5
    :return: List of all open orders.
    """
    return mt5.orders_get()

def get_filtered_list_of_orders(symbol, comment):
    """
    Function to retreive a filtered list of open orders from Mt5. Filtering is based on symbol and comment
    :param symbol: string of the symbol being traded
    :param comment: string of the comment
    :return: (filtered) list of orders
    """
    # Retrieve a list of open orders, filtered by symbol
    open_orders_by_symbol = mt5.orders_get(symbol)
    # Check if any order were retreived
    if open_orders_by_symbol is None or len(open_orders_by_symbol) == 0:
        return []
    
    # Convert the retrieved orders into a dataframe
    open_orders_dataframe = pandas.DataFrame(
        list(open_orders_by_symbol),
        columns=open_orders_by_symbol[0]._asdict().keys()
    )

    # From the open orders dataframe, fitler orders by comment
    open_orders_dataframe = open_orders_dataframe[open_orders_dataframe['comment'] == comment]
    # Create a list to store the open order numbers
    open_orders = {}
    # Iterate through the dataframe and add order numbers to the list
    for order in open_orders_dataframe['ticket']:
        open_orders.append(order)
    return open_orders

def cancel_filtered_orders(symbol, comment):
    """
    Function to cancel a list of filtered orders. Based upon two filters: symbol & comment
    :param symbol: string of symbol
    :param commment: string of the commment
    :return: Boolean. True = orders cancelled. False = issue with cancellation request
    """
    # Retrieve a list of the orders based upon the filter
    orders = get_filtered_list_of_orders(symbol, comment)
    if len(orders) > 0:
        # Iterate and cancel
        for order in orders:
            cancel_outcome = cancel_order(order)
            if not cancel_outcome:
                return False
        return True
    else:
        return True

class Timeframe(Enum):
    M1  = mt5.TIMEFRAME_M1
    M2  = mt5.TIMEFRAME_M2
    M3  = mt5.TIMEFRAME_M3
    M4  = mt5.TIMEFRAME_M4
    M5  = mt5.TIMEFRAME_M5
    M6  = mt5.TIMEFRAME_M6
    M10 = mt5.TIMEFRAME_M10
    M12 = mt5.TIMEFRAME_M12
    M15 = mt5.TIMEFRAME_M15
    M20 = mt5.TIMEFRAME_M20
    M30 = mt5.TIMEFRAME_M30
    MN1 = mt5.TIMEFRAME_MN1
    H1  = mt5.TIMEFRAME_H1
    H2  = mt5.TIMEFRAME_H2
    H3  = mt5.TIMEFRAME_H3
    H4  = mt5.TIMEFRAME_H4
    H6  = mt5.TIMEFRAME_H6
    H8  = mt5.TIMEFRAME_H8
    D1  = mt5.TIMEFRAME_D1
