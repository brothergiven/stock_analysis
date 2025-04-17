import sys, time
import os

from fetcher.ndx_weekly import get_ndx_weekly

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.database import engine, init_db
from kis_auth import auth, getTREnv, get_headers

# 0. 토큰 발급, DB 초기화

auth()

env = getTREnv()
headers = get_headers()

init_db()

# 1. NASDAQ-100

tickers = [
    "AAPL", "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "AMAT", "AMD", "AMGN",
    "AMZN", "ANSS", "APP", "ARM", "ASML", "AVGO", "AXON", "AZN", "BIIB", "BKNG",
    "BKR", "CCEP", "CDNS", "CDW", "CEG", "CHTR", "CMCSA", "COST", "CPRT", "CRWD",
    "CSCO", "CSGP", "CSX", "CTAS", "CTSH", "DASH", "DDOG", "DXCM", "EA", "EXC",
    "FANG", "FAST", "FTNT", "GEHC", "GFS", "GILD", "GOOG", "GOOGL", "HON", "IDXX",
    "INTC", "INTU", "ISRG", "KDP", "KHC", "KLAC", "LIN", "LRCX", "LULU", "MAR",
    "MCHP", "MDB", "MDLZ", "MELI", "META", "MNST", "MRVL", "MSFT", "MSTR", "MU",
    "NFLX", "NVDA", "NXPI", "ODFL", "ON", "ORLY", "PANW", "PAYX", "PCAR", "PDD",
    "PEP", "PLTR", "PYPL", "QCOM", "REGN", "ROP", "ROST", "SBUX", "SNPS", "TEAM",
    "TMUS", "TSLA", "TTD", "TTWO", "TXN", "VRSK", "VRTX", "WBD", "WDAY", "XEL", "ZS"
]

# 2. fetch

CUR_YEAR = 2025

for year in range(CUR_YEAR - 10, CUR_YEAR):
    for ticker in tickers:
        print(f"[조회 시작] {ticker}, {year}")
        params = {
            "FID_COND_MRKT_DIV_CODE": "N",
            "FID_INPUT_DATE_1": f"{year}0101",
            "FID_INPUT_DATE_2": f"{year}1231",
            "FID_PERIOD_DIV_CODE": 'W',
            "FID_INPUT_ISCD" : ticker
        }
        data = get_ndx_weekly(env, ticker, headers, year)

        if not data.empty:
            data['code'] = ticker
            data.to_sql('ndx_weekly', con=engine, if_exists="append", index=False)
        print(f'[저장 완료] {ticker}, {year}')
