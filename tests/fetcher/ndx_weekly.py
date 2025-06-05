import sys, time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
import requests
import pandas as pd
from kis_auth import auth, getTREnv, get_headers

url_suffix = "/uapi/overseas-price/v1/quotations/inquire-daily-chartprice"

def get_ndx_weekly(env, stock_code, headers, year):
    headers['tr_id'] = 'FHKST03030100'
    headers['custtype'] = 'P'

    url = env.my_url+url_suffix
    params = {
        "FID_COND_MRKT_DIV_CODE": "N",
        "FID_INPUT_DATE_1": f"{year}0101",
        "FID_INPUT_DATE_2": f"{year}1231",
        "FID_PERIOD_DIV_CODE": 'W',
        "FID_INPUT_ISCD" : stock_code
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    
    if response.status_code == 200 and data['rt_cd'] == "0":
        print(f"[조회 성공] {stock_code} / 상태코드: {response.status_code} ")  

        weekly_raw = data['output2']
        weekly_df = pd.DataFrame(weekly_raw)
        if not weekly_df.empty:
            weekly_df = weekly_df[['stck_bsop_date', 'ovrs_nmix_prpr', 'ovrs_nmix_oprc', 'ovrs_nmix_hgpr', 'ovrs_nmix_lwpr', 'acml_vol']]

            weekly_df = weekly_df.rename(columns={
                "stck_bsop_date": "date",
                "ovrs_nmix_prpr": "close",
                "ovrs_nmix_oprc": "open",
                "ovrs_nmix_hgpr": "high",
                "ovrs_nmix_lwpr": "low",
                "acml_vol": "acml_volume"
            })

        return weekly_df

    else:
        print(f"[조회 실패] {stock_code} / 상태코드: {response.status_code} / 응답: {data}")        
        return None
    
if __name__ == "__main__":
    auth()
    env = getTREnv()    
    headers = get_headers()
    data = get_ndx_weekly(env, "AAPL", headers, 2024)

    print(data)