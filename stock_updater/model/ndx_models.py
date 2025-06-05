from sqlalchemy import *
from db.database import Base

# NASDAQ-100 종목의 주간 데이터 저장
class NDXWeekly(Base):
    __tablename__ = "ndx_weekly"
    code = Column(String(10), primary_key=True, comment="종목 코드")
    date = Column(Date, primary_key=True, comment="기준일")

    close = Column(Numeric(10, 2), nullable=False, comment="종가")
    open = Column(Numeric(10, 2), nullable=False, comment="시가")
    high = Column(Numeric(10, 2), nullable=False, comment="고가")
    low = Column(Numeric(10, 2), nullable=False, comment="저가")
    acml_volume = Column(Numeric(20, 2), comment="누적 거래량")
    


class NDXDaily(Base):
    __tablename__ = 'ndx_daily'

    code = Column(String(10), primary_key=True)
    date = Column(Date, primary_key=True)
    close = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(BigInteger)
    trade_amount = Column(BigInteger)
