import sys, time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from datetime import datetime
import requests
import pandas as pd
from kis_auth import auth, getTREnv, get_headers

url_suffix = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"

def get_kospi200_weekly(env, stock_code, headers, year):
    headers['tr_id'] = 'FHKST03010100'
    headers['custtype'] = 'P'

    url = env.my_url+url_suffix
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code,
        'fid_input_date_1': f'{year}0101',
        'fid_input_date_2': f'{year}1231',
        'fid_period_div_code': 'W',
        'fid_org_adj_prc': 0
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if response.status_code == 200 and data['rt_cd'] == "0":
        print(f"[조회 성공] {stock_code} / 상태코드: {response.status_code} ")  
        meta_raw = data['output1']
        meta_parsed = {
            "code": meta_raw["stck_shrn_iscd"],
            "face_value": int(meta_raw["stck_fcam"]),
            "listed_shares": int(meta_raw["lstn_stcn"]),
            "capital": int(meta_raw["cpfn"]),
            "market_cap": int(meta_raw["hts_avls"]),
            "per": float(meta_raw["per"]),
            "eps": float(meta_raw["eps"]),
            "pbr": float(meta_raw["pbr"]),
            "loan_balance_ratio": float(meta_raw["itewhol_loan_rmnd_ratem name"])
        }

        weekly_raw = data['output2']
        weekly_df = pd.DataFrame(weekly_raw)
        if not weekly_df.empty:
            weekly_df = weekly_df[['stck_bsop_date', 'stck_clpr', 'stck_oprc', 'stck_hgpr', 'stck_lwpr', 'acml_vol', 'acml_tr_pbmn']]

            weekly_df = weekly_df.rename(columns={
                "stck_bsop_date": "date",
                "stck_clpr": "close",
                "stck_oprc": "open",
                "stck_hgpr": "high",
                "stck_lwpr": "low",
                "acml_vol": "volume",
                "acml_tr_pbmn": "trade_amount"
            })

        return pd.DataFrame([meta_parsed]), weekly_df

    else:
        print(f"[조회 실패] {stock_code} / 상태코드: {response.status_code} / 응답: {data}")        
        return None
    
if __name__ == "__main__":
    auth()
    env = getTREnv()    
    headers = get_headers()
    data = get_kospi200_weekly(env, "005930", headers, 2024)

    print(data[0])
    print(len(data[1]))
