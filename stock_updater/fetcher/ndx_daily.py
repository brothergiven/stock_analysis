import pandas as pd
import requests

url_suffix ="uapi/domestic-stock/v1/quotations/inquire-daily-price"

def get_ndx_daily(env: dict, ticker: str, headers: dict, date) -> pd.DataFrame:
    params = {
        "fid_cond_mrkt_div_code": "U",  # U: NASDAQ
        "fid_input_iscd": ticker,
        "fid_input_date_1": date,
        "fid_input_date_2": date,
        "fid_period_div_code": "D",  # Daily
        "fid_org_adj_prc": "0"
    }
    url = env.myurl + url_suffix

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"[HTTP 오류] {response.status_code}")
        return None

    data = response.json()
    if response.status_code == 200 and data['rt_cd'] == "0":
        print(f"[일간 조회 성공] {date}")
        daily_raw = data['output2']
        daily_df = pd.DataFrame(daily_raw)

        if not daily_df.empty:
            daily_df = daily_df[['stck_bsop_date', 'stck_clpr', 'stck_oprc', 'stck_hgpr', 'stck_lwpr', 'acml_vol', 'acml_tr_pbmn']]
            daily_df = daily_df.rename(columns={
                "stck_bsop_date": "date",
                "stck_clpr": "close",
                "stck_oprc": "open",
                "stck_hgpr": "high",
                "stck_lwpr": "low",
                "acml_vol": "volume",
                "acml_tr_pbmn": "trade_amount"
            })
        else:
            print(f"[일간 조회 실패] {ticker}: {date} / 코드: {response.status_code}, 응답: {data}")
            print(params)
    return daily_df
