# import文
import boto3
import os

def get_csv(credentials : list):
    '''S3からcsvファイルを取得する関数
    
    parameter
    =========
    credentials : S3にアクセスするための認証情報のリスト
    
    return
    =========
    csv_file : S3から取得してきたcsvファイル
    '''
    
    s3 = boto3.client('s3', 
                      aws_access_key_id=credentials[1], 
                      aws_secret_access_key=credentials[2],
                      aws_session_token=credentials[3])
    
    # csv読み取り対象バケット名の取得（環境変数に設定済み）
    bucket = os.getenv('BUCKET_NAME')
    # DataFrameの取得
    csv_file = s3.get_object(Bucket=bucket, Key='dataframe.csv')['Body']
    
    return csv_file