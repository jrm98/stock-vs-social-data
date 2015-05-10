

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg
import urllib2, time, threading, tweets
from bs4 import BeautifulSoup

# favorites
favorites = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

csv_map = {'AAPL':'apple', 'GOOG':'google', 'MSFT':'microsoft', 'AMZN':'amazon'}

# load symbols from a static file
# sym = pd.read_csv('data/companylist.csv')
# symbols = sym['Symbol'].tolist()

# fig = plt.figure()
# ax = fig.add_axes( (0.15, 0.3, 0.75, 0.65) )


for sym in favorites:
	url = "https://finance.yahoo.com/q/hp?s="+sym+"+Historical+Prices"
	url += "&a=00&b=22&c=2015&d=03&e=26&f=2015&g=d" # specifies date

	response = urllib2.urlopen(url).read()

	soup = BeautifulSoup(response)

	table = soup.findAll('table',{'class':'yfnc_datamodoutline1'})[0]
	table = table.tr.td.table

	# gathers and cleans header data
	headers = []
	for h in table.findAll('tr')[0].findAll('th'):
		txt = h.text
		punc = '.,:;"\'-!?*\n '
		for p in punc:
		    txt = txt.replace(p,'')
		headers.append(txt)


	# gathers the table data into a matrix
	length = len(table.findAll('td', {'class':'yfnc_tabledata1', 'align':'right'}))/len(headers)
	data = [[0 for x in range(len(headers))] for y in range(length)]
	i = 0
	j = 0
	for r in table.findAll('tr'):
		for d in r.findAll('td', {'class':'yfnc_tabledata1', 'align':'right'}):
			# if number of columns doesn't match, then skip the row
			if len(r.findAll('td', {'class':'yfnc_tabledata1', 'align':'right'})) <\
			len(headers):
				continue
			# print d.text
			txt = d.text.replace(',','')
			if j == 0:
				data[i][j] = txt
			elif j == 5:
				data[i][j] = int(txt)
			else:
				data[i][j] = float(txt)
			j = (j+1) % len(headers)
			if j == 0:
				i += 1


	# data.insert(0, headers)

	# creates various informative df's/series's
	df = pd.DataFrame(data, columns=headers)
	rev = df.iloc[::-1]
	diff = rev[['AdjClose']].diff()
	pct_chg = pd.DataFrame((diff['AdjClose'] / rev['AdjClose']) *100, columns=['AdjClose'])
	plt.plot(range(len(df['AdjClose'])), pct_chg['AdjClose'], label=sym)

	# gets tweet data that has been collected for the user accounts below
	traders = ['bkfViking123', 'Burns277', 'investorslive', 'markflowchatter', 'mbusigin', 'OptionsHawk', 'STT2318', 'Super_Trades', 'SZAman']
	tfreq = tweets.tweet_freq(traders, 65, [sym.lower(),csv_map[sym].lower()])
	# scaling to price data
	tfreq = np.array(tfreq).astype(float)
	tfreq = (((tfreq - min(tfreq))/max(tfreq))) * pct_chg['AdjClose'].max()
	# plots frequency of tweets mentioning given keywords
	plt.plot(range(65), tfreq, label='tweet freq for '+sym+' and '+csv_map[sym])

	# plotting search trends
	st1 = pd.read_csv('trends/report_'+csv_map[sym]+'.csv')
	st1[[csv_map[sym]]] = st1[[csv_map[sym]]].astype(float)
	st2 = pd.read_csv('trends/report_'+sym+'.csv')
	st2[[sym.lower()]] = st2[[sym.lower()]].astype(float)
	# making sure trend data is same length as prices data
	if len(st1) > len(df['AdjClose']):
		st1 = pd.DataFrame(st1.iloc[len(st1) - len(df['AdjClose']):,:])
	if len(st2) > len(df['AdjClose']):
		st2 = pd.DataFrame(st2.iloc[len(st2) - len(df['AdjClose']):,:])
	# combines company name trend and symbol trend
	st = st1[csv_map[sym]] + st2[sym.lower()]
	# scaling the trend data to be comparable to price data
	st = (((st - st.min())/st.max())**2) * pct_chg['AdjClose'].max()
	plt.plot(range(len(df['AdjClose'])), st, label=csv_map[sym]+' search trend')
	# creates line for y=0
	plt.plot(range(len(df['AdjClose'])), [0 for x in range(len(df['AdjClose']))], 'k--')

	plt.title('%% Change in Closing Prices & Social Interest Trends Over %d Days' % len(df['AdjClose']))
	plt.xlabel('day')
	plt.ylabel('% change in price')
	plt.legend(loc='best', fancybox=True, framealpha=0.5)
	plt.show()



# old plots commented out below, compared different stock prices

# # creates line for y=0
# plt.plot(range(len(df['AdjClose'])), [0 for x in range(len(df['AdjClose']))], 'k--')

# plt.title('%% Change of Closing Prices Over the Last %d Days' % len(df['AdjClose']))
# plt.xlabel('day')
# plt.ylabel('% change in price')
# plt.legend(loc='best', fancybox=True, framealpha=0.5)
# plt.show()
