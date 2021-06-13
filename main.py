# Importing necessary packages
from zipfile import ZipFile
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
from urllib.request import urlretrieve
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

# Downloading and Importing dataset from Kaggle using API (zip)
api.dataset_download_files('olistbr/brazilian-ecommerce')

# Extracting dataset zip file
zf = ZipFile('brazilian-ecommerce.zip')
zf.extractall()
zf.close()

# Reading necessary files into DataFrames and printing its head and shape check data is valid
orders_df = pd.read_csv('olist_orders_dataset.csv')
customers_df = pd.read_csv('olist_customers_dataset.csv')

print(orders_df.head(), customers_df.head())
print(orders_df.shape, customers_df.shape)

# Setting and sorting index of both dataframes to the files to use when merging/joining: customer_id
orders_df_indsort = orders_df.set_index('customer_id').sort_index()
customers_df_indsort = customers_df.set_index('customer_id').sort_index()

# Merging both dataframes into one: olist_df
olist_df = orders_df_indsort.merge(customers_df_indsort, on='customer_id')

# Checking for missing and duplicate values
# Printing count of missing values and duplicate rows to verify
olist_df_missing = pd.isnull(olist_df).sum()
olist_df_duplicates = olist_df.duplicated().sum()

print(olist_df_missing)
print(olist_df_duplicates)

# Replacing missing values
olist_df = olist_df.fillna('Not Available')

# Slicing data, customers from the state of Rio de Janeiro (RJ)
olist_df_RJ = olist_df.loc[olist_df['customer_state'] == 'RJ']

# For loop to list column names
for val in olist_df:
    print(val)

# Reset index in case visualisation errors
# olist_df = olist_df.reset_index()
# print(olist_df.head())

# Iterrows over olist_df to produce a meaningful description of order ID and its delivery location and status
for index, row in olist_df.iterrows():
    print('Status of Order ID ' + row['order_id'] + ', delivered to ' + row['customer_city']
          + ', ' + row['customer_state'] + ' = ' + row['order_status'])
    # adding a break to prevent for loop to run over the whole dataframe (prevent memory issues)
    break

#
