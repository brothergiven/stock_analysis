
import sys, time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from fetcher.company import get_all_listed_stocks, get_company_static_info
from db.database import engine, init_db, get_session
import pandas as pd
from kis_auth import auth, getTREnv, get_headers
from sqlalchemy.orm import Session
from db.models import CompanyInfo
# 0. 토큰 발급, DB 초기화화

auth()

env = getTREnv()
headers = get_headers()

init_db()

# 1. 모든 tickers list 조회(pykrx)

tickers = get_all_listed_stocks()

# 2. 모든 tickers에 대해 종목 정보 조회(KIS OpenAPI)

for i, row in tickers.iterrows():
    stock_code = row["code"]
    name = row["name"]
    market = row['market']

    with get_session() as session:
        exists = session.query(CompanyInfo).filter(CompanyInfo.code == stock_code).first()

        if exists:
            print(f"[PASS] 이미 존재: {stock_code} {name}")
            continue

    info = get_company_static_info(env, headers, stock_code, name, market)
    if info:
        print(f"[INSERT] {stock_code} {name}")
        pd.DataFrame([info]).to_sql("company_info", engine, if_exists='append', index=False)
    else:
        print(f"[FAIL] 조회 실패: {stock_code} {name}")
    time.sleep(0.3)


