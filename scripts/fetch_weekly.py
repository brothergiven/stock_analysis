# KOSPI200 종목 fetch

import sys, time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from db.database import engine, init_db, get_session
import pandas as pd
from kis_auth import auth, getTREnv, get_headers
from sqlalchemy.orm import Session
from db.models import CompanyInfo
from db.weekly_models import Kospi200WeeklyMeta
from fetcher.weekly import get_kospi200_weekly


# 0. 토큰 발급, DB 초기화

auth()

env = getTREnv()
headers = get_headers()

init_db()


# 1. COMPANY_INFO DB에서 KOSPI200 종목 조회

with get_session() as session:
    kospi_200 = session.query(CompanyInfo.code, CompanyInfo.name).filter(CompanyInfo.market=="KOSPI200").all()



# 2. KOSPI 200 종목 코드에 대해 데이터 fetch(최근 10년년)

CUR_YEAR = 2025

for year in range(CUR_YEAR - 10, CUR_YEAR):
    for stock in kospi_200:
        print("f[조회 시작] {stock.code}, {year}")
        data = get_kospi200_weekly(env, stock.code, headers, year)

        if not data[0].empty:
            with get_session() as session:
                exists = session.query(Kospi200WeeklyMeta.code).filter(Kospi200WeeklyMeta.code == stock.code).first()
                if not exists:
                    data[0].to_sql('kospi200_weekly_meta', con=engine, if_exists="append", index=False)
        if not data[1].empty:
            data[1]['code'] = stock.code
            data[1].to_sql('kospi200_weekly', con=engine, if_exists="append", index=False)
        print(f"[저장 완료] {stock.code} {len(data[1])}")

