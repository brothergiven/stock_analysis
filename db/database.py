from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from contextlib import contextmanager

load_dotenv()  
DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:password@localhost:3306/stock_db")


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# DB 초기화 (최초 1회 사용)
def init_db():
    from db.models import CompanyInfo, DailyPrice, ForeignStock
    from db.weekly_models import Kospi200Weekly, Kospi200WeeklyMeta, NDXWeekly
    from db.finstmt_models import Activity, Growth, Profitability, Stability
    # DB 스키마 생성
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()  
    except:
        session.rollback()
        raise
    finally:
        session.close()