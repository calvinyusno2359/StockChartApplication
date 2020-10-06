import pandas as pd

class StockData():
	def __init__(self, filepath):
		self.data = self.read_csv(filepath).set_index('Date')
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

	def calculate_SMA(self, N):
		"""
		Given self.data and N, find the SMA(N) and augments self.data with the SMA data as new column
		"""
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
		pass

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
	raw = StockData("../data/GOOG2.csv")
	selected = raw.get_data('2018-01-02', '2020-09-22')
	print(raw.data)
	print(selected)
