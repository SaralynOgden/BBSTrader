import indicator_lib
import mt5_lib

def ema_cross_strategy(symbol, timeframe, short_term_ema, long_term_ema):
    """
    Function which runs the EMA Cross Strategy
    :param symbol: string of the sumbol to be queried
    :param timeframe: string of the timeframe to be queried
    :param short_term_ema: integer of the lowest timeframe length for EMA
    :param long_term_ema: intefer of the highest timeframe length for EMA
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
        short_term_ema=short_term_ema,
        long_term_ema=long_term_ema
    )
    return dataframe

# Function to calculate the indicators for this strategy
def calculate_indicators(data, short_term_ema, long_term_ema):
    """
    Function to calculate the indicators for the EMA Cross strategy
    :param data: dataframe of the raw data
    :param short_term_ema: integer for the first ema
    :param long_term_ema: integer for the second ema
    :return: dataframe with updated columns
    """
    # Calculate the first EMA
    dataframe = indicator_lib.calc_ema(
        dataframe=data,
        ema_size=short_term_ema
    )
    # Calculate the second ema
    dataframe = indicator_lib.calc_ema(
        dataframe=dataframe,
        ema_size=long_term_ema
    )
    # Calculate the EMA Cross
    dataframe = indicator_lib.ema_cross_calc(
        dataframe=dataframe,
        short_term_ema=short_term_ema,
        long_term_ema=long_term_ema
    )
    # Return the dataframe to the user with the indicators
    return dataframe
