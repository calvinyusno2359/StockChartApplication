import pandas as pd

class StockData():
	def __init__(self, filepath):
		self.data = self.read_csv(filepath)

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
		return self

if __name__ == "__main__":
	x = StockData("../data/C31.SI.csv")
	print(x.data)
