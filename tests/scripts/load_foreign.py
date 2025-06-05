
import sys, time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pandas as pd
from datetime import datetime
from db.database import get_session, init_db
from db.models import ForeignStock

def load_foreign_stock_file(file_path: str):
    # 파일 불러오기
    df = pd.read_csv(file_path, encoding='cp949', header=None)

    # 컬럼 수동 지정
    df.columns = [
        'nation_code', 'exchange_id', 'exchange_code', 'exchange_name', 'symbol',
        'realtime_symbol', 'name_kr', 'name_en', 'security_type', 'currency',
        'float_pos', 'data_type', 'base_price', 'bid_unit', 'ask_unit', 'open_time',
        'close_time', 'is_dr', 'dr_country', 'industry_code', 'index_component',
        'tick_type', 'etf_type', 'tick_sub_type'
    ]

    # 필요한 항목만 정리
    df = df[['symbol', 'name_kr', 'name_en', 'exchange_name', 'security_type', 'currency']]
    df.columns = ['code', 'name', 'eng_name', 'exchange', 'type', 'currency']
    for col in ["code", "name", "eng_name", "exchange", "currency"]:
        df[col] = df[col].astype(str).str.strip()
    # DB에 저장
    with get_session() as session:
        for _, row in df.iterrows():
            # print(row)
            stock = ForeignStock(
                code=row['code'],
                name=row['name'],
                eng_name=row['eng_name'],
                exchange=row['exchange'],
                type=row['type'],
                currency=row['currency']
            )
            session.merge(stock)
        session.commit()

    print(f"[완료] 총 {df.size}개의 해외 종목이 저장되었습니다.")

if __name__ == "__main__":
    init_db()
    load_foreign_stock_file('./files/NASMST.csv')