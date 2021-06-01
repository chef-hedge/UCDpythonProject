# Importing necessary packages

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt

# Import data and check for integrity

data_07_10 = pd.read_csv('Air_Traffic_Passenger_Statistics_07-10.csv')
data_17_20 = pd.read_csv('Air_Traffic_Passenger_Statistics_17-20.csv')

print(data_07_10.head(), data_17_20.head())
print(data_07_10.shape, data_17_20.shape)

