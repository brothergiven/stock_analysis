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
import xml.etree.ElementTree as ET
from fetcher.financial_statement_kospi200 import fetch_finstmt


# 0. 토큰 발급, DB 초기화

auth()

env = getTREnv()
headers = get_headers()

init_db()


# 1. COMPANY_INFO DB에서 KOSPI200 종목 조회

with get_session() as session:
    kospi_200 = session.query(CompanyInfo.code, CompanyInfo.name).filter(CompanyInfo.market=="KOSPI200").all()


# 2. KOSPI200 종목의 Corporation name 조회

# 2-0. XML 파일 파싱 후 저장
tree = ET.parse("../corp_code/CORPCODE.xml")
root = tree.getroot()

corp_list = []
for child in root:
    corp_code = child.find("corp_code").text
    corp_name = child.find("corp_name").text
    stock_code = child.find("stock_code").text
    modify_date = child.find("modify_date").text

    corp_list.append({
        "corp_code": corp_code,
        "corp_name": corp_name,
        "stock_code": stock_code,
        "modify_date": modify_date
    })

df = pd.DataFrame(corp_list)
df = df[df["stock_code"] != " "]  # 상장 종목만 필터링

# 3. fetch - M210000(수익성 지표)

li = [('2023', '11014'), ('2023', '11011'), ('2024', '11011'), ('2024', '11012'), ('2024', '11013'), ('2024', '11014') ]

for stock in kospi_200:
    line = df[df["stock_code"] == stock.code] # 해당 코드 데이터
    for l in li: # 분기별
        data = fetch_finstmt(line.iloc[0]['corp_code'], year = l[0], reprt = l[1], idx_cl="M210000")
        df_finst = pd.DataFrame([data])
        df_finst['corp_code'] = line.iloc[0]['corp_code']
        df_finst['stock_code'] = stock.code
        df_finst= df_finst.rename(columns={
            '순이익률': 'net_profit_margin',
            '총포괄이익률': 'comprehensive_income_margin',
            '매출총이익률': 'gross_profit_margin',
            '매출원가율': 'cost_of_sales_ratio',
            'ROE': 'roe',
            '판관비율': 'sga_ratio',
            '총자산영업이익률': 'operating_income_total_assets_ratio',
            '자기자본영업이익률': 'operating_income_equity_ratio',
            '자본금영업이익률': 'operating_income_capital_ratio',
            '납입자본이익률': 'paid_in_capital_return',
            '영업수익경비율': 'opex_to_orev'
        })
        columns_needed = [
            'corp_code',
            'stock_code',
            'date',
            'net_profit_margin',
            'comprehensive_income_margin',
            'gross_profit_margin',
            'cost_of_sales_ratio',
            'roe',
            'sga_ratio',
            'operating_income_total_assets_ratio',
            'operating_income_equity_ratio',
            'operating_income_capital_ratio',
            'paid_in_capital_return',
            'opex_to_orev'
        ]
        df_finst = df_finst[[col for col in columns_needed if col in df_finst.columns]]
        df_finst = df_finst.replace('#########', None)
        df_finst.to_sql('profitability', con=engine, if_exists="append", index=False)
        time.sleep(0.3)

# 3. fetch - M220000(안정성 지표)

for stock in kospi_200:
    line = df[df["stock_code"] == stock.code] # 해당 코드 데이터
    for l in li: # 분기별
        data = fetch_finstmt(line['corp_code'], year = l[0], reprt = l[1], idx_cl="M220000")
        df_finst = pd.DataFrame([data])
        df_finst['corp_code'] = line['corp_code']
        df_finst['stock_code'] = stock.code
        df_finst = df_finst.rename(columns={
            '자기자본비율': 'equity_ratio',
            '부채비율': 'debt_ratio',
            '유동비율': 'current_ratio',
            '유동부채비율': 'current_liability_ratio',
            '비유동부채비율': 'noncurrent_liability_ratio',
            '비유동비율': 'noncurrent_ratio',
            '금융비용부담률': 'interest_burden_ratio',
            '재무레버리지': 'financial_leverage',
            '비유동적합률': 'noncurrent_suitability_ratio',
            '비유동자산구성비율': 'noncurrent_asset_composition_ratio',
            '유형자산구성비율': 'tangible_asset_composition_ratio',
            '유동자산구성비율': 'current_asset_composition_ratio',
            '재고자산구성비율': 'inventory_composition_ratio',
            '유동자산/비유동자산비율': 'current_to_noncurrent_asset_ratio',
            '재고자산/유동자산비율': 'inventory_to_current_asset_ratio'
        })
        columns_needed=[
            'corp_code',
            'stock_code',
            'date',
            'equity_ratio',
            'debt_ratio',
            'current_ratio',
            'current_liability_ratio',
            'noncurrent_liability_ratio',
            'noncurrent_ratio',
            'interest_burden_ratio',
            'financial_leverage',
            'noncurrent_suitability_ratio',
            'noncurrent_asset_composition_ratio',
            'tangible_asset_composition_ratio',
            'current_asset_composition_ratio',
            'inventory_composition_ratio',
            'current_to_noncurrent_asset_ratio',
            'inventory_to_current_asset_ratio'
        ]
        df_finst =df_finst[[col for col in columns_needed if col in df_finst.columns]]
        df_finst = df_finst.replace('#########', None)
        df_finst.to_sql('stability', con=engine, if_exists="append", index=False)
        time.sleep(0.3)

