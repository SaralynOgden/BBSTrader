import indicator_lib
import mt5_lib

def ema_cross_strategy(symbol, timeframe, short_term_ema, long_term_ema):
    """
    Function which runs the EMA Cross Strategy
    :param symbol: string of the sumbol to be queried
    :param timeframe: string of the timeframe to be queried
    :param short_term_ema: integer of the lowest timeframe length for EMA
    :param long_term_ema: integer of the highest timeframe length for EMA
    """

    # Get candlesticks dataframe
    candlesticks_dataframe = get_candlesticks_dataframe(
        symbol=symbol,
        timeframe=timeframe
    )
    # Append indicators to dataframe
    candlesticks_dataframe = calc_ind(
        data=candlesticks_dataframe,
        ema_one=short_term_ema,
        ema_two=long_term_ema
    )
    return candlesticks_dataframe

# Function to calculate the indicators for this strategy
def calc_ind(data, ema_one, ema_two):
    """
    Function to calculate the indicators for the EMA Cross strategy
    :param data: dataframe of the raw data
    :param ema_one: integer for the first ema
    :param ema_two: integer for the second ema
    :return: dataframe with updated columns
    """
    # Calculate the first EMA
    dataframe = indicator_lib.calc_ema(
        candlesticks_dataframe=data,
        ema_size=ema_one
    )
    # Calculate the second ema
    dataframe = indicator_lib.calc_ema(
        candlesticks_dataframe=dataframe,
        ema_size=ema_two
    )
    # Calculate the EMA Cross
    dataframe = indicator_lib.ema_cross_calc(
        dataframe=dataframe,
        ema_one=ema_one,
        ema_two=ema_two
    )
    # Return the dataframe to the user with the indicators
    return dataframe

def get_candlesticks_dataframe(symbol, timeframe):
    """
    Function to retreive candlesticks from MT5 as a dataframe.
    :param symbol: string of the symbol to be retreived
    :param timeframe: string of the timeframe to be retreived
    :return: dataframe to user
    """

    # Retreive the data
    candlesticks_dataframe = mt5_lib.get_candlesticks(
        symbol=symbol,
        timeframe=timeframe,
        num_candlesticks=1000
    )
    # Return data
    return candlesticks_dataframe