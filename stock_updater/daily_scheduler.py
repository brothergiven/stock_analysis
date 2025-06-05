import threading
import schedule
import time
from datetime import datetime
from kospi200_updater import Kospi200Updater
from nasdaq_updater import NasdaqDataUpdater
import sys, json, os
from dataclasses import dataclass


@dataclass
class Config:
    DATABASE_URL: str
    API_DELAY: float
    MAX_RETRIES: int
    
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





def run_daily_job():
    def job():
        print(f"[{datetime.now()}] Starting daily update job...")
        config_data = load_config()
        config = create_config_from_file(config_data)
        kospi_updater = Kospi200Updater(config)
        kospi_updater.fetch_and_store_daily()
        
        ndx_updater = NasdaqDataUpdater(config)
        ndx_updater.fetch_and_store_daily()

        print(f"[{datetime.now()}] Daily update job completed.")

    return job

# 한국장 마감 16:00 기준 실행
schedule.every().day.at("16:00").do(run_daily_job())

# 미국장 마감 06:00 (한국 시간 기준) 실행
schedule.every().day.at("06:00").do(run_daily_job())

def run_scheduler():
    print(f"[{datetime.now()}]  Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(30)  # 30초마다 확인

if __name__ == "__main__":
    run_scheduler()
