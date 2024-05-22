import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ダウンロードしたサービスアカウントキーのパス
KEY_FILE = 'ambient-scope-423207-c1-c4fcf9545008.json'

# 認証情報の設定
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE,
    scopes=['https://www.googleapis.com/auth/indexing']
)

# APIクライアントの作成
service = build('indexing', 'v3', credentials=credentials)

# コマンドライン引数からURLリストを取得
urls = sys.argv[1:]

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
        print(f'Successfully indexed: {url}')
        print(response)
    except HttpError as err:
        print(f'Failed to index: {url}')
        print(f'Error code: {err.resp.status}')
        print(f'Error details: {err.content.decode("utf-8")}')
    except Exception as e:
        print(f'Failed to index: {url}')
        print(f'Unexpected error: {e}')
