# KOSPI200 종목 fetch (재무제표)

import sys, time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
import requests
from dotenv import load_dotenv
import pandas as pd


url = "https://opendart.fss.or.kr/api/fnlttSinglIndx.json"
load_dotenv()

params = {
    "crtfc_key" :os.getenv("DART_KEY")
}

li = [('2023', '11014'), ('2023', '11011'), ('2024', '11011'), ('2024', '11012'), ('2024', '11013'), ('2024', '11014') ]
codes = ['M210000', 'M220000', 'M230000', 'M240000']




def fetch_finstmt(corp_code, year, reprt, idx_cl):
    """
    corp_code: 회사 코드
    year: 연도
    reprt: 분기 
    idx_cl : 지표 ('M210000', 'M220000', 'M230000', 'M240000')
    """
    params['corp_code'] = corp_code
    params['bsns_year'] = year
    params['reprt_code'] = reprt
    params['idx_cl_code'] = idx_cl

    response = requests.get(url, params)
    try:
        data = response.json()
    except ValueError as e:
        print("JSONDecodeError 발생: 응답 본문이 JSON이 아님")
        data = None
    if response.status_code == 200 and data['status'] == '000':
        li = data['list']
        d = {}
        d['date'] = li[0]['stlm_dt']
        for elm in li:
            if 'idx_nm' in elm and 'idx_val' in elm:
                d[elm['idx_nm']] = elm['idx_val']
        print(f"[조회 성공] {corp_code} / 상태코드: {response.status_code} ")  
        return d
    
    else:
        print(f"[조회 실패] {corp_code} / 상태코드: {response.status_code} / 응답: {data['message']}")        
        return None


if __name__ == "__main__":
    print(fetch_finstmt("00126380", "2024", "11011", "M240000"))