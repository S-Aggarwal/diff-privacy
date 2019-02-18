from collections import defaultdict
from urllib import request
import pandas as pd
import utm
from tqdm import tqdm

import os

tqdm.pandas()   # Set-up tqdm for pandas

def to_utm(long, lat):
    x, y, _, _ = utm.from_latlon(lat, long)
    return x, y


date = '2016-01'
location = 'manhattan'
filename = 'yellow_tripdata_' + date + '.csv'
# filename = 'test2.csv'
filepath = 'data/' + location + '/' + filename

if not os.path.exists(filepath):
    print("File doesn't exist locally, re-downloading...")
    request.urlretrieve('https://s3.amazonaws.com/nyc-tlc/trip+data/' + filename, filepath)

df = pd.read_csv(filepath,
                 usecols=['tpep_pickup_datetime', 'pickup_longitude', 'pickup_latitude',
                          'dropoff_longitude', 'dropoff_latitude', 'tpep_dropoff_datetime'])

print('Read complete')

df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], errors='coerce', infer_datetime_format=True)
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], errors='coerce', infer_datetime_format=True)
df = df.dropna()

buckets = defaultdict(list)

for _, row in tqdm(df.iterrows()):
    # Pickup
    b = str(row['tpep_pickup_datetime'])[:13].replace(' ', '-')
    x, y = to_utm(row['pickup_longitude'], row['pickup_latitude'])
    buckets[b].append((x, y))

    # Dropoff
    b = str(row['tpep_dropoff_datetime'])[:13].replace(' ', '-')
    x, y = to_utm(row['dropoff_longitude'], row['dropoff_latitude'])
    buckets[b].append((x, y))


for bucket, points in tqdm(buckets.items()):
    with open('data/manhattan/processed/' + date + '/' + bucket + '.txt', 'w') as f:
        f.writelines(map(lambda p: str(p[0]) + ' ' + str(p[1]) + '\n', points))
