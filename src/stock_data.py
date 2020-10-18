import numpy as np
import pandas as pd

class StockData():
	def __init__(self, filepath):
		self.filepath = filepath
		self.data = self.read_csv(filepath).set_index('Date')
		self.check_data()

	def read_csv(self, filepath):
		"""
		Given inputted csv filepath (str), parses csv into a dataframe and returns it
		Error handling:
		- Invalid filepath: raises exception
		"""
		try:
			return pd.read_csv(filepath)
		except IOError as e:
			raise Exception(e)

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

	def calculate_crossover(self):
		stock_position = []  # which SMA line is on top
		stock_signal = []  # the buy/sell signal --> the 1s and -1s
		for i in range(len(SMA1)):  # ensure the length of the list is the same as the SMA one
			if SMA1[i] > SMA2[i]:
				stock_position.append(1)  # SMA1 above SMA2
			elif SMA1[i] < SMA2[i]:
				stock_position.append(0)  # SMA2 above SMA1
			elif SMA1[i] == SMA2[i]:
				# if the SMAs are equal, repeat the previous entry
				stock_position.append(stock_position[i-1])
			else:
				stock_position.append('NA')

			for j in range(len(stock_position)):  # find the places where crossover occurs
				if j == 0:
					# 'shifts' the data one period to the right
					stock_signal.append('NA')
				else:
					# calculation for the crossover signals
					stock_signal.append(stock_position[j] - stock_position[j-1])

		return (stock_position, stock_signal)

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
	new.calculate_SMA(15)
	new.calculate_SMA(50)
	new.calculate_SMA(50)
	selected = new.get_data('2020-01-02', '2020-09-22')
	print(selected)
