# db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  
DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:password@localhost:3306/stock_db")


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# DB 초기화 (최초 1회 사용)
def init_db():
    from models import CompanyInfo, MarketDaily, TradingByInvestorDaily
    # DB 스키마 생성
    Base.metadata.create_all(bind=engine)

