import requests
import csv
from datetime import datetime, timedelta

# Set up the Twelve Data API URL and parameters
twelve_data_url = 'https://api.twelvedata.com/time_series'
twelve_data_params = {
    'apikey': 'abbf0261b03c472ca47601471aa9ddd0',  # Replace with your Twelve Data API Key
}

# Define the available currency pairs
currency_pairs = [
    ('USD', 'EUR'),
    ('USD', 'JPY'),
    ('USD', 'GBP'),
    ('USD', 'CZK'),
    # Add other currency pairs here as desired
]

# Prompt the user to select a currency pair
print("Select a currency pair:")
for i, pair in enumerate(currency_pairs):
    print(f"{i+1}: {pair[0]}/{pair[1]}")
pair_choice = int(input("> ")) - 1
currency_pair = currency_pairs[pair_choice]

# Prompt the user to select a time interval
print("Select a time interval:")
print("1: Minutes")
print("2: Hours")
print("3: Days")
time_choice = int(input("> "))

# Set the appropriate function and time interval parameters based on user input
if time_choice == 1:
    twelve_data_params['interval'] = '1min'
elif time_choice == 2:
    twelve_data_params['interval'] = '1h'
elif time_choice == 3:
    twelve_data_params['interval'] = '1day'

# Prompt the user to enter the number of data points to retrieve
data_points = int(input("Enter the number of data points to retrieve: "))

# Set currency pair and data type parameters
twelve_data_params['symbol'] = f"{currency_pair[0]}/{currency_pair[1]}"
twelve_data_params['outputsize'] = data_points

response = requests.get(twelve_data_url, params=twelve_data_params).json()
data = []

time_format = '%Y-%m-%d %H:%M:%S'

raw_data = [(datetime.strptime(entry['datetime'], time_format), entry) for entry in response['values']]

for date, fx_data in raw_data:
    data.append([
        date.strftime(time_format),
        fx_data['open'],
        fx_data['high'],
        fx_data['low'],
        fx_data['close']
    ])

# Save the forex data to a CSV file
with open('forex_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'Open', 'High', 'Low', 'Close'])
    writer.writerows(data)

print(f"Saved {data_points} data points to forex_data.csv")
