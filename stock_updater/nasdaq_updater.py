from dataclasses import dataclass
from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker
from db.database import Base
from model.ndx_models import NDXWeekly
from kis_auth import getTREnv, get_headers
from fetcher.ndx_weekly import get_ndx_weekly
from fetcher.ndx_daily import get_ndx_daily
import time
import datetime
import pandas as pd

@dataclass
class Config:
    DATABASE_URL: str
    API_DELAY: float
    MAX_RETRIES: int

class NasdaqDataUpdater:
    def __init__(self, config: Config):
        self.engine = create_engine(config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.api_delay = config.API_DELAY
        self.max_retries = config.MAX_RETRIES
        self.tickers = [
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
        ] # NASDAQ-100 티커 생략
        self.env = getTREnv()
        self.headers = get_headers()

    def fetch_and_store_weekly(self, ticker: str, start_date: datetime.date, end_date: datetime.date):
        print(f"[조회] {ticker}: {start_date} ~ {end_date}")
        try:
            start_str = start_date.strftime("%Y%m%d")
            end_str = end_date.strftime("%Y%m%d")

            df = get_ndx_weekly(self.env, ticker, self.headers.copy(), start_str, end_str)
            if df is None or df.empty:
                print(f"[데이터 없음] {ticker}")
                return

            df['code'] = ticker
            df['date'] = pd.to_datetime(df['date'], format="%Y%m%d").dt.date
            df = df[['code', 'date', 'close', 'open', 'high', 'low', 'acml_volume']]
            df.to_sql('ndx_weekly', con=self.engine, if_exists='append', index=False)
            print(f"[저장 완료] {ticker}")
        except Exception as e:
            print(f"[에러] {ticker}: {e}")
        time.sleep(self.api_delay)

    def full_update(self, start_date=datetime.date(2015, 1, 1)):
        """최초 실행: 가능한 범위 전체 저장"""
        today = datetime.date.today()
        for ticker in self.tickers:
            self.fetch_and_store_weekly(ticker, start_date, today)

    def incremental_update(self):
        """DB에서 가장 최근 날짜 조회 → 이후 데이터만 수집"""
        today = datetime.date.today()
        session = self.Session()
        try:
            for ticker in self.tickers:
                latest: datetime.date = session.query(func.max(NDXWeekly.date))\
                    .filter(NDXWeekly.code == ticker)\
                    .scalar()

                if latest is None:
                    print(f"[신규 티커] {ticker} - 전체 수집")
                    start_date = datetime.date(2015, 1, 1)
                else:
                    start_date = latest + datetime.timedelta(days=1)

                if start_date > today:
                    print(f"[건너뜀] {ticker} - 최신 상태")
                    continue

                self.fetch_and_store_weekly(ticker, start_date, today)
        finally:
            session.close()
            
    def get_data_status(self):
        session = self.Session()
        result = {}
        try:
            for ticker in self.tickers:
                rows = session.execute(
                    text(f"SELECT COUNT(*), MIN(date), MAX(date) FROM ndx_weekly WHERE code = '{ticker}'")
                ).fetchone()

                result[ticker] = {
                    "record_count": rows[0],
                    "earliest_date": str(rows[1]) if rows[1] else "-",
                    "latest_date": str(rows[2]) if rows[2] else "-"
                }
        finally:
            session.close()
        return result
    
    def fetch_and_store_daily(self, ticker: str, date: datetime.date):
        print(f"[DAILY 조회] {ticker}: {date}")
        try:
            date_str = date.strftime("%Y%m%d")
            df = get_ndx_daily(self.env, ticker, self.headers.copy(),
                              date_str)
            if df is None or df.empty:
                print(f"[DAILY 없음] {ticker}")
                return

            df['code'] = ticker
            df['date'] = pd.to_datetime(df['date'], format="%Y%m%d").dt.date
            df = df[['code', 'date', 'close', 'open', 'high', 'low', 'volume', 'trade_amount']]
            df.to_sql('ndx_daily', con=self.engine, if_exists='append', index=False)
            print(f"[일간 저장 완료] {ticker} - {date}")
        except Exception as e:
            print(f"[에러 - 일간 저장 실패] {ticker}: {e}")
        time.sleep(self.api_delay)