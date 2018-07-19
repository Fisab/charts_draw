import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd

import indicators

import os
from matplotlib.gridspec import GridSpec

def update(path):
	df = pd.read_csv(path)

	df = indicators.moving_average(df, 15)
	df = indicators.exponential_moving_average(df, 30)
	df = indicators.relative_strength_index(df, 14)
	df = indicators.macd(df, 12, 26)

	# print(df)
	df = df.astype(float)

	f = lambda x: mdates.date2num(datetime.datetime.fromtimestamp(x))
	df['Date'] = df['Date'].apply(f)

	# print(df['Date'])
	return df

def draw(f1, ax, ax1, ax2, ax3, ohlc, zoom, pair, draw=False):
	width = 0.1
	width_bar = 0.015
	if zoom == 'day':
		width = 1/(24*60)*20
	elif zoom == 'week':
		width = 1/10
		width_bar = 0.1
	elif zoom == 'month':
		width = 1/2
		width_bar = 0.5

	candlestick_ohlc(ax, ohlc.values, width=width, colorup='green', colordown='red')
	ax1.bar(ohlc['Date'], ohlc['Volume'], width=width_bar)

	ax.plot(ohlc['Date'], ohlc['MA_15'], color='purple', label='MA_15')
	ax.plot(ohlc['Date'], ohlc['EMA_30'], color='blue', label='EMA_30')

	ax2.plot(ohlc['Date'], ohlc['RSI_14'], color='orange', label='RSI_14')
	ax2.plot(ohlc['Date'], [0.7]*len(ohlc['RSI_14']), color='red', label='RSI_14_sell')
	ax2.plot(ohlc['Date'], [0.3]*len(ohlc['RSI_14']), color='green', label='RSI_14_buy')

	ax3.plot(ohlc['Date'], ohlc['MACD_12_26'], color='brown', label='MACD_12_26')
	ax3.plot(ohlc['Date'], ohlc['MACDsign_12_26'], color='red', label='MACDsign_12_26')
	ax3.plot(ohlc['Date'], ohlc['MACDdiff_12_26'], color='blue', label='MACDdiff_12_26')

	f1.autofmt_xdate()

	ax.xaxis_date()
	ax1.xaxis_date()

	date_format = {
		'day': [mdates.HourLocator(), mdates.DateFormatter('%d %H:%M')],
		'week': [mdates.DayLocator(), mdates.DateFormatter('%d %H:%M')],
		'month': [mdates.DayLocator(), mdates.DateFormatter('%d.%m')]
	}

	for i in [ax3, ax2, ax1, ax]:
		i.xaxis.set_major_locator(date_format[zoom][0])
		i.xaxis.set_major_formatter(date_format[zoom][1])

		i.grid(True)
		if len(i.get_legend_handles_labels()[0]) > 0:
			i.legend()

	ax1.set_title('%s  %s' % (pair, zoom))
	plt.subplots_adjust(bottom=0.065, top=0.95, left=0.05, right=0.95)


	if draw == True:
		plt.show()

def create_images():
	os.system('python download_ohlc.py')

	fig = plt.figure('Charts', figsize =(16,8))

	ax1 = plt.subplot(6,1,1)
	ax2 = plt.subplot(6,1,2)
	ax3 = plt.subplot(6,1,3)
	ax = plt.subplot(2,1,2)

	intervals = ['day', 'week', 'month']
	pairs = ['BTC_USD', 'ETH_USD', 'LTC_USD', 'ETC_BTC', 'ZEC_BTC', 'LTC_BTC', 'ZEC_USD', 'ETH_BTC', 'XRP_BTC', 'XRP_USD']

	for pair in pairs:
		for interval in intervals:
			path = 'charts/%s/%s_%s.csv' % (pair, pair, interval)
			ohlc = update(path)

			for i in [ax, ax1, ax2, ax3]:
				i.cla()
			draw(fig, ax, ax1, ax2, ax3, ohlc, interval, pair)

			name = 'graphs/%s_%s.png' % (pair, interval)
			fig.savefig(name, bbox_inches='tight')



def main():
	os.system('python download_ohlc.py')
	fig = plt.figure('Charts', figsize =(16,8))

	ax1 = plt.subplot(6,1,1)
	ax2 = plt.subplot(6,1,2)
	ax3 = plt.subplot(6,1,3)
	ax = plt.subplot(2,1,2)

	pair = 'BTC_USD'
	interval = 'day'

	path = 'charts/%s/%s_%s.csv' % (pair, pair, interval)
	ohlc = update(path)

	draw(fig, ax, ax1, ax2, ax3, ohlc, interval, pair, draw=True)


create_images()
# main()