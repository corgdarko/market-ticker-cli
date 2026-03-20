# Imports
import warnings
import yfinance as yf
import pandas as pd
import shutil
import time
from pathlib import Path
from datetime import datetime

# Ignore Warnings
warnings.filterwarnings("ignore", category=pd.errors.Pandas4Warning)

# FinGetToday BOX
def print_left_box(lines):
    max_length = max(len(line) for line in lines)

    top = "┌" + "─" * (max_length + 2) + "┐"
    bottom = "└" + "─" * (max_length + 2) + "┘"

    print(top)
    for line in lines:
        print(f"│ {line.ljust(max_length)} │")
    print(bottom)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

lines = [
    "Welcome to FinGetToday",
    now
]

print_left_box(lines)


# Ticker Info
your_ticker = ("This is the range of price in your ticker for today: ")
ticker_interest = input("Type a ticker symbol, like AAPL or TSLA: " )
print()
df = yf.download(ticker_interest, period="10d", interval="1d", progress=False)
formatted_df = df.copy()
for column in ["Open", "High", "Low", "Close"]:
    formatted_df[column] = formatted_df[column].map(lambda x: f"${x:,.2f}")

formatted_df["Volume"] = formatted_df["Volume"].map(lambda x: f"{x:,.0f}")
print(your_ticker)
print()
print(formatted_df.tail())
print()

next_ticker = input("Do you want to take a look to another ticker?: ")
if next_ticker in ["Yes", "y", "Y","yes"]:
    
    ticker_interest = input("Type a ticker symbol, like AAPL or TSLA: " )
    df = yf.download(ticker_interest, period="10d", interval="1d", progress=False)
    formatted_df = df.copy()
    for column in ["Open", "High", "Low", "Close"]:
        formatted_df[column] = formatted_df[column].map(lambda x: f"${x:,.2f}")

    formatted_df["Volume"] = formatted_df["Volume"].map(lambda x: f"{x:,.0f}")
    print(your_ticker)
    print(formatted_df.tail())
else: 
    print()
    def print_left_box(lines):
        max_length = max(len(line) for line in lines)

        top = "┌" + "─" * (max_length + 2) + "┐"
        bottom = "└" + "─" * (max_length + 2) + "┘"

        print(top)
        for line in lines:
            print(f"│ {line.ljust(max_length)} │")
            print(bottom)
    lines = [
        "Thanks for using FinGetToday, Goodbye!"
    ]

    print_left_box(lines)

    time.sleep(10)


    