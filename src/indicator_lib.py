import numpy

def calc_ema(dataframe, ema_size):
    """
    Calculates the Experimental Moving Average (EMA) of size `ema_size`
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