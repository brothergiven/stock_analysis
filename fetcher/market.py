from pykrx import stock
import pandas as pd

def fetch_market_daily(date: str, codes: list[str]) -> pd.DataFrame:
    price_df = stock.get_market_ohlcv(date, date)
    fund_df = stock.get_market_fundamental(date)
    cap_df = stock.get_market_cap(date)
    foreign_df = stock.get_exhaustion_rates_of_foreign_investment(date)

    results = []
    for code in codes:
        try:
            results.append({
                'date': date,
                'code': code,
                'open': int(price_df.loc[code]['시가']),
                'high': int(price_df.loc[code]['고가']),
                'low': int(price_df.loc[code]['저가']),
                'close': int(price_df.loc[code]['종가']),
                'volume': int(price_df.loc[code]['거래량']),
                'trade_value': int(price_df.loc[code]['거래대금']),
                'market_cap': int(cap_df.loc[code]['시가총액']),
                'listed_shares': int(cap_df.loc[code]['상장주식수']),
                'PER': float(fund_df.loc[code]['PER']),
                'EPS': int(fund_df.loc[code]['EPS']),
                'PBR': float(fund_df.loc[code]['PBR']),
                'BPS': int(fund_df.loc[code]['BPS']),
                'DIV': float(fund_df.loc[code]['DIV']),
                'DPS': int(fund_df.loc[code]['DPS']),
                'foreign_shares': int(foreign_df.loc[code]['보유수량']),
                'ownership_ratio': float(foreign_df.loc[code]['지분율']),
                'limit_ratio': float(foreign_df.loc[code]['한도소진율']),
            })
        except:
            continue
    return pd.DataFrame(results)
