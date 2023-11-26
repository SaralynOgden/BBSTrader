from mock import MagicMock, patch

import json
import pytest
import sys

sys.path.append("src")
from mt5_lib import connect

sys.modules['mt5'] = MagicMock()

settings = json.loads("""{
    "mt5": {
        "server": "MetaQuotes-Demo",
        "symbols": ["EURJPY"],
        "timeframe": 60000,
        "timeout" : 100
    }
}""")

credentials = json.loads("""{
    "mt5": {
        "login": 1,
        "password": "abc123",
        "terminal_pathway": "terminal64.exe",
        "server": "server"
    }
}""")

@patch('mt5_lib.mt5.login')
@patch('mt5_lib.mt5.initialize')
def test_connect_init_and_login_successful(mock_init, mock_login):
    mock_init.return_value = True
    mock_login.return_value = True
    connection_result = connect(settings, credentials)
    assert connection_result

@patch('mt5_lib.mt5.login')
@patch('mt5_lib.mt5.initialize')
def test_connect_init_unsucessful(mock_init, mock_login):
    with pytest.raises(ConnectionError):
        mock_init.return_value = False
        mock_login.return_value = True
        connect(settings, credentials)

@patch('mt5_lib.mt5.login')
@patch('mt5_lib.mt5.initialize')
def test_connect_login_errors(mock_init, mock_login):
    mock_init.return_value = True
    mock_login.side_effect = ConnectionError
    with pytest.raises(ConnectionError):
        connect(settings, credentials)

def test_connect_setting_value_missing():
    bad_settings = json.loads('{}')
    with pytest.raises(KeyError):
        connect(bad_settings, credentials)