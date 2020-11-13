import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class StockData():
	"""
	handles and operates on yahoo stock data (.csv)

	Attributes
	.filepath : str
		filepath to the source stock data .csv file used to initialize StockData
	.data : DataFrame
		dataframe containing the stock data, indexed by datetime string of format YYYY=MM-DD
	.selected_data : DataFrame
		dataframe ontaining the selected stock data, indexed by datetime string of format YYYY=MM-DD
	"""
	def __init__(self, filepath):
		"""
		initializes StockData object by parsing stock data .csv file into a dataframe
		(assumes 'Date' column exists and uses it for index),
		also checks and handles missing data

		Parameters
		filepath : str
			filepath to the stock data .csv file, can be relative or absolute

		Raises
		IOError :
			failed I/O operation, e.g: invalid filepath, fail to open .csv
		"""
		self.filepath = filepath
		self.data = pd.read_csv(filepath).set_index('Date')
		self.check_data()

	def check_data(self, overwrite=True):
		"""
		checks and handles missing data by filling in missing values by interpolation

		Parameters
		overwrite : bool (True)
			if True, overwrites original source stock data .csv file

		Returns
		self : StockData
		"""
		# function to fill in missing values
		# by averaging previous data and after (interpolation)
		self.data = self.data.interpolate()
		self.data.to_csv(self.filepath, index=overwrite)
		return self

	def get_data(self, start_date, end_date):
		"""
		returns a subset of the stock data from start_date to end_date inclusive

		Parameters
		start_date : str
			start date of stock data range, must be of format YYYY-MM-DD
		end_date : str
			end date of stokc data range, must be of format YYYY-MM-DD

		Returns:
		selected_data : DataFrame
			stock data dataframe indexed from specified start to end date inclusive

		Raises
		KeyError :
			data for this date does not exist
		AssertionError :
			selected range is empty
		"""
		self.selected_data = self.data[str(start_date):str(end_date)]
		return self.selected_data

	def get_period(self):
		"""
		returns a string tuple of the first and last index
		which make up the maximum period of StockData

		Returns
		period : (str, str)

		Raises
		TypeError :
			the return tuple is probably (nan, nan) because .csv is empty
		"""
		index = list(self.data.index)
		(first, last) = (index[0], index[-1])
		return (first, last)

	def _calculate_SMA(self, n, col='Close'):
		"""
		calculates simple moving average (SMA) and augments the stock dataframe
		with this SMA(n) data as a new column

		Parameters
		n : int
			the amount of stock data to use to calculate average
		col : str ('Close')
			the column head title of the values to use to calculate average

		Returns
		self : StockData
		"""
		col_head = f'SMA{n}'
		if col_head not in self.data.columns:
			sma = self.data[col].rolling(n).mean()
			self.data[f'SMA{n}'] = np.round(sma, 4)
			self.data.to_csv(self.filepath, index=True)
		return self

	def _calculate_crossover(self, SMA1, SMA2, col='Close'):
		"""
		calculates the crossover positions and values,
		augments the stock dataframe with 2 new columns
		'Sell' and 'Buy' containing the value at which SMA crossover happens

		Parameters
		SMA1 : str
			the first column head title containing the SMA values
		SMA2 : str
			the second column head title containing the SMA values
		col : str ('Close')
			the column head title whose values will copied into 'Buy' and 'Sell'
			columns to indicate crossovers had happen on that index

		Returns
		self : StockData

		Raises
		Exception :
			SMA1 and SMA2 provided are the same, they must be different
		"""
		if SMA1 < SMA2: signal = self.data[SMA1] - self.data[SMA2]
		elif SMA1 > SMA2: signal = self.data[SMA2] - self.data[SMA1]
		else: raise Exception(f"{SMA1} & {SMA2} provided are the same. They must be different SMA.")

		signal[signal > 0] = 1
		signal[signal <= 0] = 0
		diff = signal.diff()

		self.data['Sell'] = np.nan
		self.data['Buy'] = np.nan
		self.data.loc[diff.index[diff < 0], 'Sell'] = self.data.loc[diff.index[diff < 0], col]
		self.data.loc[diff.index[diff > 0], 'Buy'] = self.data.loc[diff.index[diff > 0], col]

		self.data.to_csv(self.filepath, index=True)
		return self

	def plot_graph(self, col_headers, style, ax, show=True):
		"""
		plots columns of selected values as line plot and/or columns of values
		as scatter plot as specified by style to an Axes object

		Parameters
		col_headers : [str, str, ...]
			a list containing column header names whose data are to be plotted
		style : [str, str, ...]
			a list of matplotlib built-in style strings to indicate whether to plot
			line or scatterplot and the colours corresponding to each value in
			col_headers (hence, must be same length)
		ax : Axes
			matplotlib axes object on which the plot will be drawn

		Raises
		AttributeError :
			self.selected_data has not been specified,
			call StockData.get_data(start, end) before plotting
		AssertionError :
			self.selected_data is empty, perhaps due to OOB or invalid range
		"""
		assert not self.selected_data.empty
		self.selected_data[col_headers].plot(style=style,
		                                     ax=ax,
		                                     grid=True,
		                                     x_compat=True,
		                                     linewidth=1)
		if show: plt.show()

	def calculate_SMA(self, n):
		"""
		calculates simple moving average (SMA) and augments the stock dataframe
		with this SMA(n) data as a new column

		Parameters
		n : int
			the amount of stock data to use to calculate average
		col : str ('Close')
			the column head title of the values to use to calculate average

		Returns
		self : StockData
		"""
		col_head = 'SMA' + str(n)
		df = self.data.reset_index()

		if col_head not in df.columns:
			# Extract full dataframe from the actual data
			# (to check if there is enough data for sma)
			dateList = self.data.index.values.tolist()
			returnList = []
			for date in dateList: # for date in dateList
			# find the index of date in the full data
				dateIndex = df[df["Date"]==date].index.values[0]
				if dateIndex < n: # if date index is less than n: append None
					returnList.append(np.nan)
				else:
					sum = 0
					for i in range(n):
						sum += df.iloc[dateIndex-i]["Close"]
					# append the SMA for each day to a list
					returnList.append(sum/n)

			self.data[col_head] = returnList
			print(self.data)
			self.data.to_csv(self.filepath, index=True)

		return self

	def calculate_crossover(self, SMAa, SMAb):
		"""
		calculates the crossover positions and values,
		augments the stock dataframe with 2 new columns
		'Sell' and 'Buy' containing the value at which SMA crossover happens

		Parameters
		SMA1 : str
			the first column head title containing the SMA values
		SMA2 : str
			the second column head title containing the SMA values
		col : str ('Close')
			the column head title whose values will copied into 'Buy' and 'Sell'
			columns to indicate crossovers had happen on that index

		Returns
		self : StockData

		Raises
		Exception :
			SMA1 and SMA2 provided are the same, they must be different
		"""
		col_head1 = 'Position'
		col_head2 = 'Signal'
		col_head3 = 'Buy'
		col_head4 = 'Sell'
		df = self.data

		# to ensure the correct number of elements in the loop
		SMAlist = self.data.index.values.tolist()
		# extracts the SMA from the specific column in self.data
		if SMAa < SMAb:
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

		# goes through every element
		for i in range(len(SMAlist)):
			if SMA1[i] > SMA2[i]: stockPosition.append(1)   # SMA1 above SMA2
			elif SMA1[i] < SMA2[i]: stockPosition.append(0) # SMA2 above SMA1
			# if the SMAs are equal, repeat the previous entry
			# because no crossover has occured yet
			elif SMA1[i] == SMA2[i]: stockPosition.append(stockPosition[i-1])
			else: stockPosition.append(np.nan) # if no data, leave blank

		# find the places where crossover occurs
		for j in range(len(stockPosition)):
			# 'shifts' the data one period to the right
			# to ensure crossovers are reflected on the correct date
			if j == 0: stockSignal.append(np.nan)
			# calculation for the crossover signals
			else: stockSignal.append(stockPosition[j] - stockPosition[j-1])


		for k in range(len(stockSignal)): # finding location of buy signals
			if stockSignal[k] == 1:
				value = self.data[SMAa].tolist()[k]
				buySignal.append(value)
			else: buySignal.append(np.nan) # if no signal leave blank

		for k in range(len(stockSignal)): # finding location of sell signals
			if stockSignal[k] == -1:
				value = self.data[SMAa].tolist()[k]
				sellSignal.append(value)
			else: sellSignal.append(np.nan) # if no signal leave blank

		self.data[col_head3] = buySignal
		self.data[col_head4] = sellSignal

		print(self.data)
		self.data.to_csv(self.filepath, index=True)
		return self

if __name__ == "__main__":
	# How working data looks like
	# raw = StockData("../data/GOOG2.csv")
	# selected = raw.get_data('2018-01-02', '2020-09-22')
	# print(selected)

	old = StockData("../data/C31.SI.csv")
	new = StockData("../data/GOOG.csv")

	new._calculate_SMA(15)
	new._calculate_SMA(50)
	new._calculate_crossover('SMA15', 'SMA50', 'SMA15')
	start, end = new.get_period()
	print(f'{start} to {end}')

	# new.calculate_SMA(15)
	# new.calculate_SMA(50)
	# new.calculate_SMA(50) # should not run again because data alr exists
	# new.calculate_crossover('SMA15', 'SMA50')

	selected = new.get_data(start, end)
	print(selected)
	fig, ax = plt.subplots()
	new.plot_graph(['Close', 'SMA15', 'SMA50','Sell','Buy'], ['k-','b-','c-','ro','yo'], ax=ax, show=False)
	plt.tight_layout()
	plt.show()
