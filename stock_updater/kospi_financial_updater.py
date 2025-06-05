from dataclasses import dataclass
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.database import Base

from model.kospi_financial import Kospi200Financial  

import time
import datetime
from fetcher.kospi_finance import fetch_dart_financials, extract_key_accounts  
from util.corp_code import get_corp_code_map, kospi200_tickers
@dataclass
class Config:
    DATABASE_URL: str
    API_DELAY: float
    MAX_RETRIES: int
class KospifinancialUpdater:
    def __init__(self, config: Config):
        self.engine = create_engine(config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.api_delay = config.API_DELAY

        self.tickers = kospi200_tickers().copy()
        self.ticker_to_corp = get_corp_code_map().copy()

    def fetch_and_store(self, ticker: str, year: int, reprt_code: str):
        corp_code = self.ticker_to_corp.get(ticker)
        if corp_code is None:
            print(f"[건너뜀] {ticker} → corp_code 없음")
            return
        try:
            print(f"[FETCH] {ticker} {year} {reprt_code}")
            raw = fetch_dart_financials(corp_code, year, reprt_code, fs_div="CFS")
            parsed = extract_key_accounts(raw)
            self.save_to_db(corp_code, year, reprt_code, parsed)
            return
        except Exception as e:
            print(f"[Error] {ticker} {year} {reprt_code}: {e}")
            time.sleep(self.api_delay)

    def full_update(self, start_year=2015):
        today = datetime.date.today()
        current_year = today.year
        for ticker in self.tickers:
            for year in range(start_year, current_year + 1):
                for reprt_code in ["11013", "11012", "11014", "11011"]:
                    self.fetch_and_store(ticker, year, reprt_code)
                    time.sleep(self.api_delay)
                    
    def incremental_update(self):
        session = self.Session()
        today = datetime.date.today()
        current_year = today.year
        try:
            for ticker in self.tickers:
                corp_code = self.ticker_to_corp.get(ticker)
                if corp_code is None:
                    print(f"[건너뜀] {ticker} → corp_code 없음")
                    continue

                result = session.execute(
                    text("SELECT MAX(year) FROM kospi200_financial WHERE corp_code = :corp_code"),
                    {"corp_code": corp_code},
                ).scalar()

                start_year = result + 1 if result else 2015
                if start_year > current_year:
                    print(f"[최신] {ticker}")
                    continue

                for year in range(start_year, current_year + 1):
                    for reprt_code in ["11013", "11012", "11014", "11011"]:
                        self.fetch_and_store(ticker, year, reprt_code)
                        time.sleep(self.api_delay)
        finally:
            session.close()
            
    def save_to_db(self, corp_code: str, year: int, reprt_code: str, data: dict):
        if not any(data.values()):
            print(f"[!] Skipping DB save: No valid financial data for {corp_code} {year} {reprt_code}")
            return
        session = self.Session()
        try:
            financial = Kospi200Financial(
                corp_code=corp_code,
                year=year,
                reprt_code=reprt_code,
                
                current_assets=data.get("current_assets"),
                non_current_assets=data.get("non_current_assets"),
                current_liabilities=data.get("current_liabilities"),
                non_current_liabilities=data.get("non_current_liabilities"),
                total_equity=data.get("total_equity"),
                
                revenue=data.get("revenue"),
                cost_of_sales=data.get("cost_of_sales"),
                gross_profit=data.get("gross_profit"),
                other_comprehensive_income=data.get("other_comprehensive_income"),
                net_income=data.get("net_income"),
            )
            session.merge(financial)
            session.commit()
            print(f"[DB] Saved: {corp_code} {year} {reprt_code}")
        except Exception as e:
            session.rollback()
            print(f"[DB Error] {corp_code} {year} {reprt_code}: {e}")
        finally:
            session.close()