# Scripts

### fetch_finstmt.py

- KOSPI200 종목의 재무제표(2023년 3분기 ~)를 읽어와 DB에 저장합니다. (DART API)

### fetch_weekly_ndx.py

- NASDAQ-100 종목의 10년치 주간 종가, 시가, 고가, 저가, 누적 거래량 데이터를 읽어와 DB에 저장합니다. (KIS API)

### fetch_weekly.py

- KOSPI200 종목의 10년치 주간 종가, 시가, 고가, 저가, 거래량 데이터와 각 종목의 액면가, 상장 주수, 자본금, 시가총액, PER, EPS, PBR을 읽어와 DB에 저장합니다 (KIS API)

### init_company.py

- KOSPI, KOSDAQ, KYNEX의 모든 종목의 종목 코드와 종목명, 업종, 자본금, 상장주식수를 읽어와 DB에 저장합니다. (PyKRX)

### load_daily.py

- 국내 주식 10개 종목 : SK하이닉스(000660), 현대자동차(005380), POSCO홀딩스(005490), 삼성전자(005930), NAVER(035420), 카카오(035720), 신한지주(055550), 셀트리온(068270), 삼성바이오로직스(207940), LG에너지솔루션(373220)
- 미국 주식 10개 종목 : 애플(AAPL), 어도비(ADBE), AMD(AMD), 아마존(AMZN), 알파벳(GOOGL), 인텔(INTC), 메타플랫폼스(META), 마이크로소프트(MSFT), 엔비디아(NVDA), 테슬라(TSLA)

의 일간 시가, 고가, 저가, 종가, 거래량을 DB에 저장합니다.

### load_foreign.py

- NASDAQ의 모든 종목의 종목코드, 종목명, 영어이름, 화폐 단위, 상품유형 코드를 DB에 저장합니다. (KIS API) 

