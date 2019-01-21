import matplotlib
import osmnx as ox
import pandas as pd
import os
import urllib.request
import io

class TaxiDataset:
	def __init__(self, location, coords, timestamps):
		self.location = location
		self.coords = coords
		self.timestamps = timestamps
	
def fetch_taxi_dataset(location='manhattan', date='2016-01'):
	"""
	Downloads and caches the taxi dataset for the given location (and date for NYC).
	"""
	filename = 'yellow_tripdata_' + date + '.csv'
	filepath = 'data/' + location + '/' + filename
	
	if not os.path.exists(filepath):
		urllib.request.urlretrieve('https://s3.amazonaws.com/nyc-tlc/trip+data/' + filename, filepath)
	
	df = pd.read_csv(filepath, nrows=10, usecols=['tpep_pickup_datetime', 'pickup_longitude', 'pickup_latitude'])
	return TaxiDataset(location, zip(df['pickup_longitude'], df['pickup_latitude']), df['tpep_pickup_datetime'])


def fetch_osm_map(location="manhattan"):
	"""
	Downloads and caches the OSM street graph for the given location
	"""

	raw_graph = ox.graph_from_place("Manhattan, New York, USA", network_type='drive')
	ox.plot_graph(raw_graph)

fetch_osm_map()
