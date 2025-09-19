import requests
import os
import openai
import csv
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("API_KEY is not set. Please add it to your .env or environment variables.")
    raise SystemExit(1)

print(API_KEY)


LIMIT = 1000

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"
response = requests.get(url)
tickers = []


data = response.json()
for ticker in data['results']:
    tickers.append(ticker)

while 'next_url' in data:
    print('requesting next page', data['next_url'])
    response = requests.get(data['next_url'] + f'&apiKey={API_KEY}')
    data = response.json()

    if 'results' not in data:
        print('no results in response, stopping')
        break

    for ticker in data['results']:
        tickers.append(ticker)

print(len(tickers))

fieldnames = [
    "ticker",
    "name",
    "market",
    "locale",
    "primary_exchange",
    "type",
    "active",
    "currency_name",
    "cik",
    "last_updated_utc",
]

out_path = os.path.join(os.path.dirname(__file__), "tickers.csv")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for t in tickers:
        row = {
            "ticker": t.get("ticker", ""),
            "name": t.get("name", ""),
            "market": t.get("market", ""),
            "locale": t.get("locale", ""),
            "primary_exchange": t.get("primary_exchange", ""),
            "type": t.get("type", ""),
            # convert Python boolean to lowercase true/false to match example
            "active": "true" if t.get("active") else "false",
            "currency_name": t.get("currency_name", ""),
            "cik": t.get("cik", ""),
            "last_updated_utc": t.get("last_updated_utc", ""),
        }
        writer.writerow(row)

print(f"Wrote {len(tickers)} rows to {out_path}")