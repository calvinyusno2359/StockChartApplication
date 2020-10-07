import pandas as pd
import numpy as np

class StockData():
	def __init__(self, filepath):
		self.data = self.read_csv(filepath).set_index('Date')
		self.dataraw = self.read_csv("../data/GOOG.csv")
		# self.check_data
		# self.calculate_SMA
		# self.calculate_crossover

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
		"""
		df = self.dataraw #Extract full dataframe from the actual data(to check if there is enough data for sma)
		dateList = self.data.index.values.tolist() #List of data in self dataframe
		returnList = []
		for date in dateList: #for date in dateList
			dateIndex = df[df["Date"]==date].index.values[0] # find the index of date in the full data
	#         print(dateIndex)
			if dateIndex < n: # if date index is less than n: append None
				returnList.append(np.nan)
			else:
				sum = 0
				for i in range(n):
					sum += df.iloc[dateIndex-i]["Adj Close"]#else sum of data from dateIndex to dateIndex-i(0,1,2...n)
				returnList.append(sum/n)  #append the SMA for each day to a list
		self.data['SMA' + str(n)] = returnList
		print(self.data)
		return self #returnlist

	def get_data(self, start_date, end_date):
		"""
		Given start_date and end_date objects, return the corresponding slice of self.data

		Error handling:
		- end_date < start_date: selects none
		- date out of bounds on either side: selects up to max available data on the side that is oob
		"""
		self.selected_data = self.data[str(start_date):str(end_date)]
		return self.selected_data


	def check_data(self, filename):
		# df = self.dataraw
		nData = self.data.reset_index()
		newData = nData.interpolate() #function to fill in naan with average with the one previous and after data
		newData.to_csv(filename, index=False) #overwrite old csv with new clean data csv
		return newData
		

	def calculate_crossover(self):
		pass

	def get_period(self):
		"""
		Returns first and last index which make up the maximum period of stock data
		"""
		index = list(self.data.index)
		(first, last) = (index[0], index[-1])
		return (first, last)

if __name__ == "__main__":
	# raw = StockData("../data/GOOG2.csv")
	# selected = raw.get_data('2018-01-02', '2020-09-22')
	# newDataf = raw.check_data("../data/GOOG.csv")
	new = StockData("../data/GOOG.csv")
	print(new.check_data("../data/GOOG.csv"))
	new2 = StockData("../data/GOOG.csv")
	# print(new2)
	new2.calculate_SMA(15)
	new2.calculate_SMA(50)
	new2.calculate_SMA(50)
	# print(raw.data)
	# print(selected)
	# print(raw.check_data("../data/GOOG.csv"))

