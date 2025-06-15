# 📊 NASDAQ / KOSPI 데이터 수집기

주요 글로벌·국내 지수(NASDAQ-100, KOSPI200)의 **시계열 데이터 / 재무제표 / 메타정보**를 수집·저장하는 CLI 기반 통합 수집기입니다.

---

## 🔧 구성 요소

- **주가 시계열** (주간 단위, OHLCV)
- **재무 데이터** (손익계산서, 재무상태표 등)
- **기업 메타정보** (섹터, CIK 등)

> 백엔드는 SQLAlchemy 기반 RDB에 저장됩니다.

---

## 🗂️ 데이터셋 종류

| Dataset 이름 | 설명 |
|--------------|------|
| `nasdaq-weekly` | NASDAQ-100 종목 주간 시계열 데이터 |
| `kospi200-weekly` | KOSPI200 종목 주간 시계열 데이터 |
| `nasdaq-financial` | 미국 상장사 재무제표 (10-K/10-Q 기반) |
| `kospi-financial` | 국내 상장사 재무제표 (전자공시 기반) |
| `nasdaq-meta` | NASDAQ 종목의 섹터, 기업명, CIK 등 메타정보 |

---

## 🚀 실행 방법

```bash
python nasdaq_collector.py --dataset <데이터셋> --mode <작업모드> [--tickers A B C] [--config path/to/config.json]
