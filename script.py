import requests
import os
import openai
import csv
from dotenv import load_dotenv
import snowflake.connector
from datetime import datetime

def run_stock_job():
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        print("API_KEY is not set. Please add it to your .env or environment variables.")
        raise SystemExit(1)

    LIMIT = 1000
    DS = '2025-10-04'
# convert DS string to a date object for Snowflake DATE column
    ds_date = datetime.strptime(DS, "%Y-%m-%d").date()
    url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"
    response = requests.get(url)
    if not response.ok:
        print(f"Initial request failed: {response.status_code} {response.text[:200]}")
        raise SystemExit(1)

    tickers = []

    try:
        data = response.json()
    except ValueError:
        print("Failed to parse JSON from initial response")
        raise SystemExit(1)

    for ticker in data.get('results', []):
        tickers.append(ticker)

    while data.get('next_url'):
        print('requesting next page', data['next_url'])
        resp = requests.get(data['next_url'] + f'&apiKey={API_KEY}')
        if not resp.ok:
            print(f"Next page request failed: {resp.status_code} {resp.text[:200]}")
            break
        try:
            data = resp.json()
        except ValueError:
            print("Failed to parse JSON from paginated response")
            break
        for ticker in data.get('results', []):
            tickers.append(ticker)

    print(f"Collected {len(tickers)} tickers")

    # Build rows to insert
    rows = []
    for t in tickers:
        rows.append((
            t.get("ticker", ""),
            t.get("name", ""),
            t.get("market", ""),
            t.get("locale", ""),
            t.get("primary_exchange", ""),
            t.get("type", ""),
            "true" if t.get("active") else "false",
            t.get("currency_name", ""),
            t.get("cik", ""),
            t.get("composite_figi", ""),
            t.get("share_class_figi", ""),
            t.get("last_updated_utc", ""),
            ds_date
        ))

    # Snowflake connection settings - must be set in environment
    SF_USER = os.getenv("SNOWFLAKE_USER")
    SF_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SF_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SF_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SF_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
    SF_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    SF_ROLE = os.getenv("SNOWFLAKE_ROLE")

    missing = [k for k,v in {
        "SNOWFLAKE_USER":SF_USER,
        "SNOWFLAKE_PASSWORD":SF_PASSWORD,
        "SNOWFLAKE_ACCOUNT":SF_ACCOUNT,
        "SNOWFLAKE_WAREHOUSE":SF_WAREHOUSE,
        "SNOWFLAKE_DATABASE":SF_DATABASE,
    }.items() if not v]
    if missing:
        print("Missing Snowflake environment variables:", ", ".join(missing))
        print("Set them and re-run the script. Example (Windows cmd):")
        print(r'setx SNOWFLAKE_USER jgmeher && setx SNOWFLAKE_PASSWORD "your_password" && setx SNOWFLAKE_ACCOUNT "your_account" && setx SNOWFLAKE_WAREHOUSE "COMPUTE_WH" && setx SNOWFLAKE_DATABASE "MYDB"')
        raise SystemExit(1)

    conn = None
    cur = None
    total_inserted = 0
    table_ident = None
    try:
        conn = snowflake.connector.connect(
            user=SF_USER,
            password=SF_PASSWORD,
            account=SF_ACCOUNT,
            warehouse=SF_WAREHOUSE,
            database=SF_DATABASE,
            schema=SF_SCHEMA,
            role=SF_ROLE,
        )
        cur = conn.cursor()

        # Create table if not exists
        table_ident = f'"{SF_DATABASE}"."{SF_SCHEMA}"."STOCK_TICKERS"'
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_ident} (
                TICKER VARCHAR,
                NAME VARCHAR,
                MARKET VARCHAR,
                LOCALE VARCHAR,
                PRIMARY_EXCHANGE VARCHAR,
                TYPE VARCHAR,
                ACTIVE VARCHAR,
                CURRENCY_NAME VARCHAR,
                CIK VARCHAR,
                composite_figi VARCHAR,
                share_class_figi VARCHAR,
                LAST_UPDATED_UTC VARCHAR,
                DS VARCHAR
            )
        """)

        # Insert in batches
        insert_sql = f"INSERT INTO {table_ident} (TICKER, NAME, MARKET, LOCALE, PRIMARY_EXCHANGE, TYPE, ACTIVE, CURRENCY_NAME, CIK, COMPOSITE_FIGI, SHARE_CLASS_FIGI, LAST_UPDATED_UTC, DS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        table_ident = f'"{SF_DATABASE}"."{SF_SCHEMA}"."STOCK_TICKERS"'
        batch_size = 1000
        total_inserted = 0
        for i in range(0, len(rows), batch_size):
            chunk = rows[i:i+batch_size]
            cur.executemany(insert_sql, chunk)
            total_inserted += len(chunk)
            print(f"Inserted {total_inserted}/{len(rows)}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    print(f"Wrote {total_inserted} rows to Snowflake table {table_ident}")

if __name__ == "__main__":
    run_stock_job()