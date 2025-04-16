from pykrx import stock
import pandas as pd

def fetch_investor_trading(date: str, codes: list[str]) -> pd.DataFrame:
    results = []
    for code in codes:
        try:
            df = stock.get_market_trading_value_by_investor(date, date, code)
            for investor in df.index:
                results.append({
                    'date': date,
                    'code': code,
                    'investor_type': investor,
                    'buy_amount': int(df.loc[investor]['매수']),
                    'sell_amount': int(df.loc[investor]['매도']),
                    'net_buy_amount': int(df.loc[investor]['순매수']),
                })
        except:
            continue
    return pd.DataFrame(results)
