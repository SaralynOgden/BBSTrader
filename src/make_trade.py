import mt5_lib as trader
import helper_functions as hf

def make_trade(balance, comment, risk_pct, symbol, take_profit, stop_loss, stop_price):
    """
    Makes a MT5 trade.

    :param balance    : Float. Trade balance
    :param comment    : String. Used for managing multi-algorithmic trading
    :param risk_pct   : Float. Risk amount as a percentage
    :param symbol     : String. Symbol name
    :param take_profit: Float. Take profit value
    :param stop_loss  : Float. Stop loss value
    :param stop_price : Float. Stop price value
    :return           : Boolean. True if trade made successfully. Otherwise, false
    """

    # Get proper types and format
    balance = (round(float(balance), 2))
    take_profit = (round(float(take_profit), 2))
    stop_loss = (round(float(stop_loss), 2))
    stop_price = (round(float(stop_price), 2))

    # Get lot size
    lot_size = hf.calc_lot_size(balance, risk_pct, stop_loss, stop_price, symbol)

    # Determine trade type
    (trade_type := "BUY_STOP") if stop_price > stop_loss else (trade_type := "SELL_STOP")

    # Send trade
    trade_outcome = trader.place_order(trade_type, symbol, lot_size, stop_loss, take_profit, comment, stop_price, False)

    return trade_outcome

    