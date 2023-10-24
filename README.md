# BBSTrader

## Setup
The following sections give an in-order overview on how to properly setup BBSTrader.

### Install MetaTrader 5
Currently, MetaTrader 5 supports the following platforms:
* Windows
* macOS
* Ubuntu/Debian Linux
* iOS
* Android
To choose your installation, click [here](https://www.metatrader5.com/en/download).

### Configure Settings.json
The following **settings.json** fields must be set for BBSTrader to work:
* _login_--Your MetaTrader 5 login ID
* _password_--Your MetaTrader 5 password
* _server_--The server name on which trades will be made
* _terminal_pathway_--The file path to MetaTrader's **terminal64.exe**

The remaining fields may be updated to your liking:
* _symbols_--An array of valid MetaTrader5 trading symbols
* _timeframe_--The number of milliseconds allocated to attempt connection establishment before timing out.
