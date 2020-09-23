import pandas as pd

class StockData():
	def __init__(self, filepath):
		self.data = pd.read_csv(filepath)

	def get_SMA15(self):
		return self

	def get_SMA50(self):
		return self

if __name__ == "__main__":
	print("hello world")
	x = StockData("../data/C31.SI.csv")
	print(x.data)
