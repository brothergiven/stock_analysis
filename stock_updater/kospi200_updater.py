from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, text
import datetime
from model.kospi_models import Kospi200Meta, Kospi200Weekly
from fetcher.kospi200 import get_kospi200_meta, get_kospi200_weekly_data, get_kospi200_daily
from db.database import Base
import time
import pandas as pd
from dataclasses import dataclass
from kis_auth import getTREnv, get_headers
from util.corp_code import kospi200_tickers


@dataclass
class Config:
    DATABASE_URL: str
    API_DELAY: float
    MAX_RETRIES: int

class Kospi200Updater:
    def __init__(self, config: Config):
        self.engine = create_engine(config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.api_delay = config.API_DELAY
        self.max_retries = config.MAX_RETRIES

        self.tickers = kospi200_tickers()
        self.env = getTREnv()
        self.headers = get_headers()

    def fetch_and_store_weekly(self, ticker: str, start_date: datetime.date, end_date: datetime.date):
        print(f"[조회] {ticker}: {start_date} ~ {end_date}")
        # try:
        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")

        df = get_kospi200_weekly_data(self.env, ticker, self.headers.copy(), start_str, end_str)
        if df is None or df.empty:
            print(f"[데이터 없음] {ticker}")
            return
        df['code'] = ticker
        df['date'] = pd.to_datetime(df['date'], format="%Y%m%d").dt.date
        df = df[['code', 'date', 'close', 'open', 'high', 'low', 'volume', 'trade_amount']]
        df.to_sql("kospi200_weekly", con=self.engine, if_exists='append', index=False)
        print(f"[저장 완료] {ticker}")
        # except Exception as e:
        #     print(f"[에러] {ticker}: {e}")
        time.sleep(self.api_delay)

    def save_meta_data(self, ticker):
        meta = get_kospi200_meta(self.env, ticker, self.headers.copy())
        if meta:
            session = self.Session()
            try:
                obj = Kospi200Meta(**meta)
                session.merge(obj)
                session.commit()
                print(f"[메타 저장 완료] {ticker} ")
            finally:
                session.close()

    def full_update(self, start_date=datetime.date(2015, 1, 1)):
        today = datetime.date.today()
        for ticker in self.tickers:
            self.fetch_and_store_weekly(ticker, start_date, today)
            time.sleep(self.api_delay)  
            self.save_meta_data(ticker)


        

    def incremental_update(self):
        today = datetime.now().date()
        session = self.Session()
        try:
            for ticker in self.tickers:
                latest = session.query(func.max(Kospi200Weekly.date))\
                    .filter(Kospi200Weekly.code == ticker)\
                    .scalar()

                start_year = 2015 if latest is None else latest.year
                end_year = today.year
                self.save_meta_data(ticker)
                for year in range(start_year, end_year + 1):
                    # 메타데이터 연도별 저장


                    # 날짜 범위 계산
                    start_date = datetime(year, 1, 1).date()
                    end_date = datetime(year, 12, 31).date()
                    if end_date > today:
                        end_date = today

                    self.fetch_and_store_weekly(ticker, start_date, end_date)
        finally:
            session.close()

    def update_ticker_data(self, ticker):
        today = datetime.now().date()
        session = self.Session()
        try:
            latest = session.query(func.max(Kospi200Weekly.date))\
                .filter(Kospi200Weekly.code == ticker)\
                .scalar()
            start_year = 2015 if latest is None else latest.year
            self.save_meta_data(ticker)
            # for year in range(start_year, today.year + 1):
                # self.save_weekly_data(ticker, year)
        finally:
            session.close()

    def get_data_status(self):
        session = self.Session()
        result = {}
        try:
            for ticker in self.tickers:
                # 주간 시세 정보
                rows = session.execute(
                    text(f"""
                        SELECT COUNT(*) AS cnt, MIN(date) AS min_date, MAX(date) AS max_date 
                        FROM kospi200_weekly 
                        WHERE code = :code
                    """),
                    {'code': ticker}
                ).fetchone()

                # 메타데이터 정보
                meta_rows = session.execute(
                    text(f"""
                        SELECT COUNT(*) AS cnt, MIN(year) AS min_year, MAX(year) AS max_year 
                        FROM kospi200_meta 
                        WHERE code = :code
                    """),
                    {'code': ticker}
                ).fetchone()

                result[ticker] = {
                    "record_count": rows[0],
                    "earliest_date": str(rows[1]) if rows[1] else "-",
                    "latest_date": str(rows[2]) if rows[2] else "-",
                    "meta_count": meta_rows[0],
                    "meta_start_year": str(meta_rows[1]) if meta_rows[1] else "-",
                    "meta_end_year": str(meta_rows[2]) if meta_rows[2] else "-"
                }
        finally:
            session.close()
        return result
    
    def fetch_and_store_daily(self, ticker: str, date: datetime.date):
        print(f"[DAILY 조회] {ticker}: {date}")
    
        try:
            date_str = date.strftime("%Y%m%d")
            df = get_kospi200_daily(self.env, ticker, self.headers.copy(), date_str)
            if df is None or df.empty:
                print(f"[일간 데이터 없음] {ticker} - {date}")
                return

            df['code'] = ticker
            df['date'] = pd.to_datetime(df['date'], format="%Y%m%d").dt.date
            df = df[['code', 'date', 'close', 'open', 'high', 'low', 'volume', 'trade_amount']]

            df.to_sql("kospi200_daily", con=self.engine, if_exists='append', index=False)
            print(f"[일간 저장 완료] {ticker} - {date}")
        except Exception as e:
            print(f"[에러 - 일간 저장 실패] {ticker}: {e}")
        time.sleep(self.api_delay)
        