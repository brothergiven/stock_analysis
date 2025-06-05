import requests
import pandas as pd
from datetime import datetime, timedelta

url_suffix = "/uapi/overseas-price/v1/quotations/inquire-daily-chartprice"


def get_ndx_weekly(env, stock_code, headers, start_date: str, end_date: str):
    headers['tr_id'] = 'FHKST03030100'
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
            "FID_COND_MRKT_DIV_CODE": "N",
            "FID_INPUT_DATE_1": s_str,
            "FID_INPUT_DATE_2": e_str,
            "FID_PERIOD_DIV_CODE": 'W',
            "FID_INPUT_ISCD": stock_code
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200 and data['rt_cd'] == "0":
            weekly_raw = data['output2']
            weekly_df = pd.DataFrame(weekly_raw)
            if not weekly_df.empty:
                weekly_df = weekly_df[['stck_bsop_date', 'ovrs_nmix_prpr', 'ovrs_nmix_oprc',
                                       'ovrs_nmix_hgpr', 'ovrs_nmix_lwpr', 'acml_vol']]
                weekly_df = weekly_df.rename(columns={
                    "stck_bsop_date": "date",
                    "ovrs_nmix_prpr": "close",
                    "ovrs_nmix_oprc": "open",
                    "ovrs_nmix_hgpr": "high",
                    "ovrs_nmix_lwpr": "low",
                    "acml_vol": "acml_volume"
                })
                total_df = pd.concat([total_df, weekly_df], ignore_index=True)
        else:
            print(f"[조회 실패] {stock_code}: {s_str} ~ {e_str} / 코드: {response.status_code}, 응답: {data}")
    
    return total_df