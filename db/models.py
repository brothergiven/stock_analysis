"""
DB 정의
"""

from sqlalchemy import Column, String, Integer, BigInteger, Float, DateTime, Date
from db.database import Base
from datetime import datetime


# 회사 정보
class CompanyInfo(Base):
    __tablename__ = 'company_info'
    code = Column(String(10), primary_key=True, comment="종목 코드")
    name = Column(String(50), nullable=False, comment="종목명")
    market = Column(String(20), nullable=False, comment="대표 시장명 (예: KOSPI, KOSDAQ)")
    industry = Column(String(50), nullable=False, comment="업종명")
    capital = Column(BigInteger, nullable=True, comment="자본금 (억원)")
    shares = Column(BigInteger, nullable=True, comment="상장 주식 수")
    fiscal_month = Column(Integer, nullable=True, comment="결산월 (1~12)")
    created_at = Column(DateTime, default=datetime.now(), nullable=False, comment="데이터 생성 시각")
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False, comment="데이터 수정 시각")

# 일간 데이터
class DailyPrice(Base):
    __tablename__ = "daily_price"

    date = Column(Date, primary_key=True, comment="거래일")
    open = Column(Integer, nullable=False, comment="시가")
    high = Column(Integer, nullable=False, comment="고가")
    low = Column(Integer, nullable=False, comment="저가")
    close = Column(Integer, nullable=False, comment="종가")
    volume = Column(BigInteger, nullable=False, comment="거래량")
    code = Column(String(10), primary_key=True, comment="종목코드")


# 해외 주식 데이터
class ForeignStock(Base):
    __tablename__ = "foreign_stock"

    code = Column(String(16), primary_key=True, comment="종목 코드")
    name = Column(String(100), nullable=False, comment="종목명 (한글)")
    eng_name = Column(String(100), nullable=True, comment="종목명 (영문)")
    exchange = Column(String(50), nullable=False, comment="거래소 이름")
    type = Column(String(10), nullable=True, comment="상품유형 코드 (1:지수, 2:주식, 3:ETP(ETF), 4: Warrant)")
    currency = Column(String(10), nullable=True, comment="통화 단위")
    