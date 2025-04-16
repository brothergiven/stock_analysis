"""
DB 정의
"""

from sqlalchemy import Column, String, Integer, BigInteger, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 회사 정보
class CompanyInfo(Base):
    __tablename__ = 'company_info'
    code = Column(String(6), primary_key=True) # 종목 코드
    company = Column(String(100)) # 회사 이름
    market = Column(String(10))  # KOSPI, KOSDAQ, KONEX
    last_update = Column(Date) # 마지막으로 정보가 갱신된 날짜


# 일간 OHLCV 데이터
class OHLCVDaily(Base):
    __tablename__ = 'ohlcv_daily'
    date = Column(Date, primary_key=True) # 거래일
    code = Column(String(6), primary_key=True) # 종목코드

    open = Column(Integer) # 시가
    high = Column(Integer) # 고가
    low = Column(Integer) # 저가
    close = Column(Integer) # 종가
    volume = Column(BigInteger) # 거래량

# 기업의 일별 재무지표
class FundamentalDaily(Base):
    __tablename__ = 'fundamental_daily'
    date = Column(Date, primary_key=True) 
    code = Column(String(6), primary_key=True)

    BPS = Column(Integer) # 주당순자산(Book value Per Share)
    PER = Column(Float) # 주가수익비율(Price / Earnings)
    PBR = Column(Float) # 주가순자산비율(Price / Book)
    EPS = Column(Integer) # 주당순이익(Earnings per share)
    DIV = Column(Float) # 배당수익률(%)
    DPS = Column(Integer) # 주당배당금(원)

# 시가총액 및 유동성 정보
class MarketCapDaily(Base):
    __tablename__ = 'market_cap_daily'

    date = Column(Date, primary_key=True)
    code = Column(String(6), primary_key=True)

    market_cap = Column(BigInteger) # 시가총액
    volume = Column(BigInteger) # 상장 주식 수
    trade_value = Column(BigInteger) # 거래량
    listed_shares = Column(BigInteger) # 거래대금

# 외국인 지분 정보
class ForeignOwnership(Base):
    __tablename__ = 'foreign_ownership'

    date = Column(Date, primary_key=True)
    code = Column(String(6), primary_key=True)

    foreign_shares = Column(BigInteger) # 외국인 보유 주식 수
    ownership_ratio = Column(Float) # 외국인 지분율
    limit_ratio = Column(Float) # 외국인 한도 소진율

# 개인, 외국인, 기관별 거래 추이
class TradingByInvestorDaily(Base):
    __tablename__ = 'trading_by_investor_daily'

    date = Column(Date, primary_key=True)
    code = Column(String(6), primary_key=True)
    investor_type = Column(String(20), primary_key=True)  # 투자자 구분(예: 개인, 외국인, 기관합계)

    buy_amount = Column(BigInteger) # 매수 금액
    sell_amount = Column(BigInteger) # 매도 금액
    net_buy_amount = Column(BigInteger) # 순매수 금액
