from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from model.ndx_meta import NasdaqMeta
from kis_auth import getTREnv, get_headers
from util.cik_map import default_tickers
from fetcher.ndx_meta import get_ndx_meta
import time

@dataclass
class Config:
    DATABASE_URL: str
    API_DELAY: float


class NDXMetaUpdater:
    def __init__(self, config: Config):
        self.engine = create_engine(config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

        self.api_delay = config.API_DELAY

        # 실제 수집할 NASDAQ ticker 리스트
        self.tickers = default_tickers()
        self.env = getTREnv()
        self.headers = get_headers()

    def fetch_and_store_meta(self, ticker: str):
        
        meta = get_ndx_meta(self.env, ticker, self.headers.copy())
        if meta:
            session = self.Session()
            try:
                obj = NasdaqMeta(**meta)
                session.merge(obj)  # 기존 데이터는 업데이트, 없으면 insert
                session.commit()
                print(f"[메타 저장 완료] {ticker}")
            finally:
                session.close()
        else:
            print(f"[메타 저장 실패] {ticker}")

        time.sleep(self.api_delay)

    def full_update(self):
        for ticker in self.tickers:
            self.fetch_and_store_meta(ticker)