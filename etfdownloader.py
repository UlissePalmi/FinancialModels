import yfinance as yf
import pandas as pd
import numpy as np

# ---------------------------
# Parameters
# ---------------------------
start_date = "1998-01-01"
end_date = None  # defaults to today

sector_etfs = {
    "Energy": "XLE",
    "Materials": "XLB",
    "Industrials": "XLI",
    "Consumer Discretionary": "XLY",
    "Consumer Staples": "XLP",
    "Health Care": "XLV",
    "Financials": "XLF",
    "Information Technology": "XLK",
    "Utilities": "XLU",
    "Communication Services": "XLC",
    "Real Estate": "XLRE"
}

# ---------------------------
# Download adjusted prices
# ---------------------------
tickers = list(sector_etfs.values())

prices = yf.download(
    tickers,
    start=start_date,
    end=end_date,
    auto_adjust=True,   # total return (dividends included)
    progress=False
)["Close"]

# ---------------------------
# Convert to annual returns
# ---------------------------
year_end_prices = prices.resample("Y").last()
annual_returns = year_end_prices.pct_change()

# Use calendar year labels
annual_returns.index = annual_returns.index.year

# Rename columns to sector names
annual_returns = annual_returns.rename(
    columns={v: k for k, v in sector_etfs.items()}
)

# Drop first year (no prior year for return calc)
annual_returns = annual_returns.dropna(how="all")

# ---------------------------
# Optional: save output
# ---------------------------
annual_returns.to_csv("gics_sector_returns_etf_proxy.csv")

print(annual_returns.head())
