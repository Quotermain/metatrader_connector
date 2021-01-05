import MetaTrader5 as mt5
import pandas as pd

def get_positions():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    positions = mt5.positions_get()
    if positions is None:
        return None
    else:
        positions = pd.DataFrame(
            list(positions), columns=positions[0]._asdict().keys()
        )
        return positions

if __name__ == '__main__':
    print(get_positions())
