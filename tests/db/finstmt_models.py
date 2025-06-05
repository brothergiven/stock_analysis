
from sqlalchemy import Column, String, Integer, BigInteger, Float, DateTime, Date
from db.database import Base
from datetime import datetime


# 수익성 지표(M210000)
class Profitability(Base):
    __tablename__ = "profitability"
    corp_code = Column(String(12))
    stock_code = Column(String(6), primary_key=True)

    date = Column(Date, comment = "기준일", primary_key=True)
    net_profit_margin = Column(Float, comment="순이익률")
    comprehensive_income_margin = Column(Float, comment="총포괄이익률")
    gross_profit_margin = Column(Float, comment="매출총이익률")
    cost_of_sales_ratio = Column(Float, comment="매출원가율")
    roe = Column(Float, comment="자기자본이익률")
    sga_ratio = Column(Float, comment="판관비율")
    operating_income_total_assets_ratio = Column(Float, comment="총자산영업이익률")
    operating_income_equity_ratio = Column(Float, comment="자기자본영업이익률")
    operating_income_capital_ratio = Column(Float, comment="자본금영업이익률")
    paid_in_capital_return = Column(Float, comment="납입자본이익률")
    opex_to_orev = Column(Float, comment="영업수익경비율")

# 안정성 지표(M220000)
class Stability(Base):
    __tablename__ = "stability"

    corp_code = Column(String(12), comment="고유 회사 코드")
    stock_code = Column(String(6), primary_key=True, comment="종목 코드")
    date = Column(Date, primary_key=True, comment="기준일")

    equity_ratio = Column(Float, comment="자기자본비율")
    debt_ratio = Column(Float, comment="부채비율")
    current_ratio = Column(Float, comment="유동비율")
    current_liability_ratio = Column(Float, comment="유동부채비율")
    noncurrent_liability_ratio = Column(Float, comment="비유동부채비율")
    noncurrent_ratio = Column(Float, comment="비유동비율")
    interest_burden_ratio = Column(Float, comment="금융비용부담률")
    financial_leverage = Column(Float, comment="재무레버리지")
    noncurrent_suitability_ratio = Column(Float, comment="비유동적합률")
    noncurrent_asset_composition_ratio = Column(Float, comment="비유동자산구성비율")
    tangible_asset_composition_ratio = Column(Float, comment="유형자산구성비율")
    current_asset_composition_ratio = Column(Float, comment="유동자산구성비율")
    inventory_composition_ratio = Column(Float, comment="재고자산구성비율")
    current_to_noncurrent_asset_ratio = Column(Float, comment="유동자산/비유동자산비율")
    inventory_to_current_asset_ratio = Column(Float, comment="재고자산/유동자산비율")

# 성장성 지표(M230000)
class Growth(Base):
    __tablename__ = "growth"

    corp_code = Column(String(12), comment="고유번호")
    stock_code = Column(String(6), primary_key=True, comment="종목코드")
    date = Column(Date, primary_key=True, comment="기준일")

    revenue_growth_yoy = Column(Float, comment="매출액증가율")
    gross_profit_growth_yoy = Column(Float, comment="매출총이익증가율")
    operating_income_growth_yoy = Column(Float, comment="영업이익증가율")
    net_income_growth_yoy = Column(Float, comment="순이익증가율")
    comprehensive_income_growth_yoy = Column(Float, comment="총포괄이익증가율")

    total_assets_growth = Column(Float, comment="총자산증가율")
    noncurrent_assets_growth = Column(Float, comment="비유동자산증가율")
    tangible_assets_growth = Column(Float, comment="유형자산증가율")
    total_liabilities_growth = Column(Float, comment="부채총계증가율")
    equity_growth = Column(Float, comment="자기자본증가율")

    current_assets_growth = Column(Float, comment="유동자산증가율")
    inventory_growth = Column(Float, comment="재고자산증가율")
    current_liabilities_growth = Column(Float, comment="유동부채증가율")
    noncurrent_liabilities_growth = Column(Float, comment="비유동부채증가율")


# 활동성 지표(M240000)

class Activity(Base):
    __tablename__ = "activity"

    corp_code = Column(String(12), comment="고유번호")
    stock_code = Column(String(6), primary_key=True, comment="종목코드")
    date = Column(Date, primary_key=True, comment="기준일")

    total_assets_turnover = Column(Float, comment="총자산회전율")
    inventory_turnover = Column(Float, comment="재고자산회전율")
    cogs_to_inventory = Column(Float, comment="매출원가/재고자산")
    noncurrent_assets_turnover = Column(Float, comment="비유동자산회전율")
    tangible_assets_turnover = Column(Float, comment="유형자산회전율")
    liabilities_turnover = Column(Float, comment="타인자본회전율")
    equity_turnover = Column(Float, comment="자기자본회전율")
    capital_turnover = Column(Float, comment="자본금회전율")
    dividend_payout_ratio = Column(Float, comment="배당성향(%)")