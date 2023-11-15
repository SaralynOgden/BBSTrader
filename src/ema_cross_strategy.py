import indicator_lib
import mt5_lib
import make_trade as mt

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

    trade_event = ema_x_strategy_table.tail(1).copy()

    if trade_event['ema_cross'].values:
        new_trade = True
        comment = f"EMA_Cross_strategy_{symbol}"
        print(comment)
        make_trade_outcome = mt.make_trade(balance, comment, risk_pct, symbol, trade_event['take_profit'].values, trade_event['stop_price'].values, trade_event['stop_loss'].values)
    else:
        make_trade_outcome = False

    return make_trade_outcome

# Function to calculate the indicators for this strategy
def calculate_indicators(ema_x_strategy_table, short_term_ema_length, long_term_ema_length):
    """
    Function to calculate the indicators for the EMA Cross strategy
    :param ema_x_strategy_table: dataframe which holds candle raw data and ema calculations
    :param short_term_ema_length: length of the short-term ema
    :param long_term_ema_length: length of the long-term ema
    """

    # Calculate and add a column for the short-term EMA
    indicator_lib.calc_ema(ema_x_strategy_table, short_term_ema_length)

    # Calculate and add a column for the long-term ema
    indicator_lib.calc_ema(ema_x_strategy_table, long_term_ema_length)

    # Calculate and add a column for the EMA Cross
    indicator_lib.ema_cross_calc(ema_x_strategy_table, short_term_ema_length, long_term_ema_length)
