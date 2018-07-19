# HOVER_STATE = 'hover',
# SELECT_STATE = 'select',
# MILLISECOND = 'millisecond',
# SECOND = 'second',
# MINUTE = 'minute',
# HOUR = 'hour',
# DAY = 'day',
# WEEK = 'week',
# MONTH = 'month',
# YEAR = 'year',

#https://exmo.com/ctrl/chartMain?&period=second&para=BTC_USD

import requests
from time import sleep

import os
import datetime

intervals = ['day', 'week', 'month']

pairs = ['BTC_USD', 'ETH_USD', 'LTC_USD', 'ETC_BTC', 'ZEC_BTC', 'LTC_BTC', 'ZEC_USD', 'ETH_BTC', 'XRP_BTC', 'XRP_USD']

for pair in pairs:
	if not os.path.exists('charts/' + pair):
		os.makedirs('charts/' + pair)

def remove_files(path):
	for the_file in os.listdir(path):
		file_path = os.path.join(path, the_file)
		if os.path.isfile(file_path):
			os.unlink(file_path)

def write(pair, interval, data):
	fname = '%s_%s.csv' % (pair, interval)
	if fname in os.listdir('charts/' + pair):
		file_r = open('charts/' + pair + '/' + fname, 'r').read()
		file_r = file_r.split('\n' + str(int(data[0][0]/1000)))[0]
		for i in data:
			if not str(int(i[0]/1000)) in file_r:
				file_r += '\n%s,%f,%f,%f,%f,%f' % (str(int(i[0]/1000)), i[1], i[2], i[3], i[4], i[5])
		file = open('charts/' + pair + '/' + fname, 'w')
		file.write(file_r)
		file.close()
	else:
		file = open('charts/' + pair + '/' + fname, 'w')
		data_csv = ''
		data_csv += 'Date,Open,High,Low,Close,Volume'

		# data_csv += 'Open,High,Low,Close,Volume\n'
		for i in data:
			# date = datetime.datetime.fromtimestamp(i[0]/1000)	
			#data, open, high, low, close date.strftime("%d/%m/%y %H:%M")
			data_csv += '\n%s,%f,%f,%f,%f,%f' % (str(int(i[0]/1000)), i[1], i[2], i[3], i[4], i[5])
			# data_csv += '%f,%f,%f,%f\n' % (i[1], i[2], i[3], i[4])
		file.write(data_csv)
		file.close()


while True:
	for pair in pairs:
		# remove_files(pair + '/')
		for interval in intervals:
			print(pair, interval)
			params = (
				('period', interval),
				('para', pair),
			)
			url = 'https://exmo.me/ctrl/chartMain'
			raw_data = requests.get(url, params=params).json()
			data = raw_data['data']['price']
			for i in data:
				for j in raw_data['data']['amount']:
					if i[0] == j[0]:
						i.append(j[1])
			write(pair, interval, data)
			sleep(1)
	print('-'*30)
	break
	sleep(30)

#https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&limit=2000&aggregate=3&e=exmo
#histohour histominute