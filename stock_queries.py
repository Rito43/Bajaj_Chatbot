'''import pandas as pd


bfs = pd.read_csv("data/BFS_Daily_Closing_Price.csv", parse_dates=["Date"], dayfirst=True)
bfs.columns = bfs.columns.str.strip()  # Remove extra spaces in column names

# Clean 'Closing_Price' column: remove commas, strip spaces, convert to float
bfs["Closing_Price"] = (
    bfs["Closing_Price"]
    .astype(str)
    .str.replace(",", "")
    .str.strip()
    .astype(float)
)


sensex = pd.read_csv("data/Sensex_Daily_Historical_Data.csv", parse_dates=["Date"], dayfirst=True)
sensex.columns = sensex.columns.str.strip()  # Clean column names

# Clean 'Close' column (if needed)
sensex["Close"] = (
    sensex["Close"]
    .astype(str)
    .str.replace(",", "")
    .str.strip()
    .astype(float)
)


def get_price_stats(df, month_str):
    start = pd.to_datetime("01-" + month_str, format="%d-%b-%y")
    end = start + pd.offsets.MonthEnd(0)
    month_df = df[(df["Date"] >= start) & (df["Date"] <= end)]

    return {
        "highest": round(month_df["Closing_Price"].max(), 2),
        "lowest": round(month_df["Closing_Price"].min(), 2),
        "average": round(month_df["Closing_Price"].mean(), 2)
    }


def compare_returns(start_str, end_str):
    start = pd.to_datetime("01-" + start_str, format="%d-%b-%y")
    end = pd.to_datetime("01-" + end_str, format="%d-%b-%y") + pd.offsets.MonthEnd(0)

    bfs_range = bfs[(bfs["Date"] >= start) & (bfs["Date"] <= end)]
    sensex_range = sensex[(sensex["Date"] >= start) & (sensex["Date"] <= end)]

    bfs_return = (bfs_range["Closing_Price"].iloc[-1] - bfs_range["Closing_Price"].iloc[0]) / bfs_range["Closing_Price"].iloc[0] * 100
    sensex_return = (sensex_range["Close"].iloc[-1] - sensex_range["Close"].iloc[0]) / sensex_range["Close"].iloc[0] * 100

    return {
        "Bajaj Finserv Return (%)": round(bfs_return, 2),
        "Sensex Return (%)": round(sensex_return, 2)
    }'''



import pandas as pd
import re

# Load and clean Bajaj Finserv data
bfs = pd.read_csv("data/BFS_Daily_Closing_Price.csv", parse_dates=["Date"], dayfirst=True)
bfs.columns = bfs.columns.str.strip()
bfs["Closing_Price"] = bfs["Closing_Price"].astype(str).str.replace(",", "").str.strip().astype(float)

# Load and clean Sensex data
sensex = pd.read_csv("data/Sensex_Daily_Historical_Data.csv", parse_dates=["Date"], dayfirst=True)
sensex.columns = sensex.columns.str.strip()
sensex["Close"] = sensex["Close"].astype(str).str.replace(",", "").str.strip().astype(float)

# Helper: stats for 1 month
def get_price_stats(df, month_str):
    start = pd.to_datetime("01-" + month_str, format="%d-%b-%y")
    end = start + pd.offsets.MonthEnd(0)
    month_df = df[(df["Date"] >= start) & (df["Date"] <= end)]

    return {
        "highest": round(month_df["Closing_Price"].max(), 2),
        "lowest": round(month_df["Closing_Price"].min(), 2),
        "average": round(month_df["Closing_Price"].mean(), 2)
    }

# Helper: return % comparison
def compare_returns(start_str, end_str):
    start = pd.to_datetime("01-" + start_str, format="%d-%b-%y")
    end = pd.to_datetime("01-" + end_str, format="%d-%b-%y") + pd.offsets.MonthEnd(0)

    bfs_range = bfs[(bfs["Date"] >= start) & (bfs["Date"] <= end)]
    sensex_range = sensex[(sensex["Date"] >= start) & (sensex["Date"] <= end)]

    bfs_return = (bfs_range["Closing_Price"].iloc[-1] - bfs_range["Closing_Price"].iloc[0]) / bfs_range["Closing_Price"].iloc[0] * 100
    sensex_return = (sensex_range["Close"].iloc[-1] - sensex_range["Close"].iloc[0]) / sensex_range["Close"].iloc[0] * 100

    return {
        "Bajaj Finserv Return (%)": round(bfs_return, 2),
        "Sensex Return (%)": round(sensex_return, 2)
    }

# 🔍 Master function for chatbot
def answer_query(query: str) -> str:
    query = query.lower()

    # Handle price stats like "highest/lowest/average stock price in Jul-24"
    stats_match = re.search(r"(highest|lowest|average).+stock price.+?([a-z]{3}-\d{2})", query)
    if stats_match:
        kind = stats_match.group(1)
        month_str = stats_match.group(2).capitalize()
        stats = get_price_stats(bfs, month_str)
        return f"The {kind} stock price for Bajaj Finserv in {month_str} was ₹{stats[kind]}."

    # Handle compare returns like "compare bajaj finserv and sensex from Jul-23 to Jun-24"
    compare_match = re.search(r"compare.+from ([a-z]{3}-\d{2}) to ([a-z]{3}-\d{2})", query)
    if compare_match:
        start = compare_match.group(1).capitalize()
        end = compare_match.group(2).capitalize()
        returns = compare_returns(start, end)
        return (
            f"Between {start} and {end}:\n"
            f"- Bajaj Finserv Return: {returns['Bajaj Finserv Return (%)']}%\n"
            f"- Sensex Return: {returns['Sensex Return (%)']}%"
        )

    return "❓ Sorry, I couldn't understand your stock-related question."


