from sqlalchemy import Column, String, Integer, BigInteger, Float, DateTime, Date
from db.database import Base
from datetime import datetime

# KOSPI200 종목의 메타데이터 저장
class Kospi200WeeklyMeta(Base):
    __tablename__ = "kospi200_weekly_meta"

    code = Column(String(10), primary_key=True, comment="종목 코드")

    face_value = Column(BigInteger, comment="주식 액면가")
    listed_shares = Column(BigInteger, comment="상장 주수")
    capital = Column(BigInteger, comment="자본금")
    market_cap = Column(BigInteger, comment="HTS 시가총액")

    per = Column(Float, comment="PER")
    eps = Column(Float, comment="EPS")
    pbr = Column(Float, comment="PBR")
    loan_balance_ratio = Column(Float, comment="전체 융자 잔고 비율")


# KOSPI200 종목의 주간 데이터 저장
class Kospi200Weekly(Base):
    __tablename__ = "kospi200_weekly"

    code = Column(String(10), primary_key=True, comment="종목 코드")
    date = Column(Date, primary_key=True, comment="주간 기준일")

    close = Column(BigInteger, nullable=False, comment="종가")
    open = Column(BigInteger, nullable=False, comment="시가")
    high = Column(BigInteger, nullable=False, comment="고가")
    low = Column(BigInteger, nullable=False, comment="저가")

    volume = Column(BigInteger, comment="누적 거래량")
    trade_amount = Column(BigInteger, comment="누적 거래대금")

# NASDAQ-100 종목의 주간 데이터 저장
class NDXWeekly(Base):
    __tablename__ = "ndx_weekly"
    code = Column(String(10), primary_key=True, comment="종목 코드")
    date = Column(Date, primary_key=True, comment="기준일")

    close = Column(BigInteger, nullable=False, comment="종가")
    open = Column(BigInteger, nullable=False, comment="시가")
    high = Column(BigInteger, nullable=False, comment="고가")
    low = Column(BigInteger, nullable=False, comment="저가")
    acml_volume = Column(BigInteger, comment="누적 거래량")