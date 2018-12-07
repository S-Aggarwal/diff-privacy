# import osmnx as ox
import pandas as pd
import os
import urllib.request
import io

class TaxiDataset:
	def __init__(self, location, coords, timestamps):
		self.location = location
		self.coords = coords
		self.timestamps = timestamps
	
def fetch_dataset(date='2016-01', location='manhattan'):
	"""
	Downloads and caches the NYC dataset for the given date.
	"""
	filename = 'yellow_tripdata_' + date + '.csv'
	filepath = 'data/' + location + '/' + filename
	
	if not os.path.exists(filepath):
		urllib.request.urlretrieve('https://s3.amazonaws.com/nyc-tlc/trip+data/' + filename, filepath)
	
	df = pd.read_csv(filepath, nrows=10, usecols=['tpep_pickup_datetime', 'pickup_longitude', 'pickup_latitude'])
	return TaxiDataset(location, zip(df['pickup_longitude'], df['pickup_latitude']), df['tpep_pickup_datetime'])
