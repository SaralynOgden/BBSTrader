import numpy as np

def calc_ema(dataframe, ema_size):
    """
    Calculates the Exponential Moving Average (EMA) of size `ema_size`
    for each entry in `dataframe`.

    :param `dataframe`: The dataframe from which EMAs will be determined.
    :param `ema_size`: The EMA size
    """
    # Column name to append to dataframe
    ema_name = "ema_" + str(ema_size)

    # Create EMA multiplier
    multiplier = 2/(ema_size + 1)

    # Calculate the Simple Moving Average (SMA)
    initial_mean = dataframe['close'].head(ema_size).mean()

    # Loop through each row of dataframe
    for i in range(len(dataframe)):
        # Set SMA
        if i == ema_size:
            dataframe.loc[i, ema_name] = initial_mean
        # If i is > ema_size set EMA
        elif i > ema_size:
            ema_value = dataframe.loc[i, 'close'] * multiplier + dataframe.loc[i-1, ema_name]*(1-multiplier)
            dataframe.loc[i, ema_name] = ema_value
        # Disregard rows 0 to ema_size-1
        else:
            dataframe.loc[i, ema_name] = 0.00
    # Return modified dataframe
    return dataframe

# Function to calculate a crossover event between two EMAs
def ema_cross_calc(dataframe, short_term_ema, long_term_ema):
    """
    Function to calculate an  event. 
    :param datafram: dataframe object
    :param ema_one: integer of EMA 1 size
    :param ema_two: integer of EMA 2 size
    :return: dataframe with cross events
    """
    # Get the column names
    ema_one_column = "ema_" + str(short_term_ema)
    ema_two_column = "ema_" + str(long_term_ema)

    # Creata a position column
    dataframe['position'] = dataframe[ema_one_column] > dataframe[ema_two_column]
    # Create a pre-position column
    dataframe['pre_position'] = dataframe['position'].shift(1)
    # Drop any N/A values => uses ".dropna"
    dataframe.dropna(inplace=True) 
    # Define crossover events => lambda function, needs two boolean values (ommitted from tutorial)
    dataframe['ema_cross'] = np.where(dataframe['position'] == dataframe['pre_position'],False,True)
    # Drop the position and pre_position columns => uses ".drop"
    dataframe = dataframe.drop(columns="position")
    dataframe = dataframe.drop(columns="pre_position")
    # return dataframe with  detected to the user
    return dataframe