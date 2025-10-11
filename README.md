# 📈 Stock Tickers ETL Pipeline  

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Polygon.io](https://img.shields.io/badge/API-Polygon.io-orange.svg)](https://polygon.io/)  

A simple **Python ETL pipeline** that retrieves all active U.S. stock tickers from the [Polygon.io API](https://polygon.io), processes the data, and stores it in a structured CSV file.  

---

## 🚀 Features  
🔄 Handles pagination until all stock tickers are retrieved

📊 Extracts key metadata: ticker, name, market, type, exchange, etc.

🧩 Uses dotenv for secure API and Snowflake credentials

❄️ Loads directly into Snowflake (creates table automatically if missing)

📅 Adds a daily partition column DS for data versioning

🧱 Modular code — can be integrated into Airflow or AWS Lambda

---

## 📂 Project Structure  
```
.
├── script.py        # Main ETL pipeline script
├── tickers.csv      # Output file (generated after running script)
├── .env             # Stores API_KEY (not committed to Git)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

## ⚙️ Setup  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/stock-tickers-pipeline.git
   cd stock-tickers-pipeline
   ```

2. **Create a virtual environment (optional but recommended)**  
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Polygon.io API key**  
   - Create a `.env` file in the project root  
   - Add:  
     ```
     API_KEY=your_polygon_api_key_here
     ```

---

## ▶️ Running the Script  

python script.py
```

This will:  
✅ Fetches all active stock tickers from Polygon.io
✅ Prints progress for each page of results
✅ Writes clean structured data into your Snowflake table:

---

## 📊 Sample Output 

requesting next page https://api.polygon.io/v3/reference/tickers?cursor=...
Inserted 1000/16000
Inserted 2000/16000
Wrote 16000 rows to Snowflake table "MYDB"."PUBLIC"."STOCK_TICKERS"

```

