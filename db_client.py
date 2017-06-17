from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

import pandas as pd

from influxdb import DataFrameClient


# InfluxDB connections settings
host = 'localhost'
port = 8086
user = 'root'
password = 'root'
dbname = 'mydb'

client = DataFrameClient(host, port, user, password, dbname)
constant_traffic_query = "SELECT * FROM \"network consumption with policy\" WHERE time >= '2017-06-16T10:13:32Z' and time < '2017-06-16T10:22:43Z';"
random_traffic_query = "SELECT * FROM \"network consumption with policy\" WHERE time >= '2017-06-17T02:02:00Z' and time < '2017-06-17T02:11:16Z';"

result = client.query(constant_traffic_query)
constant_result = result['network consumption with policy']
constant_result['Constant traffic'] = constant_result[['baseline', 'proportional']].apply(lambda row: (1.0 - (row['proportional']/row['baseline'])) * 100, axis=1)

result = client.query(random_traffic_query)
random_result = result['network consumption with policy'][:-1] #has one extra line at the end
random_result['Random traffic'] = random_result[['baseline', 'proportional']].apply(lambda row: (1.0 - (row['proportional']/row['baseline'])) * 100, axis=1)

# print constant_result[['savings_constant']]
# print random_result[['savings_random']]

result = constant_result
result['Random traffic'] = random_result['Random traffic'].values

print result[['Constant traffic', 'Random traffic']][:5]

result[['Constant traffic', 'Random traffic']].plot()
axes = plt.gca()
axes.grid(False)
plt.ylabel('Power Savings Potential (%)')
axes.set_ylim([0, 100])
plt.xlabel('Time')
plt.show()