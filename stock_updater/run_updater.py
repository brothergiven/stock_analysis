"""
NASDAQ-100 주간 데이터 수집 실행 스크립트
"""
import sys
import json
import argparse
import os
from dotenv import load_dotenv
from nasdaq_updater import NasdaqDataUpdater, Config
from kospi200_updater import Kospi200Updater
from kospi_financial_updater import KospifinancialUpdater
from nasdaq_financial_updater import NasdaqFinancialUpdater
from kis_auth import auth
from nasdaq_meta_updater import NDXMetaUpdater
from util.cik_map import build_cik_map
from db.database import init_db
load_dotenv()  # .env 파일 로드

def load_config(config_path: str = "config.json") -> dict:
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] 설정 파일 없음: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"[ERROR] 설정 파일 오류: {config_path}")
        sys.exit(1)

def resolve_env_vars(value: str):
    if isinstance(value, str) and value.startswith("env:"):
        return os.getenv(value[4:])
    return value

def create_config_from_file(config_data: dict) -> Config:
    return Config(
        DATABASE_URL=resolve_env_vars(config_data['database']['url']),
        API_DELAY=config_data['api']['delay'],
        MAX_RETRIES=config_data['api']['max_retries']
    )

def main():
    parser = argparse.ArgumentParser(description='NASDAQ 데이터 수집기')
    parser.add_argument('--dataset', choices=['nasdaq-weekly', 'kospi200-weekly', 'nasdaq-financial', 'nasdaq-meta', 'kospi-financial'], required=True,
                        help='데이터셋 종류 선택')
    parser.add_argument('--mode', choices=['init', 'update', 'status'], required=False,
                        help='작업 모드 선택')
    parser.add_argument('--config', default='config.json', help='설정 파일 경로')
    parser.add_argument('--tickers', nargs='*', help='특정 종목만 업데이트')

    args = parser.parse_args()

    config_data = load_config(args.config)
    config = create_config_from_file(config_data)
    
    cik_map = build_cik_map()  # {ticker: cik} 

    init_db()
    auth()

    if args.dataset == 'nasdaq-weekly':
        updater = NasdaqDataUpdater(config)

        if args.mode == 'init':
            print("[NASDAQ 주간 초기 수집 시작]")
            updater.full_update()

        elif args.mode == 'update':
            if args.tickers:
                print(f"[선택 종목 업데이트] {', '.join(args.tickers)}")
                for ticker in args.tickers:
                    updater.update_ticker_data(ticker)
            else:
                print("[NASDAQ 주간 증분 업데이트 시작]")
                updater.incremental_update()

        elif args.mode == 'status':
            print("[데이터 현황 조회]")
            status = updater.get_data_status()
            print(f"{'종목':<8} {'데이터 수':<10} {'시작일':<12} {'종료일':<12}")
            print("-" * 50)
            for code, info in status.items():
                print(f"{code:<8} {info['record_count']:<10} {info['earliest_date']:<12} {info['latest_date']:<12}")
            total = sum(info['record_count'] for info in status.values())
            print(f"\n총 {len(status)}종목, {total:,}건 수집됨")
            
    elif args.dataset == 'kospi200-weekly':
        updater = Kospi200Updater(config)

        if args.mode == 'init':
            print("[KOSPI200 초기 수집 시작]")
            updater.full_update()

        elif args.mode == 'update':
            print("[KOSPI200 증분 업데이트 시작]")
            updater.incremental_update()

        elif args.mode == 'status':
            print("[KOSPI200 수집 현황]")
            status = updater.get_data_status()
            print(f"{'종목':<8} {'데이터 수':<10} {'시작일':<12} {'종료일':<12}")
            print("-" * 50)
            for code, info in status.items():
                print(f"{code:<8} {info['record_count']:<10} {info['earliest_date']:<12} {info['latest_date']:<12}")
            total = sum(info['record_count'] for info in status.values())
            print(f"\n총 {len(status)}종목, {total:,}건 수집됨")
            
    elif args.dataset == 'nasdaq-financial':
        updater = NasdaqFinancialUpdater(config, tickers=args.tickers)

        if args.mode == 'init':
            print("[NASDAQ 재무정보 초기 수집 시작]")
            updater.full_update()

        elif args.mode == 'update':
            print("[NASDAQ 재무정보 업데이트 시작]")
            updater.update()

        elif args.mode == 'status':
            print("[NASDAQ 재무정보 수집 현황]")
            updater.get_data_status()
    elif args.dataset == 'nasdaq-meta':
        updater = NDXMetaUpdater(config)
        print("[NASDAQ 메타정보 수집 시작]")
        updater.full_update()
        
    elif args.dataset == 'kospi-financial':
        updater = KospifinancialUpdater(config)
        
        if args.mode == 'init':
            print("[KOSPI200 재무정보 초기 수집 시작]")
            updater.full_update()
        elif args.mode == 'update':
            print("[KOSPI200 재무정보 업데이트 시작]")
            updater.incremental_update()
            
        
            
if __name__ == "__main__":
    main()
