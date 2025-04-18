# DB 스키마

## models.py

### 회사 정보 (CompanyInfo)

PyKRX에서 불러올 수 있는 KOSPI, KOSDAQ, KYNEX의 모든 종목 메타데이터를 저장했습니다.

- `code` : 종목 코드 (`String(10)`, Primary Key)  
- `name` : 종목명 (`String(50)`, Not Null)  
- `market` : 대표 시장명 (예: KOSPI, KOSDAQ) (`String(20)`, Not Null)  
- `industry` : 업종명 (`String(50)`, Not Null)  
- `capital` : 자본금 (억원 단위) (`BigInteger`, Nullable)  
- `shares` : 상장 주식 수 (`BigInteger`, Nullable)  
- `fiscal_month` : 결산월 (1~12) (`Integer`, Nullable)

### 일간 시세 데이터 (DailyPrice)

국내 10개 종목, NASDAQ 10개 종목의 일간 시세 데이터를 해당 종목 상장 시부터 DB에 저장했습니다.

- `date` : 거래일 (`Date`, Primary Key)  
- `open` : 시가 (`Integer`, Not Null)  
- `high` : 고가 (`Integer`, Not Null)  
- `low` : 저가 (`Integer`, Not Null)  
- `close` : 종가 (`Integer`, Not Null)  
- `volume` : 거래량 (`BigInteger`, Not Null)  
- `code` : 종목코드 (`String(10)`, Primary Key)

### 해외 주식 정보 (ForeignStock)

NASDAQ에 상장된 모든 종목의 메타데이터를 DB에 저장했습니다.

- `code` : 종목 코드 (`String(16)`, Primary Key)  
- `name` : 종목명 (한글) (`String(100)`, Not Null)  
- `eng_name` : 종목명 (영문) (`String(100)`, Nullable)  
- `exchange` : 거래소 이름 (`String(50)`, Not Null)  
- `type` : 상품유형 코드 (`String(10)`, Nullable)  
  - 예: `1`: 지수, `2`: 주식, `3`: ETP(ETF), `4`: Warrant  
- `currency` : 통화 단위 (`String(10)`, Nullable)


## weekly_models.py

### KOSPI200 주간 메타데이터 (Kospi200WeeklyMeta)

KOSPI200에 등록된 종목들의 추가 메타 정보들을 DB에 저장했습니다.

- `code` : 종목 코드 (`String(10)`, Primary Key)  
- `face_value` : 주식 액면가 (`BigInteger`)  
- `listed_shares` : 상장 주수 (`BigInteger`)  
- `capital` : 자본금 (`BigInteger`)  
- `market_cap` : HTS 기준 시가총액 (`BigInteger`)  
- `per` : 주가수익비율 (PER, `Float`)  
- `eps` : 주당순이익 (EPS, `Float`)  
- `pbr` : 주가순자산비율 (PBR, `Float`)  
- `loan_balance_ratio` : 전체 융자 잔고 비율 (`Float`)

### KOSPI200 주간 시세 데이터 (Kospi200Weekly)

KOSPI200에 등록된 모든 종목의 2015년~2024년의 주간 시세데이터를 DB에 저장했습니다.

- `code` : 종목 코드 (`String(10)`, Primary Key)  
- `date` : 주간 기준일 (`Date`, Primary Key)  

- `close` : 주간 종가 (`BigInteger`, Not Null)  
- `open` : 주간 시가 (`BigInteger`, Not Null)  
- `high` : 주간 고가 (`BigInteger`, Not Null)  
- `low` : 주간 저가 (`BigInteger`, Not Null)  

- `volume` : 주간 누적 거래량 (`BigInteger`)  
- `trade_amount` : 주간 누적 거래대금 (`BigInteger`)

  
### NASDAQ-100 주간 시세 데이터 (NDXWeekly)

NASDAQ-100에 등록된 모든 종목의 2015년~2024년의 주간 시세데이터를 DB에 저장했습니다.

- `code` : 종목 코드 (`String(10)`, Primary Key)  
- `date` : 주간 기준일 (`Date`, Primary Key)  

- `close` : 주간 종가 (`BigInteger`, Not Null)  
- `open` : 주간 시가 (`BigInteger`, Not Null)  
- `high` : 주간 고가 (`BigInteger`, Not Null)  
- `low` : 주간 저가 (`BigInteger`, Not Null)  
- `acml_volume` : 주간 누적 거래량 (`BigInteger`)



## finstmt_models.py

financial statements(재무제표) 데이터를 저장하기 위한 DB를 정의하였습니다.
2023년 3분기부터의 KOSPI200 종목의 분기별 재무정보를 저장했습니다. 

