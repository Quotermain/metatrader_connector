import yfinance as yf
from sys import argv

def get_american_candles(ticker, period, interval):
	df = yf.Ticker(ticker).history(
		period=period, interval=interval
	)
	df.rename(columns={"Open": 'open', 'Close': 'close'}, inplace=True)
	return df

if __name__ == '__main__':
	ticker, period, interval = argv[1], argv[2], argv[3]
	print(get_american_candles(argv[1], argv[2], argv[3]))