# 3. fetch - M230000

for stock in kospi_200:
    line = df[df["stock_code"] == stock.code] # 해당 코드 데이터
    for l in li: # 분기별
        data = fetch_finstmt(line['corp_code'], year = l[0], reprt = l[1], idx_cl="M230000")
        df_finst = pd.DataFrame([data])
        df_finst['corp_code'] = line['corp_code']
        df_finst['stock_code'] = stock.code
        df_finst = df_finst.rename(columns={
            '매출액증가율(YoY)': 'revenue_growth_yoy',
            '매출총이익증가율(YoY)': 'gross_profit_growth_yoy',
            '영업이익증가율(YoY)': 'operating_income_growth_yoy',
            '순이익증가율(YoY)': 'net_income_growth_yoy',
            '총포괄이익증가율(YoY)': 'comprehensive_income_growth_yoy',
            '총자산증가율': 'total_assets_growth',
            '비유동자산증가율': 'noncurrent_assets_growth',
            '유형자산증가율': 'tangible_assets_growth',
            '부채총계증가율': 'total_liabilities_growth',
            '자기자본증가율': 'equity_growth',
            '유동자산증가율': 'current_assets_growth',
            '재고자산증가율': 'inventory_growth',
            '유동부채증가율': 'current_liabilities_growth',
            '비유동부채 증가율': 'noncurrent_liabilities_growth'
        })
        columns_needed = [
            'corp_code',
            'stock_code',
            'date',
            'revenue_growth_yoy',
            'gross_profit_growth_yoy',
            'operating_income_growth_yoy',
            'net_income_growth_yoy',
            'comprehensive_income_growth_yoy',
            'total_assets_growth',
            'noncurrent_assets_growth',
            'tangible_assets_growth',
            'total_liabilities_growth',
            'equity_growth',
            'current_assets_growth',
            'inventory_growth',
            'current_liabilities_growth',
            'noncurrent_liabilities_growth'
        ]
        df_finst = df_finst.replace('#########', None)
        df_finst = df_finst[[col for col in columns_needed if col in df_finst.columns]]
        df_finst.to_sql('growth', con=engine, if_exists="append", index=False)
        time.sleep(0.3)

# 3. fetch - M240000

for stock in kospi_200:
    line = df[df["stock_code"] == stock.code] # 해당 코드 데이터
    for l in li: # 분기별
        data = fetch_finstmt(line['corp_code'], year = l[0], reprt = l[1], idx_cl="M240000")
        df_finst = pd.DataFrame([data])
        df_finst['corp_code'] = line['corp_code']
        df_finst['stock_code'] = stock.code
        df_finst = df_finst.rename(columns={
            '총자산회전율': 'total_assets_turnover',
            '재고자산회전율': 'inventory_turnover',
            '매출원가/재고자산': 'cogs_to_inventory',
            '비유동자산회전율': 'noncurrent_assets_turnover',
            '유형자산회전율': 'tangible_assets_turnover',
            '타인자본회전율': 'liabilities_turnover',
            '자기자본회 전율': 'equity_turnover', 
            '자본금회전율': 'capital_turnover',
            '배당성향(%)': 'dividend_payout_ratio'
        })
        columns_needed=[
            'corp_code',
            'stock_code',
            'date',
            'total_assets_turnover',
            'inventory_turnover',
            'cogs_to_inventory',
            'noncurrent_assets_turnover',
            'tangible_assets_turnover',
            'liabilities_turnover',
            'equity_turnover',
            'capital_turnover',
            'dividend_payout_ratio'
        ]
        df_finst = df_finst[[col for col in columns_needed if col in df_finst.columns]]

        df_finst = df_finst.replace('#########', None)
        if 'capital_turnover' in df_finst.columns:
            df_finst = df_finst.astype({
                'capital_turnover': 'float'
            })
        df_finst.to_sql('activity', con=engine, if_exists="append", index=False)
        time.sleep(0.3)