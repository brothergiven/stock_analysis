from datetime import datetime
import requests
import pandas as pd
from pykrx import stock

def get_company_static_info(_env, headers, stock_code, name, market) -> dict:
    """
    
    """
    headers['tr_id'] = 'FHKST01010100'
    headers['custtype'] = 'P'
    url = f"{_env.my_url}/uapi/domestic-stock/v1/quotations/inquire-price"
    params = {
        "fid_cond_mrkt_div_code": "J" if market == "KOSPI" or market == "KOSDAQ" else "NX" , 
        "fid_input_iscd": stock_code
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if response.status_code == 200 and data['rt_cd'] == "0":
        print(f"[조회 성공] {stock_code} / 상태코드: {response.status_code} ")   
        out = data["output"]
        if stock_code == "278990":
          print(out)  
        return {
            "code": out.get("stck_shrn_iscd", stock_code), # 종목코드
            "name": name, # 종목 명
            "market": out.get("rprs_mrkt_kor_name", market), # 대표 시장 명 
            "industry": out.get("bstp_kor_isnm", ""), # 업종 명 
            "capital": int(out["cpfn"]) * 100000000, # 자본금 (원)
            "shares": int(out["lstn_stcn"]), # 상장 주식 수 
            "fiscal_month": int(out["stac_month"]), # 결산 월 (1~12)
            "created_at": datetime.now().replace(microsecond=0),
            "updated_at": datetime.now().replace(microsecond=0)
        }
    else:        
        print(f"[조회 실패] {stock_code} / 상태코드: {response.status_code} / 응답: {data}")        
        return None
    
def parse_capital(capital_str):
    if not capital_str:
        return 0
    try:
        if "억" in capital_str:
            return int(float(capital_str.replace(" 억", "").replace(",", "")) * 100_000_000)
        elif "조" in capital_str:
            return int(float(capital_str.replace(" 조", "").replace(",", "")) * 1_0000_0000_0000)
        else:
            return int(capital_str.replace(",", ""))
    except Exception as e:
        print(f"[자본금 파싱 오류] '{capital_str}' → {e}")
        return 0

def get_all_listed_stocks() -> pd.DataFrame:
    """
    모든 상장 종목 코드와 종목명을 가져온다.
    
    Returns:
        pd.DataFrame: 종목코드(code), 종목명(name), 시장구분(market)
    """
    today = datetime.today().strftime("%Y%m%d")
    # KOSPI 전체 종목
    kospi = stock.get_market_ticker_list(today, market="KOSPI")
    kospi_df = pd.DataFrame([(ticker, stock.get_market_ticker_name(ticker), "KOSPI") for ticker in kospi],
                            columns=["code", "name", "market"])

    # KOSDAQ 전체 종목
    kosdaq = stock.get_market_ticker_list(today, market="KOSDAQ")
    kosdaq_df = pd.DataFrame([(ticker, stock.get_market_ticker_name(ticker), "KOSDAQ") for ticker in kosdaq],
                            columns=["code", "name", "market"])
    
    # KONEX 전체 종목
    konex = stock.get_market_ticker_list(today, market="KONEX")
    konex_df = pd.DataFrame([(ticker, stock.get_market_ticker_name(ticker), "KONEX") for ticker in konex],
                            columns=["code", "name", "market"])

    tickers_df = pd.concat([kospi_df, kosdaq_df, konex_df], ignore_index=True)

    return tickers_df