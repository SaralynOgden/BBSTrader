import indicator_lib
import mt5_lib

def ema_cross_strategy(symbol, timeframe, ema_one, ema_two):
    """
    Function which runs the EMA Cross Strategy
    :param symbol: string of the sumbol to be queried
    :param timeframe: string of the timeframe to be queried
    :param ema_one: integer of the lowest timeframe length for EMA
    :param ema_two: intefer of the highest timeframe length for EMA
    """

    ### Pseudo Code Steps
    # Step 1: Retreive data -> get_data()
    # Step 2: Calculated indicators -> calc_ind()
    # Step 3: Determine if a trade event has occured -> det_trade()
    # Step 4: Return information back to the user

    # Step 1
    data = get_data(
        symbol=symbol,
        timeframe=timeframe
    )
    # Step 2
    data = calc_ind(
        data=data,
        ema_one=ema_one,
        ema_two=ema_two
    )
    return data

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

def get_data(symbol, timeframe):
    """
    Function to retreive data from MT5. Data is in the from of candlesticks and is retreived as a dataframe
    :param symbol: string of the symbol to be retreived
    :param timeframe: string of the timeframe to be retreived
    :return: dataframe to user
    """

    # Retreive the data
    data = mt5_lib.get_candlesticks(
        symbol=symbol,
        timeframe=timeframe,
        num_candlesticks=1000
    )
    # Return data
    return data