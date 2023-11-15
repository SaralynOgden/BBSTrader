import numpy as np
import utils

def calc_ema(ema_x_strategy_table, ema_size):
    """
    Calculates the Exponential Moving Average (EMA) of size `ema_size`
    for each entry in `dataframe`

    :param `ema_x_strategy_table`: The table which holds the raw data and ema strategy calculations
    :param `ema_size`: The EMA size
    """
    # Column name to append to dataframe
    ema_name = utils.get_ema_name(ema_size)

    # Create EMA multiplier
    multiplier = 2/(ema_size + 1)

    # Calculate the Simple Moving Average (SMA)
    initial_mean = ema_x_strategy_table['close'].head(ema_size).mean()

    # Loop through each row of dataframe
    for i in range(len(ema_x_strategy_table)):
        # Set SMA
        if i == ema_size:
            ema_x_strategy_table.loc[i, ema_name] = initial_mean
        # If i is > ema_size set EMA
        elif i > ema_size:
            ema_value = ema_x_strategy_table.loc[i, 'close'] * multiplier + ema_x_strategy_table.loc[i - 1, ema_name]*(1 - multiplier)
            ema_x_strategy_table.loc[i, ema_name] = ema_value
        # Disregard rows 0 to ema_size-1
        else:
            ema_x_strategy_table.loc[i, ema_name] = 0.00

# Function to calculate a crossover event between two EMAs
def ema_cross_calc(ema_x_strategy_table, short_term_ema_length, long_term_ema_length):
    """
    Function to calculate an  event. 
    :param `ema_x_strategy_table`: The table which holds the raw data and ema strategy calculations
    :param short_term_ema: length of short-term ema
    :param long_term_ema: length of long-term ema
    """
    # Get the column names
    short_term_ema_column = utils.get_ema_name(short_term_ema_length)
    long_term_ema_column = utils.get_ema_name(long_term_ema_length)

    # Creata a position column
    ema_x_strategy_table['position'] = ema_x_strategy_table[short_term_ema_column] > ema_x_strategy_table[long_term_ema_column]

    # Create a pre-position column
    ema_x_strategy_table['pre_position'] = ema_x_strategy_table['position'].shift(1)

    # Drop any N/A values => uses ".dropna"
    ema_x_strategy_table.dropna(inplace=True)
    
    # Define crossover events => lambda function, needs two boolean values (ommitted from tutorial)
    ema_x_strategy_table['ema_cross'] = np.where(ema_x_strategy_table['position'] == ema_x_strategy_table['pre_position'], False, True)
    # Drop the position and pre_position columns => uses ".drop"
    ema_x_strategy_table.drop(columns="position", inplace=True)
    ema_x_strategy_table.drop(columns="pre_position", inplace=True)