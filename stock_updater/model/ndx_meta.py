from sqlalchemy import Column, String, Integer, BigInteger, Date, Double, Numeric
from db.database import Base

class NasdaqMeta(Base):
    __tablename__ = "ndx_meta"

    ticker = Column(String(10), primary_key=True)
    face_value = Column(BigInteger)       # 액면가
    listed_shares = Column(BigInteger)    # 상장주식 수
    capital = Column(BigInteger)          # 자본금
    market_cap = Column(BigInteger) # 시가총액