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
    from model.ndx_models import NDXWeekly
    from model.kospi_models import Kospi200Meta, Kospi200Weekly
    from model.ndx_meta import NasdaqMeta
    from model.ndx_financial import NasdaqFinancial
    from model.kospi_financial import Kospi200Financial
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