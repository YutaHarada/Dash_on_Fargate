# import文
import boto3
import time
import os
from io import BytesIO
import pandas as pd

# 実行クエリの設定
query = "SELECT * FROM dashboard_view;"

# 環境変数の読み込み
athena_result_output = os.environ['OutputLocation']
in_bucket = os.environ['In_Bucket']
in_folder = os.environ['In_Folder']
out_bucket = os.environ['Out_Bucket']

# clientの取得
athena = boto3.client('athena')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    # Athenaクエリの実行
    response = athena.start_query_execution(
        # 実行対象のクエリの設定
        QueryString=query,
        # クエリを実行するデータベースの設定
        QueryExecutionContext={
            'Database': 'default'
        },
        # クエリの実行結果の格納先の設定
        ResultConfiguration={
            'OutputLocation': athena_result_output,
        },
        # ワークグループの設定
        WorkGroup='open-weaher'
    )
    # 実行IDの取得
    exec_id = response['QueryExecutionId']
    # クエリの実行ステータスの取得
    status = athena.get_query_execution(QueryExecutionId=exec_id)['QueryExecution']['Status']
    
    # クエリが実行完了するまで待機
    while status['State'] not in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        time.sleep(5)
        status = athena.get_query_execution(QueryExecutionId=exec_id)['QueryExecution']['Status']
        
    # 実行結果をDataFrame型で出力する    
    if status['State'] == 'SUCCEEDED':
        body_in = s3.get_object(Bucket=in_bucket, Key=f'{in_folder}/{exec_id}.csv')['Body']
        
        # csvファイルからDataFrameの作成 
        df = pd.read_csv(body_in)
        # DataFrameを一部加工
        df.replace({'name':{'Kōchi-shi': '高知市', '仙台': '仙台市'}}, inplace=True)
        
        # DataFrameをcsv化してs3に格納
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        body_out = buffer.getvalue()
        s3.put_object(Bucket=out_bucket, Key='dataframe.csv', Body=body_out)
    
        return {
            'status': 'SUCCEEDED',
            'body': 'DataFrame successfully stored in S3.'
        }
    
    return {
            'status': status['State'],
            'body': 'Failed to stored DataFrame.'
            }