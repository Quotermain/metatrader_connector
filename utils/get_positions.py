import MetaTrader5 as mt5
import pandas as pd
import sys

LOGIN_DATA = {
    'login': 3073999, 'password': 'n8ghotnw',
    'server': 'Just2Trade-MT5'
}

def get_positions(ticker):
    if not mt5.initialize(**LOGIN_DATA):
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    positions = mt5.positions_get(symbol=ticker)
    if (positions is None) or (len(positions) == 0):
        return None
    else:
        positions = pd.DataFrame(
            list(positions), columns=positions[0]._asdict().keys()
        )
        return positions

if __name__ == '__main__':
    ticker = sys.argv[1]
    print(get_positions(ticker))
