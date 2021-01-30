from mysql.connector import connect

ALL_TICKERS = ['MTSS.MM',
 'AFLT.MM', 'OGKB.MM', 'MGNT.MM', 'TATN.MM',  'MTLR.MM', 'ALRS.MM', 'SBER.MM',
 'MOEX.MM', 'HYDR.MM', 'ROSN.MM', 'LKOH.MM', 'SIBN.MM', 'GMKN.MM', 'RTKM.MM',
 'SNGS.MM', 'CHMF.MM', 'VTBR.MM', 'NVTK.MM', 'GAZP.MM', 'YNDX.MM', 'NLMK.MM',
 'FIVE.MM', 'SBER_p.MM', 'SNGS_p.MM', 'BTCUSD', 'ETHUSD', 'EURUSD', 'USDJPY',
 'GBPUSD', 'USDRUB', 'AUDUSD', 'NZDUSD', 'USDHKD', 'USDSGD', 'USDMXN', 'USDZAR',
 'USDCNH', 'USDCAD', 'USDCHF', 'AAPL', 'BA', 'AMZN', 'NVDA', 'FB', 'MSFT', 'MCD',
 'TGT', 'V', 'TWTR', 'INTC', 'GOOG', 'T', 'XOM', 'PFE', 'DIS', 'WMT', 'AMD', 'NFLX',
 'MU', 'MA', 'ATVI', 'NKE', 'CSCO', 'PYPL', 'GE', 'NEM', 'QCOM', 'SBUX', 'ADBE',
 'KO', 'KHC', 'CAT', 'BIIB', 'ABBV', 'EA', 'NEE', 'JNJ', 'CRM', 'UNH', 'FDX',
 'BMY', 'CVX', 'HPQ', 'AVGO', 'DAL', 'PG', 'F', 'GM', 'IBM']

CRIDENTIALS = {
    'host': '192.168.0.100', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}

for ticker in ALL_TICKERS:
    connection = connect(**CRIDENTIALS)
    query = f'INSERT INTO is_signal_sent_mt5 (ticker, is_sent) VALUES ("{ticker}", 0)'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
