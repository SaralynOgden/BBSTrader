# BBSTrader

## Setup
The following sections give an in-order overview on how to properly setup BBSTrader.

### Install Python
BBSTrader requires [Python](https://www.python.org/downloads/) version 3.6-3.10. Note: Python version 3.11 & 3.12 are not supported by MT5!

### Install MetaTrader 5
Currently, MetaTrader 5 supports the following platforms:
* Windows
* macOS *with XQuartz (windows shell for mac)
* Ubuntu/Debian Linux *using Wine (windows shell for Linux)

To choose your installation, click [here](https://www.metatrader5.com/en/download).

### Set your MT5 account credentials in Credentials.json
The following **credentials.json** fields must be set for BBSTrader to work:
* _server_--The server name on which trades will be made
* _terminal_pathway_--The file path to MetaTrader's **terminal64.exe**
* _login_--Your MetaTrader 5 login ID
* _password_--Your MetaTrader 5 password

### Modify Settings.json to adjust how you trade
The following **settings.json** fields must be set for BBSTrader to work:
* _timeframe_--The MetaTrader5 timeframe to use. If you are unsure what this is, learn more [here](https://myforex.com/en/mt5guide/change-timeframes.html).
The remaining fields may be updated to your liking:
* _symbols_--An array of valid MetaTrader5 trading symbols
* _timeout_--The number of milliseconds allocated to attempt connection establishment before timing out.

### Testing
Tests are located in the tests subdirectory. To run all of the tests in the terminal, run
```python -m pytest tests```
from the main directory. To run any individual test, run
```python -m pytest tests\<your test file>```
for more information, visit https://coverage.readthedocs.io/en/latest/cmd.html

Test coverage can and should be monitored. This can be done using the command
```python -m pytest tests --cov=.```
To view what lines are and are not covered, run
```python3 -m coverage html```
and view the results in your web broswer.
