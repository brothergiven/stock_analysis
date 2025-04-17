import sys, time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pandas as pd
from sqlalchemy.orm import Session
from db.database import engine, init_db, get_session
from db.models import DailyPrice
from datetime import datetime

init_db()


def load_excel_and_save_to_db(file_path: str, stock_code: str):
    print(f"[{stock_code}] 파일 로딩 중...")

    # 엑셀 읽기
    df = pd.read_excel(file_path)

    # 컬럼 이름 정제
    df = df.rename(columns={
        "시간": "date",
        "시가": "open",
        "고가": "high",
        "저가": "low",
        "종가": "close",
        "거래량": "volume"
    })

    # 날짜 형식 변환
    df["date"] = pd.to_datetime(df["date"]).dt.date

    # 필요한 컬럼만 정제
    df = df[["date", "open", "high", "low", "close", "volume"]]
    df["code"] = stock_code

    # row = df.iloc[0]  # 첫 줄만
    # print(row.to_dict())

    # daily = DailyPrice(
    #     date=row["date"],
    #     code=row["code"],
    #     open=row["open"],
    #     high=row["high"],
    #     low=row["low"],
    #     close=row["close"],
    #     volume=row["volume"]
    # )

    # with get_session() as session:
    #     session.add(daily)
    #     print("추가 완료")

    with get_session() as session:
        for _, row in df.iterrows():
            daily = DailyPrice(
                date=row["date"],
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                volume=row["volume"],
                code=row["code"]
            )
            session.add(daily)  
    session.commit()

    print(f"[{stock_code}] 저장 완료")

if __name__ == '__main__':
    dir = './files/'
    for filename in os.listdir(dir):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(dir, filename)
            stock_code = filename.replace('.xlsx', '')  # 파일명에서 종목 추출
            load_excel_and_save_to_db(file_path=filepath, stock_code=stock_code)
            
