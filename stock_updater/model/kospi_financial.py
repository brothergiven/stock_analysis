from sqlalchemy import Column, BigInteger, String, Integer, DateTime
from sqlalchemy.sql import func
from db.database import Base





class Kospi200Financial(Base):
    __tablename__ = "kospi200_financial"

    ticker_code = Column(String(12), nullable=False)
    corp_code = Column(String(12), nullable=False, primary_key=True)
    year = Column(Integer, nullable=False, primary_key=True)
    reprt_code = Column(String(6), nullable=False)  # 11011, 11012, ...
    
    current_assets = Column(BigInteger, nullable=True)
    non_current_assets = Column(BigInteger, nullable=True)
    current_liabilities = Column(BigInteger, nullable=True)
    non_current_liabilities = Column(BigInteger, nullable=True)
    total_equity = Column(BigInteger, nullable=True)

    revenue = Column(BigInteger, nullable=True)
    cost_of_sales = Column(BigInteger, nullable=True)
    gross_profit = Column(BigInteger, nullable=True)
    other_comprehensive_income = Column(BigInteger, nullable=True)
    net_income = Column(BigInteger, nullable=True)
