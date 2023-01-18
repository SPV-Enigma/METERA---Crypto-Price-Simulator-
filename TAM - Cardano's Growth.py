import requests
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

# Define the crypto asset you want to use
crypto_name = 'cardano'

# Define the number of days of historical data you want to retrieve
num_days = 1460

# Define the url for the API call
url = f"https://api.coingecko.com/api/v3/coins/{crypto_name}/market_chart?vs_currency=usd&days={num_days}"

# Make the API call and store the response
response = requests.get(url)
data = response.json()

# Extract the historical data from the response
prices = []
dates = []
for item in data["prices"]:
    prices.append(item[1])
    dates.append(item[0])

# Create a DataFrame with the historical data
df = pd.DataFrame({'date': dates, 'price': prices})

# Convert date to pandas datetime
df['date'] = pd.to_datetime(df['date'],unit='ms')
df = df.set_index('date')

# calculate daily returns
returns = df['price'].pct_change()

# calculate mean and standard deviation of returns
mean = returns.mean()
std = returns.std()

# number of simulations
num_sims = 100

# create an empty DataFrame to hold simulated prices
sim_prices = pd.DataFrame(index=range(len(returns)), columns=range(num_sims))
sim_prices.fillna(value=float('nan'), inplace=True)

# run the simulation
for i in range(num_sims):
    # generate a random normal distribution for returns
    rand_returns = np.random.normal(mean, std, len(returns))
    # create a temporary DataFrame to hold the new prices
    temp_prices = pd.DataFrame({'price': df['price'][0]}, index=[0])
    # simulate the prices
    for j in range(1, len(returns)):
        temp_prices = pd.concat([temp_prices, pd.DataFrame({'price': temp_prices.iloc[j-1]['price'] * (1 + rand_returns[j])}, index=[j])])
    # add the new prices to the sim_prices DataFrame
    sim_prices[i] = temp_prices['price']

# Plot the simulated prices
plt.figure(figsize=(10, 6))
for i in range(num_sims):
    plt.plot(sim_prices[i])
plt.xlabel('Days')
plt.ylabel('Price')
plt.show()

# Plot the normal distribution curve of returns
plt.figure()
plt.title("Normal Distribution of Returns")
plt.xlabel("Returns (%)")
plt.ylabel("Frequency (%)")
n, bins, patches = plt.hist(returns, bins=50, density=True, alpha=0.6, color='g',edgecolor='black')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mean, std)
plt.plot(x, p, 'k', linewidth=2)
plt.xlim(xmin, xmax)

# Adding percentages inside the bell curve
bin_centers = 0.5 * (bins[:-1] + bins[1:])
for c, p in zip(bin_centers, n):
    plt.gca().text(c, p, f'{p*100:0.1f}%', ha='center', va='bottom', fontsize=10)
plt.show()

# Calculate the mean of the simulated prices
mean_sim_prices = sim_prices.mean(axis=1)

# Plot the price projection
plt.figure(figsize=(10, 6))
plt.plot(mean_sim_prices)
plt.xlabel('Days')
plt.ylabel('Price')
plt.title('Price Projection')
plt.show()

# Calculate the standard deviation of the simulated prices
std_sim_prices = sim_prices.std(axis=1)

# Plot the price projection based on 1 standard deviation
plt.figure(figsize=(10, 6))
plt.plot(mean_sim_prices - std_sim_prices, label='Lower Bound')
plt.plot(mean_sim_prices + std_sim_prices, label='Upper Bound')
plt.xlabel('Days')
plt.ylabel('Price')
plt.title('Price Projection (1 Standard Deviation)')
plt.legend()
plt.show()