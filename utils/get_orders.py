import MetaTrader5 as mt5
import pandas as pd

def get_orders():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    orders = mt5.orders_get()
    print(orders)
    if orders is None:
        return None
    else:
        orders = pd.DataFrame(
            list(orders), columns=orders[0]._asdict().keys()
        )
        return orders

if __name__ == '__main__':
    print(get_orders())
