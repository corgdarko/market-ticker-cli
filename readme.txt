# FinGetToday

A Python CLI tool that fetches recent market data from Yahoo Finance, formats it for terminal display, exports reports to Excel, and generates candlestick charts for quick trend visualization.

## Features

- Fetches recent historical market data from Yahoo Finance
- Accepts ticker input from the user in the terminal
- Displays recent price data in a clean table
- Formats prices in USD
- Formats volume with thousand separators
- Exports data to Excel with multiple sheets
- Generates candlestick charts with volume
- Includes a simple short-term trend signal using a 5-day moving average
- Allows repeated ticker lookups in one session

## Tech Stack

- Python
- yfinance
- pandas
- mplfinance
- matplotlib
- openpyxl
- colorama

## Project Structure

```text
FinGetToday/
├── index.py
├── requirements.txt
├── README.md
├── .gitignore
└── fingettoday_output/

The program displays a welcome box with the current date and time

The user enters a ticker symbol such as AAPL, TSLA, or ASTS

The app downloads the latest 10 days of market data

The data is formatted for terminal display

A simple trend signal is calculated using a 5-day moving average

The app saves:

an Excel report

a candlestick chart image

The user can choose to look up another ticker

Excel Output

Each run saves an Excel file inside the fingettoday_output folder.

The Excel report includes these sheets:

Raw_Data — original downloaded market data

Formatted_Data — cleaned and formatted version for readability

Trend_Data — data used for simple trend analysis