import yfinance as yf
from sys import argv

def get_american_candles(ticker):

	data_day = yf.Ticker(ticker).history(
		period='2d', interval='1d'
	)
	data_day.rename(columns={"Open": 'open', 'Close': 'close'}, inplace=True)

	data_5_min = yf.Ticker(ticker).history(
		period='10m', interval='5m'
	)
	data_5_min.rename(columns={"Open": 'open', 'Close': 'close'}, inplace=True)

	return data_day, data_5_min


if __name__ == '__main__':
	ticker = argv[1]
	print(get_american_candles(ticker)[0])
