from pykrx import stock
import pandas as pd


def fetch_market_data_range_by_code(start_date: str, end_date: str, code: str):
    """해당 종목의 시작날짜~종료날짜 까지의 market data 조회
    :param start_date: 시작 날짜
    :param end_date: 종료 날짜
    :param code: 티커
    :return: DataFrame
    """
    price_df = stock.get_market_ohlcv_by_date(fromdate=start_date, todate=end_date, ticker="005930", adjusted=True)
    fund_df = stock.get_market_fundamental_by_date(fromdate=start_date, todate=end_date, ticker="005930")
    cap_df = stock.get_market_cap_by_date(fromdate=start_date, todate=end_date, ticker="005930")
    foreign_df = stock.get_exhaustion_rates_of_foreign_investment_by_date(fromdate=start_date, todate=end_date, ticker="005930")

    # 인덱스 리셋, 중복 칼럼 수정
    def fix_index(df, value_cols):
        df = df.copy()
        df.reset_index(inplace=True)
        df = df.rename(columns={"날짜": "date"})
        df = df[value_cols + ['date']]
        return df

    price_df = fix_index(price_df, ['시가', '고가', '저가', '종가', '거래량', '등락률'])
    fund_df = fix_index(fund_df, ['BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS'])
    cap_df = fix_index(cap_df, ['시가총액', '거래대금', '상장주식수'])  # 거래량은 중복되므로 제거 가능
    foreign_df = fix_index(foreign_df, ['보유수량', '지분율', '한도수량', '한도소진률'])

    # 날짜로 Join
    merged = price_df.merge(fund_df, on=['date'], how='left')\
                     .merge(cap_df, on=['date'], how='left')\
                     .merge(foreign_df, on=['date'], how='left')

    merged = merged.rename(columns={
        '시가': 'open',
        '고가': 'high',
        '저가': 'low',
        '종가': 'close',
        '거래량': 'volume',
        '등락률' : 'change_rate',
        'BPS' : 'bps',
        'PER' : 'per',
        'PBR' : 'pbr',
        'EPS' : 'eps',
        'DIV' : 'div',
        'DPS': 'dps',
        '시가총액': 'market_cap',
        '거래대금': 'trade_value',
        '상장주식수': 'shares',
        '보유수량': 'foreign_shares',
        '지분율': 'foreign_ratio',
        '한도수량': 'limit_shares',
        '한도소진률': 'limit_ratio'
    })

    return merged