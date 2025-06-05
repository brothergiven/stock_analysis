import requests
from datetime import datetime, timedelta
import pandas as pd

url_suffix = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"

def get_kospi200_meta(env, stock_code, headers):


    headers['tr_id'] = 'FHKST03010100'
    headers['custtype'] = 'P'

    url = env.my_url + url_suffix
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code,
        'fid_input_date_1': f'20250101',
        'fid_input_date_2': f'20251231',
        'fid_period_div_code': 'W',
        'fid_org_adj_prc': 0
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    try:
        if response.status_code == 200 and data['rt_cd'] == "0":
            meta_raw = data['output1']
            meta_parsed = {
                "code": meta_raw["stck_shrn_iscd"],
                "face_value": int(meta_raw["stck_fcam"]),
                "listed_shares": int(meta_raw["lstn_stcn"]),
                "capital": int(meta_raw["cpfn"])
            }
            return meta_parsed
        else:
            print(f"[메타 조회 실패] {stock_code} / 상태코드: {response.status_code} / 응답: {data}")
            return None
    except Exception as e: 
        print(f"[오류 발생] : {e}")

def get_kospi200_weekly_data(env, stock_code, headers, start_date, end_date):

    
    headers['tr_id'] = 'FHKST03010100'
    headers['custtype'] = 'P'

    def chunk_date_ranges(start: datetime, end: datetime):
        """최대 1년 단위로 날짜 범위 분할"""
        ranges = []
        cursor = start
        while cursor <= end:
            chunk_end = min(cursor + timedelta(days=365), end)
            ranges.append((cursor, chunk_end))
            cursor = chunk_end + timedelta(days=1)
            
        return ranges

    start_dt = datetime.strptime(start_date, "%Y%m%d")
    end_dt = datetime.strptime(end_date, "%Y%m%d")
    date_chunks = chunk_date_ranges(start_dt, end_dt)

    total_df = pd.DataFrame()

    for s, e in date_chunks:
        s_str = s.strftime("%Y%m%d")
        e_str = e.strftime("%Y%m%d")

        url = env.my_url + url_suffix

        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stock_code,
            'fid_input_date_1': s_str,
            'fid_input_date_2': e_str,
            'fid_period_div_code': 'W',
            'fid_org_adj_prc': 0
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200 and data['rt_cd'] == "0":
            print(f"[조회 성공] {s_str} ~ {e_str}")
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
                total_df = pd.concat([total_df, weekly_df], ignore_index=True)
        else:
            print(f"[조회 실패] {stock_code}: {s_str} ~ {e_str} / 코드: {response.status_code}, 응답: {data}")
            print(params)
    
    return total_df

def get_kospi200_daily(env, stock_code, headers, date):
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code,
        'fid_input_date_1': date,
        'fid_input_date_2': date,
        'fid_period_div_code': 'D',  
        'fid_org_adj_prc': 0
    }
    url = env.myurl + url_suffix
    response = requests.get(url, headers=headers, params=params)
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
            print(f"[일간 조회 실패] {stock_code}: {date} / 코드: {response.status_code}, 응답: {data}")
            print(params)
    return daily_df