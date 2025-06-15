# 📊 NASDAQ / KOSPI 데이터 수집기

주요 글로벌·국내 지수(NASDAQ-100, KOSPI200)의 **시계열 데이터 / 재무제표 / 메타정보**를 수집·저장하는 CLI 기반 통합 수집기입니다.

---

## ✔️ 데이터 출처

- KIS(한국투자증권) OpenAPI : https://apiportal.koreainvestment.com/intro
- OPENDART(전자공시시스템) : https://opendart.fss.or.kr/
- EDGAR API : https://www.sec.gov/search-filings/edgar-application-programming-interfaces

---

## 🚀 실행 방법

```bash
python run_updater.py --dataset <데이터셋> --mode <작업모드> [--config path/to/config.json]
```

- `--dataset` 옵션 : 수집할 데이터 셋을 지정합니다.
  - `nasdaq-weekly` : NASDAQ-100 종목의 주간 OHLCV 시계열 데이터를 수집합니다. `ndx_weekly` 테이블에 저장됩니다.
  - `kospi200-weekly` : KOSPI-200 종목의 주간 OHLCV 시계열 데이터와 해당 종목의 메타정보를 수집합니다. `kospi200_weekly`, `kospi200_meta` 테이블에 저장됩니다.
  - `nasdaq-financial` : NASDAQ-100 종목의 재무지표 데이터를 수집합니다. `ndx_financial` 테이블에 저장됩니다. 수집되는 지표는 포괄손익계산서, 재무상태표입니다.
  - `nasdaq-meta` : NASDAQ-100 종목의 메타정보를 수집합니다. `ndx_meta` 테이블에 저장됩니다.
  - `kospi-financial` : KOSPI-200 종목의 재무지표 데이터를 수집합니다. `kospi200-financial` 테이블에 저장됩니다. 수집되는 지표는 포괄손익계산서, 재무상태표입니다.
- `--mode` 옵션 : 작업 모드를 지정합니다.
  - `init` : 초기 데이터를 저장합니다. 2015년 1월 1일 부터 실행 시점까지의 데이터를 가져옵니다.
  - `update` : DB에 저장된 가장 최근 데이터부터 실행 시점까지의 데이터를 가져옵니다.
  - `status` : 현재 저장된 데이터의 상태를 출력합니다.
- `--config` 옵션 : `config.json` 파일의 위치를 지정합니다.

### 환경 변수

- `DB_URL` : 데이터베이스 URL
- `KIS_APP` : KIS에서 발급받은 APP KEY
- `KIS_SEC` : KIS에서 발급받은 SECURITY KEY
- `KIS_ACCT` : KIS 계좌번호 (ex. 43016876)
- `KIS_PROD` : KIS 계좌 상품 코드 (ex. 01)
- `DART_KEY` : OpenDart에서 발급받은 KEY

이 스크립트를 실행하기 위해서는 한국투자증권 회원가입 및 계좌개설 후 KEY 발급, OPENDART 회원가입 후 KEY 발급이 필요합니다.

---

## 🔧 DB 스키마

### kospi200_financial

KOSPI200 종목의 재무제표 데이터입니다. 이 때 Corp_code 칼럼은 Ticker 와 다르며, 전자 공시를 위한 회사 고유 코드입니다. 회사별 고유 코드는 `/CORPCODE.xml` 에 작성되어 있으며, 이를 위한 변환 코드는 `/util/corp_code.py` 에 작성되어 있습니다.


| 컬럼명                          | PK | 데이터 타입       | 설명                              |
| ---------------------------- | -- | ------------ | ------------------------------- |
| `corp_code`                  | ✅  | `String(12)` | 회사 고유 코드 (전자공시용)                |
| `year`                       | ✅  | `Integer`    | 사업연도                            |
| `reprt_code`                 | ❌  | `String(6)`  | 보고서 코드 (11011=1분기, 11014=사업보고서) |
| `current_assets`             | ❌  | `BigInteger` | 유동자산                            |
| `non_current_assets`         | ❌  | `BigInteger` | 비유동자산                           |
| `current_liabilities`        | ❌  | `BigInteger` | 유동부채                            |
| `non_current_liabilities`    | ❌  | `BigInteger` | 비유동부채                           |
| `total_equity`               | ❌  | `BigInteger` | 자본총계                            |
| `revenue`                    | ❌  | `BigInteger` | 매출액                             |
| `cost_of_sales`              | ❌  | `BigInteger` | 매출원가                            |
| `gross_profit`               | ❌  | `BigInteger` | 매출총이익                           |
| `other_comprehensive_income` | ❌  | `BigInteger` | 기타포괄손익                          |
| `net_income`                 | ❌  | `BigInteger` | 당기순이익                           |


