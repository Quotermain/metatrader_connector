from utils.get_positions import get_positions
import MetaTrader5 as mt5
from time import sleep
from utils.send_transaction import send_transaction

def check_and_close_position():

    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    positions = get_positions()
    if (positions is None) or (len(positions) == 0):
        return
    for _, position in positions.iterrows():
        symbol = position.symbol
        volume = position.volume
        type = position.type

        if type == 0:
            result = send_transaction(symbol, volume, 'sell')
        elif type == 1:
            result = send_transaction(symbol, volume, 'buy')

        print(symbol, result)

if __name__ == '__main__':
    while True:
        check_and_close_position()
        #sleep(2)
