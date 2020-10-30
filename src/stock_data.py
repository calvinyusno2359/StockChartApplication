import numpy as np
import pandas as pd

class StockData():
	"""
	handles and operates on yahoo stock data (.csv)

	Attributes
	.filepath : str
		filepath to the source stock data .csv file used to initialize StockData
	.data : DataFrame
		dataframe containing the stock data, indexed by datetime objects

	Methods
	"""
	def __init__(self, filepath):
		"""
		initializes StockData object by parsing stock data .csv file

		Parameters
		filepath : str
			filepath to the stock data .csv file, can be relative or absolute
		"""
		self.filepath = filepath
		self.data = self.read_csv(filepath)
		self.check_data()

	def read_csv(self, filepath):
		"""
		parses .csv stock data file into a dataframe, assumes first column are dates

		Parameters
		filepath : str
			filepath to the stock data .csv file, can be relative or absolute

		Returns
		data : DataFrame
			stock data dataframe indexed by dates

		Raises
		IOError :
			failed I/O operation, e.g: invalid filepath
		"""
		try: return pd.read_csv(filepath, index_col=0, parse_dates=True)
		except IOError as e: raise Exception(e)

	def calculate_SMA(self, n):
		"""
		Given self.data and N, find the SMA(N) and augments self.data with the SMA data as new column
		if SMA data already exists, do nothing
		"""
		col_head = 'SMA' + str(n)
		df = self.data.reset_index()

		if col_head not in df.columns:
			#Extract full dataframe from the actual data(to check if there is enough data for sma)
			dateList = self.data.index.values.tolist() #List of data in self dataframe
			returnList = []
			for date in dateList: #for date in dateList
				dateIndex = df[df["Date"]==date].index.values[0] # find the index of date in the full data
				if dateIndex < n: # if date index is less than n: append None
					returnList.append(np.nan)
				else:
					sum = 0
					for i in range(n):
						sum += df.iloc[dateIndex-i]["Adj Close"]
						# else sum of data from dateIndex to dateIndex-i(0,1,2...n)
					returnList.append(sum/n)  #append the SMA for each day to a list

			self.data[col_head] = returnList
			print(self.data)
			self.data.to_csv(self.filepath, index=True)

		return self

	def get_data(self, start_date, end_date):
		"""
		Given start_date and end_date objects, return the corresponding slice of self.data

		Error handling:
		- end_date < start_date: selects none
		- date out of bounds on either side: selects up to max available data on the side that is oob
		"""
		self.selected_data = self.data[str(start_date):str(end_date)]
		return self.selected_data

	def check_data(self):
		self.data.reset_index()
		# function to fill in naan with average with the one previous and after data
		self.data = self.data.interpolate()
		# overwrite old csv with new clean data csv
		self.data.to_csv(self.filepath, index=True)
		return self

	def calculate_crossover(self, SMAa, SMAb):

		col_head1 = 'Position'
		col_head2 = 'Signal'
		col_head3 = 'Buy'
		col_head4 = 'Sell'
		df = self.data

		SMAlist = self.data.index.values.tolist() # to ensure the correct number of elements in the loop
		if SMAa < SMAb: # extracts the SMA from the specific column in self.data where SMA data will be
			SMA1 = df[SMAa].tolist()
			SMA2 = df[SMAb].tolist()
		elif SMAa > SMAb:
			SMA1 = df[SMAb].tolist()
			SMA2 = df[SMAa].tolist()
		else: # SMAa == SMAb
			raise ValueError(f"Given {SMAa} & {SMAb} are the same. Must be different SMA.")

		stockPosition = []  # which SMA line is on top
		stockSignal = []  	# the buy/sell signal --> the 1s and -1s
		buySignal = []  		# filtered out location of buy signals
		sellSignal = []  		# filtered out location of sell signals

		for i in range(len(SMAlist)):  # goes through every element in the SMA values
			if SMA1[i] > SMA2[i]: stockPosition.append(1)  		# SMA1 above SMA2
			elif SMA1[i] < SMA2[i]: stockPosition.append(0)  	# SMA2 above SMA1
			elif SMA1[i] == SMA2[i]: stockPosition.append(stockPosition[i-1]) # if the SMAs are equal, repeat the previous entry because no crossover has occured yet
			else: stockPosition.append(np.nan) #if no data, leave blank

		for j in range(len(stockPosition)):  			# find the places where crossover occurs
			if j == 0: stockSignal.append(np.nan) 	# 'shifts' the data one period to the right to ensure crossovers are reflected on the correct date
			else: stockSignal.append(stockPosition[j] - stockPosition[j-1]) # calculation for the crossover signals

		for k in range(len(stockSignal)): # finding location of buy signals
			if stockSignal[k] == 1:
				value = (self.data[SMAa].tolist()[k] + self.data[SMAb].tolist()[k]) / 2
				buySignal.append(value) # adds '1' at the location of buy signals in a separate column
			else: buySignal.append(np.nan) # if no signal leave blank

		for k in range(len(stockSignal)): #finding location of sell signals
			if stockSignal[k] == -1:
				value = (self.data[SMAa].tolist()[k] + self.data[SMAb].tolist()[k]) / 2
				sellSignal.append(value) # adds '-1' at the location of sell signals in a separate column
			else: sellSignal.append(np.nan) # if no signal leave blank

		# self.data[col_head1] = stockPosition
		# self.data[col_head2] = stockSignal
		self.data[col_head3] = buySignal
		self.data[col_head4] = sellSignal

		print(self.data)
		self.data.to_csv(self.filepath, index=True)
		return self

	def get_period(self):
		"""
		Returns first and last index which make up the maximum period of stock data
		"""
		index = list(self.data.index)
		(first, last) = (index[0], index[-1])
		return (first, last)

if __name__ == "__main__":
	# How working data looks like
	# raw = StockData("../data/GOOG2.csv")
	# selected = raw.get_data('2018-01-02', '2020-09-22')
	# print(selected)

	old = StockData("../data/C31.SI.csv")
	new = StockData("../data/GOOG.csv")
	print(new.data)
	# new.calculate_SMA(15)
	# new.calculate_SMA(50)
	# new.calculate_SMA(50) # should not run again because data alr exists
	# new.calculate_crossover('SMA15', 'SMA50')
	# selected = new.get_data('2020-01-02', '2020-09-22')
	# print(selected)