### 수익성(Profitability) - M210000
- corp_code : 고유 법인 코드 (String(12))
- stock_code : 종목 코드 (String(6), Primary Key)
- date : 기준일 (Date, Primary Key)
- net_profit_margin : 순이익률 (Float)
- comprehensive_income_margin : 총포괄이익률 (Float)
- gross_profit_margin : 매출총이익률 (Float)
- cost_of_sales_ratio : 매출원가율 (Float)
- roe : 자기자본이익률 (Float)
- sga_ratio : 판관비율 (Float)
- operating_income_total_assets_ratio : 총자산영업이익률 (Float)
- operating_income_equity_ratio : 자기자본영업이익률 (Float)
- operating_income_capital_ratio : 자본금영업이익률 (Float)
- paid_in_capital_return : 납입자본이익률 (Float)
- opex_to_orev : 영업수익경비율 (Float)

### 안정성(Stability) - M220000

- `corp_code` : 고유 법인 코드 (`String(12)`)
- `stock_code` : 종목 코드 (`String(6)`, Primary Key)
- `date` : 기준일 (`Date`, Primary Key)

- `equity_ratio` : 자기자본비율 (`Float`, %)
- `debt_ratio` : 부채비율 (`Float`, %)
- `current_ratio` : 유동비율 (`Float`, %)
- `current_liability_ratio` : 유동부채비율 (`Float`, %)
- `noncurrent_liability_ratio` : 비유동부채비율 (`Float`, %)
- `noncurrent_ratio` : 비유동비율 (`Float`, %)
- `interest_burden_ratio` : 금융비용부담률 (`Float`, %)
- `financial_leverage` : 재무레버리지 (`Float`)
- `noncurrent_suitability_ratio` : 비유동적합률 (`Float`, %)
- `noncurrent_asset_composition_ratio` : 비유동자산구성비율 (`Float`, %)
- `tangible_asset_composition_ratio` : 유형자산구성비율 (`Float`, %)
- `current_asset_composition_ratio` : 유동자산구성비율 (`Float`, %)
- `inventory_composition_ratio` : 재고자산구성비율 (`Float`, %)
- `current_to_noncurrent_asset_ratio` : 유동자산 / 비유동자산 비율 (`Float`, %)
- `inventory_to_current_asset_ratio` : 재고자산 / 유동자산 비율 (`Float`, %)

### 성장성(Growth) - M230000

- `corp_code` : 고유 법인 코드 (`String(12)`)
- `stock_code` : 종목 코드 (`String(6)`, Primary Key)
- `date` : 기준일 (`Date`, Primary Key)

- `revenue_growth_yoy` : 매출액 증가율 (YoY) (`Float`, %)
- `gross_profit_growth_yoy` : 매출총이익 증가율 (YoY) (`Float`, %)
- `operating_income_growth_yoy` : 영업이익 증가율 (YoY) (`Float`, %)
- `net_income_growth_yoy` : 순이익 증가율 (YoY) (`Float`, %)
- `comprehensive_income_growth_yoy` : 총포괄이익 증가율 (YoY) (`Float`, %)

- `total_assets_growth` : 총자산 증가율 (`Float`, %)
- `noncurrent_assets_growth` : 비유동자산 증가율 (`Float`, %)
- `tangible_assets_growth` : 유형자산 증가율 (`Float`, %)
- `total_liabilities_growth` : 부채총계 증가율 (`Float`, %)
- `equity_growth` : 자기자본 증가율 (`Float`, %)

- `current_assets_growth` : 유동자산 증가율 (`Float`, %)
- `inventory_growth` : 재고자산 증가율 (`Float`, %)
- `current_liabilities_growth` : 유동부채 증가율 (`Float`, %)
- `noncurrent_liabilities_growth` : 비유동부채 증가율 (`Float`, %)

### 활동성(Activity) - M240000

- `corp_code` : 고유 법인 코드 (`String(12)`)
- `stock_code` : 종목 코드 (`String(6)`, Primary Key)
- `date` : 기준일 (`Date`, Primary Key)

- `total_assets_turnover` : 총자산 회전율 (`Float`)
- `inventory_turnover` : 재고자산 회전율 (`Float`)
- `cogs_to_inventory` : 매출원가 대비 재고자산 비율 (`Float`)
- `noncurrent_assets_turnover` : 비유동자산 회전율 (`Float`)
- `tangible_assets_turnover` : 유형자산 회전율 (`Float`)
- `liabilities_turnover` : 타인자본 회전율 (`Float`)
- `equity_turnover` : 자기자본 회전율 (`Float`)
- `capital_turnover` : 자본금 회전율 (`Float`)
- `dividend_payout_ratio` : 배당성향 (%) (`Float`)
