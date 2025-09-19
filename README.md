# 📈 Stock Tickers ETL Pipeline  

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Polygon.io](https://img.shields.io/badge/API-Polygon.io-orange.svg)](https://polygon.io/)  

A simple **Python ETL pipeline** that retrieves all active U.S. stock tickers from the [Polygon.io API](https://polygon.io), processes the data, and stores it in a structured CSV file.  

---

## 🚀 Features  
- 🔄 Handles **pagination** until all tickers are retrieved  
- 📊 Extracts essential fields like `ticker`, `name`, `market`, `primary_exchange`, `type`  
- 💾 Outputs a clean **CSV file (`tickers.csv`)** for further analysis  

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
   source .venv/bin/activate   # Mac/Linux
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
✅ Fetch all active stock tickers  
✅ Print progress as it requests pages  
✅ Save results into `tickers.csv`  

---

## 📊 Sample Output (`tickers.csv`)  

```csv
ticker,name,market,locale,primary_exchange,type,active,currency_name,cik,last_updated_utc
AAPL,Apple Inc,stocks,us,XNAS,CS,true,USD,0000320193,2023-09-19T00:00:00Z
MSFT,Microsoft Corp,stocks,us,XNAS,CS,true,USD,0000789019,2023-09-19T00:00:00Z
```

---

## 📜 License  
This project is licensed under the [MIT License](LICENSE).  
