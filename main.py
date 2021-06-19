# Importing necessary packages
from zipfile import ZipFile
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

# Downloading and Importing dataset from Kaggle using API (zip)
api.dataset_download_files('olistbr/brazilian-ecommerce')

# Listing files contained in the dataset
zf = ZipFile('brazilian-ecommerce.zip')
print(zf.namelist())

# Extracting the necessary dataset files
zf.extract('olist_orders_dataset.csv')
zf.extract('olist_customers_dataset.csv')
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

# Exporting sliced Dataframe to CSV
olist_df_RJ.to_csv('olist_df_RJ.csv')

# For loop to list column names
for val in olist_df:
    print(val)

# Iterrows over olist_df to produce a meaningful description of order ID and its delivery location and status
for index, row in olist_df.iterrows():
    print('Status of Order ID ' + row['order_id'] + ', delivered to ' + row['customer_city']
          + ', ' + row['customer_state'] + ' = ' + row['order_status'])
    # adding a break to prevent for loop to run over the whole dataframe
    break

# Converting columns with dates to datetime data type to allow analysis of date and time
olist_df['order_purchase_timestamp'] = pd.to_datetime(olist_df['order_purchase_timestamp'])
olist_df['order_estimated_delivery_date'] = pd.to_datetime(olist_df['order_estimated_delivery_date'])

# Calculation of time between order and estimated delivery dates
olist_df['order_time_days'] = olist_df['order_estimated_delivery_date'] - olist_df['order_purchase_timestamp']

# Convert time between orders to weeks
olist_df['order_time_weeks'] = olist_df.order_time_days / np.timedelta64(1, 'W')

print(olist_df.head())
print(olist_df.dtypes)

# Creating lists from the city and state columns, and order status for easier visualisations
olist_citylist = olist_df['customer_city'].tolist()
print(Counter(olist_citylist))
olist_statelist = olist_df['customer_state'].tolist()
print(Counter(olist_statelist))
olist_statuslist = olist_df['order_status'].tolist()
print(Counter(olist_statuslist))

# Using numpy to calculate mean, median of time in weeks between order and estimated delivery dates
# mean value
mean = np.mean(olist_df['order_time_weeks'])
# median value
median = np.median(olist_df['order_time_weeks'])
print("Mean: ", mean)
print("Median: ", median)

# Plotting 'customer_state' variable in a bar chart
labels, values = zip(*Counter(olist_statelist).items())
indexes = np.arange(len(labels))
width = 1

plt.bar(indexes, values)
plt.xticks(indexes, labels)
plt.xlabel('State')
plt.ylabel('Number of Orders')
plt.title('Orders by State')
plt.show()

# Plotting average and median delivery time per state variable in a bar chart
# Grouping averages by state
olist_df_stateavg = olist_df.groupby(['customer_state'])['order_time_weeks'].mean().reset_index()

# Plotting bar chart
plt.bar(olist_df_stateavg['customer_state'], olist_df_stateavg['order_time_weeks'])
plt.xlabel('State')
plt.ylabel('Weeks')
plt.title('Order Time by State')
plt.show()

# Plotting same bar chart with horizontal lines to compare state and country means and country median
plt.bar(olist_df_stateavg['customer_state'], olist_df_stateavg['order_time_weeks'])
plt.axhline(y=3.395378560731207, color='r', linestyle='-', label='Country avg')
plt.axhline(y=3.32005291005291, color='y', linestyle='-', label='Country median')
plt.xlabel('State')
plt.ylabel('Weeks')
plt.yticks([0, 1, 2, 3, 3.32005291005291, 3.395378560731207, 4, 5, 6, 7])
plt.title('Order Time by State')
plt.legend()
plt.show()

# Ploting order status
labels, values = zip(*Counter(olist_statuslist).items())
indexes = np.arange(len(labels))

plt.bar(indexes, values)
plt.xticks(indexes, labels)
plt.xlabel('Status')
plt.ylabel('Number')
plt.title('Order Status')
plt.show()

# Filtering and undelivered orders using reusable function
def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


olist_statusundelivered = remove_values_from_list(olist_statuslist, 'delivered')

# Plotting undelivered orders
labels, values = zip(*Counter(olist_statusundelivered).items())
indexes = np.arange(len(labels))

plt.bar(indexes, values)
plt.xticks(indexes, labels)
plt.xlabel('Status')
plt.ylabel('Number')
plt.title('Order Status')
plt.show()