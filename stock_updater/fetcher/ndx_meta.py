import requests
import pandas as pd


url_suffix = "/uapi/overseas-price/v1/quotations/price-detail"


def get_ndx_meta(env, stock_code: str, headers) -> dict:
    """
    나스닥 종목의 메타 정보(상장주수, 액면가, 자본금, 시가총액)를 가져온다.
    """
    headers['tr_id'] = 'HHDFS76200200'
    headers['custtype'] = 'P'

    url = env.my_url + url_suffix
    params = {
        "EXCD": "NAS",
        "SYMB": stock_code
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200 and data.get('rt_cd') == '0':
        output = data.get("output", {})
        meta_info = {
            "ticker": stock_code,
            "face_value": float(output.get("e_parp", "0.0")),     # 액면가
            "listed_shares": int(output.get("shar", 0)),     # 상장주수
            "capital": int(output.get("cpfn", 0)),                # 자본금
            "market_cap": int(output.get("tomv", 0))          # 시가총액
        }
        return meta_info
    else:
        print(f"[조회 실패] {stock_code} / 코드: {response.status_code} / 응답: {data}")
        return {}
