from sqlalchemy import Column, String, Date, Integer, BigInteger, Float
from db.database import Base

class Kospi200Weekly(Base):
    __tablename__ = "kospi200_weekly"

    code = Column(String(12), nullable=False, primary_key=True)  # 종목 코드 (예: 005930)
    date = Column(Date, nullable=False, primary_key=True)  # 날짜 (주간 기준일)
    open = Column(BigInteger, nullable=False)  # 시가
    high = Column(BigInteger, nullable=False)  # 고가
    low = Column(BigInteger, nullable=False)  # 저가
    close = Column(BigInteger, nullable=False)  # 종가
    volume = Column(BigInteger, nullable=False)  # 거래량
    trade_amount = Column(BigInteger, nullable=False)  # 거래대금

class Kospi200Meta(Base):
    __tablename__ = "kospi200_meta"
    code = Column(String(12), primary_key=True)  # 종목 코드 (예: 005930)
    face_value = Column(Integer, nullable=False)  # 액면가
    listed_shares = Column(BigInteger, nullable=False)  # 상장 주식 수
    capital = Column(Integer, nullable=False)  # 자본금