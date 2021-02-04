import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

ticker = 'MOEX.MM'
symbol_info = mt5.symbol_info(ticker)
point = symbol_info.point
price = symbol_info.ask

print(symbol_info)
