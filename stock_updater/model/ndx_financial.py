from sqlalchemy import Column, String, Float, Date, Integer
from db.database import Base

class NasdaqFinancial(Base):
    __tablename__ = "ndx_financial"

    ticker = Column(String(10), primary_key=True)
    date = Column(Date, primary_key=True)
    label = Column(String(64), primary_key=True)  # 예: "current_assets"
    value = Column(Float, nullable=False)
    
    year = Column(Integer)