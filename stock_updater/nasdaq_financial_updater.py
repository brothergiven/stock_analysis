from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from model.ndx_financial import NasdaqFinancial
import requests, time
from datetime import datetime
from typing import List, Dict
from util.cik_map import build_cik_map

TAG_CANDIDATES = {
    "current_assets": ["AssetsCurrent", "CurrentAssets"],
    "noncurrent_assets": ["AssetsNoncurrent", "NoncurrentAssets"],
    "current_liabilities": ["LiabilitiesCurrent", "CurrentLiabilities", "Liabilities"],
    "noncurrent_liabilities": [
        "LiabilitiesNoncurrent", "LongTermLiabilities", "OtherLiabilitiesNoncurrent",
        "LongTermDebtNoncurrent", "OperatingLeaseLiabilityNoncurrent", "FinanceLeaseLiabilityNoncurrent"
    ],
    "common_stock_shares": [
        "CommonStockSharesOutstanding", "EntityCommonStockSharesOutstanding", "WeightedAverageNumberOfSharesOutstandingBasic"
    ]
}

INCOME_TAG_CANDIDATES = {
    "revenue": [
        "Revenues",
        "SalesRevenueNet",
        "RevenueFromContractWithCustomerExcludingAssessedTax"
    ],
    "cogs": [
        "CostOfRevenue",
        "CostOfGoodsSold",
        "CostOfSales",
        "CostOfGoodsAndServicesSold", 
        "OperatingExpenses"    
    ],
    "gross_profit": [
        "GrossProfit"
    ],
    "net_income": [
        "NetIncomeLoss"
    ],
    "oci": [
        "OtherComprehensiveIncomeLossNetOfTax",
        "ComprehensiveIncomeNetOfTax"
    ]
}

@dataclass
class Config:
    DATABASE_URL: str
    API_DELAY: float
    MAX_RETRIES: int


class NasdaqFinancialUpdater:
    def __init__(self, config: Config, tickers: List[str] = None):
        self.engine = create_engine(config.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.api_delay = config.API_DELAY
        self.max_retries = config.MAX_RETRIES
        self.tickers = tickers or self.default_tickers()
        self.headers = {
            "User-Agent": "example@email.com"
        }
        self.ticker_to_cik = build_cik_map()

    def default_tickers(self) -> List[str]:
        return ['AAPL', 'ABNB', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'AMAT', 'AMD',
           'AMGN', 'AMZN', 'ANSS', 'APP', 'ARM', 'AVGO', 'AXON', 'BIIB',
           'BKNG', 'BKR', 'CDNS', 'CDW', 'CEG', 'CHTR', 'CMCSA', 'COST',
           'CPRT', 'CRWD', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTSH', 'DASH',
           'DDOG', 'DXCM', 'EA', 'EXC', 'FANG', 'FAST', 'FTNT', 'GEHC',
           'GILD', 'GOOG', 'GOOGL', 'HON', 'IDXX', 'INTC', 'INTU', 'ISRG',
           'KDP', 'KHC', 'KLAC', 'LIN', 'LRCX', 'LULU', 'MAR', 'MCHP', 'MDB',
           'MDLZ', 'MELI', 'META', 'MNST', 'MRVL', 'MSFT', 'MSTR', 'MU',
           'NFLX', 'NVDA', 'NXPI', 'ODFL', 'ON', 'ORLY', 'PANW', 'PAYX',
           'PCAR', 'PDD', 'PEP', 'PLTR', 'PYPL', 'QCOM', 'REGN', 'ROP',
           'ROST', 'SBUX', 'SNPS', 'TEAM', 'TMUS', 'TSLA', 'TTD', 'TTWO',
           'TXN', 'VRSK', 'VRTX', 'WBD', 'WDAY', 'XEL', 'ZS']


    def fetch_tag_data(self, cik: str, tag: str, unit: str) -> Dict[str, float]:
        url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json"
        for _ in range(self.max_retries):
            try:
                res = requests.get(url, headers=self.headers)
                if res.status_code != 200:
                    return {}
                data = res.json()
                items = data.get("units", {}).get(unit, [])
                result = {}
                for item in items:
                    date = item.get("end")
                    year = int(date[:4])
                    if 2014 <= year <= 2024:
                        val = item.get("val")
                        if val is not None and (date not in result or val > result[date]):
                            result[date] = val
                return result
            except:
                time.sleep(0.2)
        return {}

    def fetch_and_store(self):
        session = self.Session()
        try:
            for ticker in self.tickers:
                cik = self.ticker_to_cik.get(ticker.upper())
                if not cik:
                    print(f"[CIK 없음] {ticker}")
                    continue

                print(f"[재무 수집 시작] {ticker} (CIK={cik})")

                for source_label, tag_dict in {
                    "balance": TAG_CANDIDATES,
                    "income": INCOME_TAG_CANDIDATES
                }.items():
                    for label, tags in tag_dict.items():
                        unit = "shares" if "shares" in label.lower() else "USD"
                        for tag in tags:
                            data = self.fetch_tag_data(cik, tag, unit)
                            if data:
                                for date_str, val in data.items():
                                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                                    year = int(date_str[:4])
                                    record = NasdaqFinancial(
                                        ticker=ticker,
                                        date=date,
                                        label=label,  # 'revenue', 'gross_profit' 등
                                        value=val,
                                        year=year
                                    )
                                    session.merge(record)
                                session.commit()
                                break
                            time.sleep(self.api_delay)
        finally:
            session.close()

    def full_update(self):
        print("[NASDAQ 재무정보 전체 수집]")
        self.fetch_and_store()

    def update(self):
        self.full_update()  # 현재는 full과 동일

    def get_data_status(self):
        session = self.Session()
        try:
            rows = session.execute("""
                SELECT ticker, COUNT(*), MIN(date), MAX(date)
                FROM ndx_financial
                GROUP BY ticker
            """).fetchall()
            for row in rows:
                print(f"{row[0]}: {row[1]}개 항목 / {row[2]} ~ {row[3]}")
        finally:
            session.close()
