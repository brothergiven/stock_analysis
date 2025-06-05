from collections import namedtuple
import requests, json, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()



MY_URL = "https://openapi.koreainvestment.com:9443"
MY_APP= os.getenv("MY_APP")
MY_SEC= os.getenv("MY_SEC")

#계좌번호 앞 8자리
MY_ACCT="43016876"
#계좌번호 뒤 2자리
MY_PROD= "01"


KISEnv = namedtuple("KISEnv", [
    "my_app",       # 앱 키
    "my_sec",       # 시크릿 키
    "my_acct",      # 계좌번호
    "my_prod",      # 계좌 상품 코드
    "my_token",     # 발급된 토큰
    "my_url"        # 호출할 API URL
])


_TRENV = None
_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "charset": "UTF-8",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


TOKEN_PATH = "./.token.json"

def save_token(token: str, expired_at): # 토큰을 JSON 파일로 저장
    # expired_at이 datetime이면 문자열로 변환, 아니면 그대로 저장
    if isinstance(expired_at, datetime):
        expired_at_str = expired_at.isoformat()
    else:
        expired_at_str = expired_at  # 이미 문자열이면 그대로 사용

    data = {
        "token": token,
        "expired_at": expired_at_str
    }

    with open(TOKEN_PATH, "w") as f:
        json.dump(data, f)



def load_token(): # JSON 파일로 저장된 토큰을 로드 
    if not os.path.exists(TOKEN_PATH):
        return None, None
    with open(TOKEN_PATH, "r") as f:
        data = json.load(f)

    access_token = data.get("token")
    expired_at_str = data.get("expired_at")

    try:
        # datetime 객체로 파싱 가능하면 파싱
        expired_at = datetime.fromisoformat(expired_at_str)
    except (ValueError, TypeError):
        # iso 형식이 아니거나 None이면 그대로 문자열로 반환
        expired_at = expired_at_str

    return access_token, expired_at
    

def is_token_valid(expired_at):
    return expired_at > datetime.now() 





def getTREnv():
    """ 외부에서 환경 객체 접근 """
    return _TRENV


def get_headers():
    """ 외부에서 headers 가져오기 """
    return _HEADERS


def auth():
    """ 토큰 발급 + 환경 설정 """
    global _TRENV
    global _HEADERS

    token, expired_at = load_token()

    # print(token)
    # print(expired_at)

    if token and is_token_valid(expired_at):
        print("[TOKEN 재사용]")
    else:
        print("[TOKEN 재발급]")
        url = f"{MY_URL}/oauth2/tokenP"
        body = {
            "grant_type": "client_credentials",
            "appkey": MY_APP,
            "appsecret": MY_SEC
        }

        res = requests.post(url, headers=_HEADERS, data=json.dumps(body))
        if res.status_code != 200:
            raise Exception(f"토큰 발급 실패: {res.status_code} - {res.text}")

        data = res.json()

        token = data['access_token']
        expired_at = data["access_token_token_expired"]

    # 환경 객체 생성
    _TRENV = KISEnv(
        my_app=MY_APP,
        my_sec=MY_SEC,
        my_acct=MY_ACCT,
        my_prod=MY_PROD,
        my_token=f"Bearer {token}",
        my_url=MY_URL
    )

    # 헤더 업데이트
    _HEADERS["authorization"] = _TRENV.my_token
    _HEADERS["appkey"] = _TRENV.my_app
    _HEADERS["appsecret"] = _TRENV.my_sec

    save_token(token, expired_at)
    print("[Token 발급 완료]")
    return _TRENV




# 테스트용 CLI 실행
if __name__ == "__main__":
    env = auth()
    print("Token:", env.my_token)
    print("Account:", env.my_acct)