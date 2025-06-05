import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os



def fetch_dart_financials(corp_code: str, year: int, reprt_code: str = "11014", fs_div: str = "CFS"):
    """
    DART에서 지정한 기업의 단일 재무제표를 JSON으로 가져온다.
    :param corp_code: DART 고유 기업 코드
    :param year: 사업연도 (예: 2023)
    :param reprt_code: 보고서 코드 (11011~11014)
    :param fs_div: 연결(CFS) 또는 개별(OFS)
    :return: 항목별 dict 리스트
    """
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"  # XML → JSON
    params = {
        "crtfc_key": os.getenv("DART_KEY"),
        "corp_code": corp_code,
        "bsns_year": str(year),
        "reprt_code": reprt_code,
        "fs_div": fs_div
    }

    res = requests.get(url, params=params)
    data = res.json()

    if data.get("status") == "013":  # '해당 공시 없음'
        print(f"[!] No data for corp_code={corp_code}, year={year}, reprt_code={reprt_code}")
        return []

    return data.get("list", [])

    
def extract_key_accounts(financials):
    """
    키워드 후보 기반 주요 재무 항목 추출
    """
    candidate_keywords = {
        "current_assets": ["유동자산"],
        "non_current_assets": ["비유동자산", "비유동 자산"],
        "current_liabilities": ["유동부채"],
        "non_current_liabilities": ["비유동부채", "비유동 부채"],
        "total_equity": ["자본총계", "총자본"],
        "revenue": ["매출액", "수익"],
        "cost_of_sales": ["매출원가", "제품매출원가", "상품매출원가", "용역원가", "원가"],
        "gross_profit": ["매출총이익", "총이익"],
        "other_comprehensive_income": ["기타포괄손익", "기타포괄이익"],
        "net_income": ["당기순이익", "순이익", "당기순손익"]
    }

    result = {}
    for item in financials:
        account_name = item.get("account_nm", "")
        for key, candidates in candidate_keywords.items():
            if key not in result and any(c in account_name for c in candidates):
                try:
                    value = int(item["thstrm_amount"].replace(",", ""))
                except:
                    value = None
                result[key] = value
                break  # 한 번 매칭되면 더 이상 검사 안함
    return result


if __name__ == '__main__':
    load_dotenv()
    data = fetch_dart_financials(corp_code="00126380", year = 2022)
    key_data = extract_key_accounts(data)
    print("=== 추출된 주요 재무 항목 ===")
    for k, v in key_data.items():
        print(f"{k}: {v if v is not None else 'N/A'}")