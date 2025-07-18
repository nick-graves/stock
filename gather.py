import yfinance as yf
import pandas as pd
from scrape import get_combined_web_text
from ai import summarize_with_gemini
from report import create_etf_pdf


print(r'''
  ____________________________  _________  ____  __. .___ _______  ___________________   
 /   _____/\__    ___/\_____  \ \_   ___ \|    |/ _| |   |\      \ \_   _____/\_____  \  
 \_____  \   |    |    /   |   \/    \  \/|      <   |   |/   |   \ |    __)   /   |   \ 
 /        \  |    |   /    |    \     \___|    |  \  |   /    |    \|     \   /    |    \
/_______  /  |____|   \_______  /\______  /____|__ \ |___\____|__  /\___  /   \_______  /
        \/                    \/        \/        \/             \/     \/            \/ 
''')


etf = input("Please input the ETF you would like to search: ")


summary = yf.Ticker(etf).info.get("longBusinessSummary")
print("==========================================================================================\n")
print(summary)
print("\n==========================================================================================")

print("\n\n")


print("==========================================================================================\n")
name = yf.Ticker(etf).info.get("shortName")
text = get_combined_web_text(name)
ai_summary = summarize_with_gemini(text)
with open("data/output_summary.txt", "w", encoding="utf-8") as f:
    f.write(ai_summary)
print(ai_summary)
print("\n==========================================================================================")

print("\n\n")

# grab data about top holdings and save to csv
etf_data = yf.Ticker(etf).funds_data
top_holdings = etf_data.top_holdings
print("==========================================================================================\n")
print(top_holdings)
top_holdings.to_csv("data/top_holdings.csv", index=True)
print("Top holdings saved to top_holdings.csv\n")
print("\n==========================================================================================")


# make csv iterable
df = pd.read_csv("data/top_holdings.csv")
data = df.to_dict(orient="records")

results = []


# iterate over each top holding
for row in data:
    ticker = row["Symbol"]
    stock = yf.Ticker(ticker)
    info = stock.info

    results.append({
        "Symbol": ticker,
        "Name": info.get("shortName"),
        "EPS (TTM)": info.get("trailingEps"),
        "Profit Margin": info.get("profitMargins"),
        "Market Cap": info.get("marketCap"),
        "PE Ratio (TTM)": info.get("trailingPE"),
        "Forward PE": info.get("forwardPE")
    })


    print(f"\n=== {ticker} ===")
    print(f"Name: {info.get('shortName')}")
    print(f"EPS (TTM): {info.get('trailingEps')}")
    print(f"Profit Margin: {info.get('profitMargins')}")
    print(f"Market Cap: {info.get('marketCap')}")
    print(f"PE Ratio (TTM): {info.get('trailingPE')}")
    print(f"Forward PE: {info.get('forwardPE')}")
    print("=========================================")




df = pd.DataFrame(results)
df.to_csv("data/stock_fundamentals.csv", index=False)
print("\nSaved fundamentals to data/stock_fundamentals.csv")


create_etf_pdf(
    summary_path="data/output_summary.txt",
    csv1_path="data/top_holdings.csv",
    csv2_path="data/stock_fundamentals.csv",
    output_pdf=f"report/{etf}.pdf"
)