### kospi200_weekly

| 컬럼명            | PK | 데이터 타입       | 설명     |
| -------------- | -- | ------------ | ------ |
| `code`         | ✅  | `String(12)` | 종목 코드  |
| `date`         | ✅  | `Date`       | 주간 기준일 |
| `open`         | ❌  | `BigInteger` | 시가     |
| `high`         | ❌  | `BigInteger` | 고가     |
| `low`          | ❌  | `BigInteger` | 저가     |
| `close`        | ❌  | `BigInteger` | 종가     |
| `volume`       | ❌  | `BigInteger` | 거래량    |
| `trade_amount` | ❌  | `BigInteger` | 거래대금   |

### kospi200_daily

| 컬럼명            | PK | 데이터 타입       | 설명     |
| -------------- | -- | ------------ | ------ |
| `code`         | ✅  | `String(10)` | 종목 코드  |
| `date`         | ✅  | `Date`       | 일간 기준일 |
| `open`         | ❌  | `BigInteger` | 시가     |
| `high`         | ❌  | `BigInteger` | 고가     |
| `low`          | ❌  | `BigInteger` | 저가     |
| `close`        | ❌  | `BigInteger` | 종가     |
| `volume`       | ❌  | `BigInteger` | 거래량    |
| `trade_amount` | ❌  | `BigInteger` | 거래대금   |

### kospi200_meta

| 컬럼명             | PK | 데이터 타입       | 설명     |
| --------------- | -- | ------------ | ------ |
| `code`          | ✅  | `String(12)` | 종목 코드  |
| `face_value`    | ❌  | `Integer`    | 액면가    |
| `listed_shares` | ❌  | `BigInteger` | 상장주식 수 |
| `capital`       | ❌  | `Integer`    | 자본금    |

### ndx_financial

| 컬럼명      | PK | 데이터 타입       | 설명                    |
| -------- | -- | ------------ | --------------------- |
| `ticker` | ✅  | `String(10)` | 티커 (예: AAPL)          |
| `date`   | ✅  | `Date`       | 보고서 기준일               |
| `label`  | ✅  | `String(64)` | 항목명 (예: `net_income`) |
| `value`  | ❌  | `Float`      | 항목 값                  |
| `year`   | ❌  | `Integer`    | 사업연도                  |

### ndx_weekly

| 컬럼명           | PK | 데이터 타입           | 설명     |
| ------------- | -- | ---------------- | ------ |
| `code`        | ✅  | `String(10)`     | 티커     |
| `date`        | ✅  | `Date`           | 주간 기준일 |
| `close`       | ❌  | `Numeric(10, 2)` | 종가     |
| `open`        | ❌  | `Numeric(10, 2)` | 시가     |
| `high`        | ❌  | `Numeric(10, 2)` | 고가     |
| `low`         | ❌  | `Numeric(10, 2)` | 저가     |
| `acml_volume` | ❌  | `Numeric(20, 2)` | 누적 거래량 |


### ndx_meta

| 컬럼명             | PK | 데이터 타입       | 설명     |
| --------------- | -- | ------------ | ------ |
| `ticker`        | ✅  | `String(10)` | 티커     |
| `face_value`    | ❌  | `BigInteger` | 액면가    |
| `listed_shares` | ❌  | `BigInteger` | 상장주식 수 |
| `capital`       | ❌  | `BigInteger` | 자본금    |
| `market_cap`    | ❌  | `BigInteger` | 시가총액   |



---
