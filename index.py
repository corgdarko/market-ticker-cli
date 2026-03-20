# Imports
import warnings
import time
import colorama
import mplfinance as mpf
from colorama import Fore, Style
from pathlib import Path
from datetime import datetime

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Ignore warnings
warnings.filterwarnings("ignore", category=pd.errors.Pandas4Warning)


# ---------- UI ----------
def print_left_box(lines):
    max_length = max(len(line) for line in lines)
    top = "┌" + "─" * (max_length + 2) + "┐"
    bottom = "└" + "─" * (max_length + 2) + "┘"

    print(top)
    for line in lines:
        print(f"│ {line.ljust(max_length)} │")
    print(bottom)


# ---------- Data ----------
def download_ticker_data(ticker_symbol):
    df = yf.download(
        ticker_symbol,
        period="10d",
        interval="1d",
        progress=False,
        multi_level_index=False
    )
    return df


def format_display_table(raw_df):
    display_df = raw_df.copy()

    display_df["Date"] = pd.to_datetime(display_df["Date"]).dt.strftime("%Y-%m-%d")

    for column in ["Open", "High", "Low", "Close"]:
        display_df[column] = display_df[column].map(lambda x: f"${x:,.2f}")

    display_df["Volume"] = display_df["Volume"].map(lambda x: f"{x:,.0f}")

    return display_df


def get_trend_signal(raw_df):
    trend_df = raw_df.copy()
    trend_df["SMA_5"] = trend_df["Close"].rolling(5).mean()

    last_close = trend_df["Close"].iloc[-1]
    last_sma_5 = trend_df["SMA_5"].iloc[-1]

    if pd.isna(last_sma_5):
        return "Not enough data to determine trend", trend_df

    if last_close > last_sma_5:
        return "Bullish short-term trend", trend_df
    elif last_close < last_sma_5:
        return "Bearish short-term trend", trend_df
    else:
        return "Neutral trend", trend_df


def save_excel_and_chart(ticker_symbol, raw_df, display_df, trend_df):
    output_folder = Path.cwd() / "fingettoday_output"

    if output_folder.exists() and not output_folder.is_dir():
        raise ValueError(f"{output_folder} exists but is not a folder.")

    output_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    excel_path = output_folder / f"{ticker_symbol}_report_{timestamp}.xlsx"
    chart_path = output_folder / f"{ticker_symbol}_chart_{timestamp}.png"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        raw_df.to_excel(writer, sheet_name="Raw_Data", index=False)
        display_df.to_excel(writer, sheet_name="Formatted_Data", index=False)
        trend_df.to_excel(writer, sheet_name="Trend_Data", index=False)

    candle_df = raw_df.copy()
    candle_df["Date"] = pd.to_datetime(candle_df["Date"])
    candle_df = candle_df.set_index("Date")

    mpf.plot(
        candle_df,
        type="candle",
        mav=(5,),
        volume=True,
        style="yahoo",
        title=f"{ticker_symbol} Candlestick Chart",
        ylabel="Price (USD)",
        ylabel_lower="Volume",
        savefig=str(chart_path)
    )

    return excel_path, chart_path



def lookup_ticker():
    ticker_interest = input("Type a ticker symbol, like AAPL or TSLA: ").strip().upper()
    print()

    if not ticker_interest:
        print("You did not enter a ticker symbol.")
        print()
        return

    raw_df = download_ticker_data(ticker_interest)

    if raw_df.empty:
        print("No data found for that ticker.")
        print()
        return

    raw_df = raw_df.reset_index()
    raw_df = raw_df[["Date", "Close", "High", "Low", "Open", "Volume"]]

    display_df = format_display_table(raw_df)

    print("This is the range of price in your ticker for today:")
    print()
    print(display_df.tail(5).to_string(index=False))
    print()

    trend_message, trend_df = get_trend_signal(raw_df)
    print(f"Trend signal: {trend_message}")
    print()

    excel_path, chart_path = save_excel_and_chart(
        ticker_interest,
        raw_df,
        display_df,
        trend_df
    )

    print(Fore.GREEN + f"Excel file saved to: {excel_path}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Chart saved to: {chart_path}" + Style.RESET_ALL)
    print()


# ---------- Main ----------
def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "Welcome to FinGetToday",
        now
    ]

    print_left_box(lines)
    print()

    while True:
        lookup_ticker()

        next_ticker = input("Do you want to look up another ticker? (yes/no): ").strip().lower()
        print()

        if next_ticker not in ["yes", "y"]:
            goodbye_lines = [
                "Thanks for using FinGetToday, goodbye!"
            ]
            print_left_box(goodbye_lines)
            time.sleep(10)
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\nSomething went wrong:")
        print(type(e).__name__, "-", e)
        input("\nPress Enter to exit...")