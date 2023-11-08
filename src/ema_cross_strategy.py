import indicator_lib
import mt5_lib

def ema_cross_strategy(symbol, timeframe, short_term_ema, long_term_ema):
    """
    Function which runs the EMA Cross Strategy
    :param symbol: string of the sumbol to be queried
    :param timeframe: string of the timeframe to be queried
    :param ema_one: integer of the lowest timeframe length for EMA
    :param ema_two: intefer of the highest timeframe length for EMA
    """

    # Get vanilla MetaTrader 5 dataframe
    dataframe = mt5_lib.get_candlesticks(
        symbol=symbol,
        timeframe=timeframe,
        num_candlesticks=1000
    )
    # Append indicator columns to dataframe
    dataframe = calculate_indicators(
        data=dataframe,
        ema_one=short_term_ema,
        ema_two=long_term_ema
    )
    return dataframe

# Function to calculate the indicators for this strategy
def calculate_indicators(data, ema_one, ema_two):
    """
    Function to calculate the indicators for the EMA Cross strategy
    :param data: dataframe of the raw data
    :param ema_one: integer for the first ema
    :param ema_two: integer for the second ema
    :return: dataframe with updated columns
    """
    # Calculate the first EMA
    dataframe = indicator_lib.calc_ema(
        dataframe=data,
        ema_size=ema_one
    )
    # Calculate the second ema
    dataframe = indicator_lib.calc_ema(
        dataframe=dataframe,
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
