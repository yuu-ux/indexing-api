import sys
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from colorama import init, Fore, Style
from dotenv import load_dotenv
load_dotenv()
init(autoreset=True)

# ダウンロードしたサービスアカウントキーのパス
KEY_FILE = os.getenv('KEY_FILE')

# 認証情報の設定
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE,
    scopes=['https://www.googleapis.com/auth/indexing']
)

# APIクライアントの作成
service = build('indexing', 'v3', credentials=credentials)

# コマンドライン引数からURLリストを取得
# urls = sys.argv[1:]
# 配列で渡す
urls = [

]

if not urls:
    print("Usage: python script.py <url1> <url2> ...")
    sys.exit(1)

# 各URLに対してリクエストを送信するループ
for url in urls:
    # 各URLについてリクエストを構築
    body = {
        'url': url,
        'type': 'URL_UPDATED'
    }
    
    try:
        # リクエストの送信
        response = service.urlNotifications().publish(body=body).execute()
        print(f'{Fore.GREEN}Successfully indexed: {url}')
        print(response)
    except HttpError as err:
        print(f'{Fore.RED}Failed to index: {url}')
        print(f'{Fore.YELLOW}Error code: {err.resp.status}')
        print(f'{Fore.YELLOW}Error details: {err.content.decode("utf-8")}')
    except Exception as e:
        print(f'{Fore.RED}Failed to index: {url}')
        print(f'{Fore.YELLOW}Unexpected error: {e}')

