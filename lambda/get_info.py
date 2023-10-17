# import文
import json
import boto3
import requests
import os
from datetime import datetime, timedelta, timezone

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')

# APIキーの指定
API_Key = os.environ['API_Key']
# 格納先のS3バケット名の指定
bucket_name = os.environ['Bucket_Name']

# S3クライアントを初期化
s3 = boto3.client('s3')

# 地域名別のリストを作成
loc_list = ['naha', 'kagoshima', 'fukuoka', 'hiroshima', 'kochi-shi', 'osaka', 'nagoya',\
            'kanazawa', 'yokohama', 'tokyo', 'niigata', 'sendai', 'sapporo', 'kushiro']

# Web APIのエンドポイントを指定
api_url = 'https://api.openweathermap.org/data/2.5/forecast'
params={
        ## 天気情報を取得する対象の都市名
        "q": "naha",
        "appid": API_Key,
        "units": "metric", # 摂氏で取得
        "lang": "ja"
        }


def lambda_handler(event, context):
    
    # 現在日付の取得（フォルダ作成用）
    today = datetime.now(JST).strftime("%Y/%m/%d")

    # 都市毎に天気予報情報を取得する
    for loc in loc_list:
        # Web APIからデータを取得
        params['q'] = loc
        response = requests.get(api_url,params=params)

        # レスポンスのステータスコードを確認
        if response.status_code == 200:
            
            # レスポンスのJSONデータを取得
            data = response.json()
            
            # S3にデータをアップロード
            object_key = f'{today}/{loc}.json'
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=json.dumps(data, sort_keys=True, ensure_ascii=False))
        
        else:
            return {
                'statusCode': response.status_code,
                'body': 'Failed to retrieve data from the API.'
            }

    return {
        'statusCode': 200,
        'body': f'Data successfully retrieved and stored in S3 with folder: {today}'
    }
