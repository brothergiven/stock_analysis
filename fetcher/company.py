from pykrx import stock
import pandas as pd

def fetch_company_info() -> pd.DataFrame:
    markets = ['KOSPI', 'KOSDAQ', 'KONEX']
    data = []
    for market in markets:
        tickers = stock.get_market_ticker_list(market=market)
        for code in tickers:
            name = stock.get_market_ticker_name(code)
            data.append({
                'code': code,
                'company': name,
                'market': market
            })
    return pd.DataFrame(data)
