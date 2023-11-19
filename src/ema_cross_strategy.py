import indicator_lib
import mt5_lib
import make_trade as mt
import utils

def ema_cross_strategy(symbol, timeframe, short_term_ema_length, long_term_ema_length, balance, risk_pct):
    """
    Function which runs the EMA Cross Strategy
    :param symbol: string of the symbol to be queried
    :param timeframe: string of the timeframe to be queried
    :param short_term_ema_length: integer of the lowest timeframe length for EMA
    :param long_term_ema_length: intefer of the highest timeframe length for EMA
    :return table with raw candle data and ema calculations
    """

    # Get vanilla MetaTrader 5 dataframe
    ema_x_strategy_table = mt5_lib.get_candlesticks(symbol, timeframe, 1000)

    # Append indicator columns to dataframe
    calculate_indicators(ema_x_strategy_table, short_term_ema_length, long_term_ema_length)

    det_trade(ema_x_strategy_table, short_term_ema_length, long_term_ema_length)

    trade_event = ema_x_strategy_table.tail(1).copy()

    if trade_event['ema_cross'].values:
        comment = f"EMA_Cross_strategy_{symbol}"
        make_trade_outcome = mt.make_trade(balance, comment, risk_pct, symbol, trade_event['take_profit'].values, trade_event['stop_price'].values, trade_event['stop_loss'].values)
    else:
        make_trade_outcome = False

    return make_trade_outcome

# Function to determine on which symbols trade events should occur and calculate their trade signals
def det_trade(ema_x_strategy_table, short_term_ema_length, long_term_ema_length):
    """
    Function to calculate a trade signals for symbols that saw their ema cross
    :param ema_x_strategy_table: dataframe in which we are calculating the cross strategy
    :param short_term_ema_length: integer of the lowest timeframe length for EMA
    :param long_term_ema_length: intefer of the highest timeframe length for EMA
    """

    if (long_term_ema_length <= short_term_ema_length):
        raise ValueError("Long-term EMA length must be larger than short-term EMA length")

    # Stop-loss is always the ema with the longer timeframe
    stop_loss_column_name = utils.get_ema_name(long_term_ema_length)

    min_value = long_term_ema_length

    ema_x_strategy_table['stop_loss'] = 0.0
    ema_x_strategy_table['stop_price'] = 0.0
    ema_x_strategy_table['take_profit'] = 0.0

    for i in range(min_value + 1, len(ema_x_strategy_table)):
        if ema_x_strategy_table.loc[i, 'ema_cross']:
            stop_loss = ema_x_strategy_table.loc[i, stop_loss_column_name]

            # Green candle (BUY)
            if ema_x_strategy_table.loc[i, 'open'] < ema_x_strategy_table.loc[i, 'close']:
                stop_price = ema_x_strategy_table.loc[i, 'high']
                distance = stop_price - stop_loss
                take_profit = stop_price + distance
            # Red candle (SELL)
            elif ema_x_strategy_table.loc[i, 'open'] > ema_x_strategy_table.loc[i, 'close']:
                stop_price = ema_x_strategy_table.loc[i, 'low']
                distance = stop_loss - stop_price
                take_profit = stop_price - distance

            ema_x_strategy_table.loc[i, 'stop_loss'] = stop_loss
            ema_x_strategy_table.loc[i, 'stop_price'] = stop_price
            ema_x_strategy_table.loc[i, 'take_profit'] = take_profit

# Function to calculate the indicators for this strategy
def calculate_indicators(ema_x_strategy_table, short_term_ema_length, long_term_ema_length):
    """
    Function to calculate the indicators for the EMA Cross strategy
    :param ema_x_strategy_table: dataframe in which we are calculating the cross strategy
    :param short_term_ema_length: length of the short-term ema
    :param long_term_ema_length: length of the long-term ema
    """

    # Calculate and add a column for the short-term EMA
    indicator_lib.calc_ema(ema_x_strategy_table, short_term_ema_length)

    # Calculate and add a column for the long-term ema
    indicator_lib.calc_ema(ema_x_strategy_table, long_term_ema_length)

    # Calculate and add a column for the EMA Cross
    indicator_lib.ema_cross_calc(ema_x_strategy_table, short_term_ema_length, long_term_ema_length)
