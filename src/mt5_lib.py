"""MetaTrader5 API import"""
import MetaTrader5 as mt5


def connect(json_settings: dict) -> bool:
    """
    Attempts to initialize and log into MetaTrader5.

    :param json_settings: A dict containing MetaTrader5
    login details.
    :returns bool: True if initialization and login succeeds.
    Otherwise, false.
    """
    try:
        pathway = json_settings["mt5"]["terminal_pathway"]
        login = json_settings["mt5"]["login"]
        password = json_settings["mt5"]["password"]
        server = json_settings["mt5"]["server"]
        timeout = json_settings["mt5"]["timeframe"]

        initialized = mt5.initialize(
            pathway, login=login, password=password, server=server, timeout=timeout
        )
        if not initialized:
            raise ConnectionError

        # Safe to login here. Returns true if login succeeds. Otherwise, returns false.
        return mt5.login(login=login, password=password, server=server, timeout=timeout)

    except KeyError as e:
        print(f"The queried dictionary key does not exist: {e.args}")
        raise e
    except ConnectionError as e:
        print(f"Could not connect to MetaTrader5: {e.args}")
        raise e


def disconnect():
    """
    Close the previously established connection to the MetaTrader 5 terminal.
    """
    mt5.shutdown()
