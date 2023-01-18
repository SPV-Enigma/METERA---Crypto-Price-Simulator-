# METERA---Crypto-Price-Simulator-


Crypto Price Simulator -

This script is a simple price simulator for a specified crypto asset using historical data from CoinGecko's API. The script retrieves the historical data, simulates future prices using a Monte Carlo method, and plots the results.

Usage -

Make sure you have Python3, requests, numpy, pandas, scipy, and matplotlib installed.
Replace "cardano" in line 9 with the crypto asset of your choice.
Replace 1460 in line 10 with the number of days of historical data you want to retrieve.
Run the script by typing python3 crypto_price_simulator.py in your command line.

Output -

The script will output two plots. The first plot shows the simulated prices for the specified number of simulations. The second plot shows the normal distribution of returns. The script also calculates the mean of the simulated prices and projects the price in a separate plot.

Note
This script is for educational and informational purposes only and should not be used for investment or financial advice. The author is not responsible for any investment or financial decisions made based on the output of this script.
