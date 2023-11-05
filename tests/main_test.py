import json
import pytest
import sys

sys.path.append("../src")
from main import get_trader_settings, ACCOUNT_SETTINGS_PATH

correct_file_path = "../" + ACCOUNT_SETTINGS_PATH

def test_get_trader_settings_gets_file_data():
    with open(correct_file_path, "r", encoding="utf8") as file:
        json_settings = json.load(file)
        assert json_settings == get_trader_settings(correct_file_path)

def test_get_trader_settings_fails_when_no_file():
    file_path = 'setting.json'
    with pytest.raises(FileExistsError) as excinfo:
        get_trader_settings(file_path)
    assert str(excinfo.value) == f'Could not locate resource: {file_path}'