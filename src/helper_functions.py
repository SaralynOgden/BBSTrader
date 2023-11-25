def calc_lot_size(balance, risk_pct, stop_loss, stop_price, symbol):
    """
    Calculates the lot size (volume) for `symbol`

    :param balance   : Float.  The investment balance
    :param risk_pct  : Float.  The amount to risk as a percentage
    :param stop_loss : Float.  The losing exit price
    :param stop_price: Float.  The gaining exit price
    :param symbol    : String. The symbol name
    """

    # Get actual risk
    currency_risk = balance * risk_pct

    # Format `symbol`
    symbol_name = symbol.split(".")[0]

    if symbol_name == "USDJPY":

        # Known constant. More info: https://www.investopedia.com/terms/p/pip.asp#:~:text=In%20this%20case%2C%20the%20value,The%20pip%20value%20is%20%241.
        pip_size = 0.01

        pip_risk = abs((stop_price - stop_loss) / pip_size)
        pip_value = currency_risk / pip_risk * stop_price

        raw_lot_size = pip_value / 1000
    
    elif symbol_name == "USDCAD":
        pip_size = 0.0001

        pip_risk = abs((stop_price - stop_loss) / pip_size)
        pip_value = currency_risk / pip_risk * stop_price

        raw_lot_size = pip_value / 1000

    else:
        pip_size = 0.0001

        pip_risk = abs((stop_price - stop_loss) / pip_size)
        pip_value = currency_risk / pip_risk

        raw_lot_size = pip_value / 1000

    lot_size = float(raw_lot_size)
    lot_size = round(lot_size, 2)

    if lot_size >= 10:
        lot_size = 9.99
    elif lot_size < 1.0:
        lot_size = 1.0
    return lot_size