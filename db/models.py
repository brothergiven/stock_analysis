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


# 개인, 외국인, 기관별 거래 추이
class TradingByInvestorDaily(Base):
    __tablename__ = 'trading_by_investor_daily'

    date = Column(Date, primary_key=True)
    code = Column(String(6), primary_key=True)
    investor_type = Column(String(20), primary_key=True)  # 투자자 구분(예: 개인, 외국인, 기관합계)

    buy_amount = Column(BigInteger) # 매수 금액
    sell_amount = Column(BigInteger) # 매도 금액
    net_buy_amount = Column(BigInteger) # 순매수 금액


