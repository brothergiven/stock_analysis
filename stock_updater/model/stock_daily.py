from db.database import Base
from sqlalchemy import Column, String, Integer, BigInteger, Date

class Kospi200Daily(Base):
    __tablename__ = "Kospi200_daily"
    
    code = Column(String(10), index=True, primary_key=True)
    date = Column(Date, index=True, primary_key=True)
    open = Column(BigInteger)
    high = Column(BigInteger)
    low = Column(BigInteger)
    close = Column(BigInteger)
    volume = Column(BigInteger)
    trade_amount = Column(BigInteger)