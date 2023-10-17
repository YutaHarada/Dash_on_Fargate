# import文
import sys
from module.boto3 import get_csv

import pandas as pd
import numpy as np

from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

# boto3用認証情報の取得
credentials = sys.argv
# DataFrameオブジェクトの生成
df = pd.read_csv(get_csv(credentials))

# ドロップダウンに表示するラベルと紐づく値を作成
city_names = [{'label': city, 'value': city} for city in df['name'].unique()]

# ページレイアウトの設定

# サイドバーの設定
sidebar = html.Div([
    html.Div([
        html.H2([
            "5days",
            html.Br(),
            "Information"
    ]),
    ], style={'font-weight': 700,'margin-bottom': '20px','margin-top': '20px'}),
    
    html.Hr(style={'color': 'midnightblue', 'borderWidth': '2px', 'borderStyle': 'dashed'}),
    
    html.Div([
        html.P('都市名を選択してください。'),
        html.Div(
            dcc.Dropdown(
                id='dropdown_1', 
                options = city_names, 
                value = '東京都',
                multi=False,
                placeholder='都市名'
            ),
            style={'width': '40%', 'display': 'inline-block','margin-right': 10}
        )
    ])
])

# コンテンツの設定
content = html.Div([
    html.Div([
        dcc.Graph(id='output-table',style={'width': '150vh', 'height': '155vh'})
    ])
])

# Bootstrapのグリッドシステムによって画面を分割する。(縦方向に12分割)
layout = dbc.Container(
    [
        dbc.Row(
            [
                # 12分割された区画を3:9に分ける。
                dbc.Col(sidebar, width=2, className='bg-light'),
                dbc.Col(content, width=10)
                ],
            style={"height": "100vh"}
            ),
        ],
    fluid=True,
)

# コールバック関数の設定
@callback(
    Output('output-table', 'figure'),
    Input('dropdown_1', 'value'))
def update_graph(input_value):
    # 表示項目の指定
    items = ['天気', '降水確率(%)', '最高気温(℃)', '最低気温(℃)', '湿度(%)', '気圧(hPa)']
    # 入力値に応じたDataFrameを抽出
    df_input_city = df.query('name == @input_value')
    # 表示対象日付の取得
    date_list = df_input_city['jst_date'].unique()
    
    # 5日分のテーブルを作成
    figure = make_subplots(rows=5, cols=1,
                           subplot_titles=tuple(date_list),
                           specs=[[{"type": "table"}]]*5,
                           vertical_spacing=0.05)
    
    for i, date in enumerate(date_list, 1):
        # 日付に応じたDataFrameを抽出
        df_date = df_input_city.query('jst_date == @date')
        # 表示時刻を取得
        time_list = np.insert(df_date['jst_time'].unique(), 0, '気象情報')
        # 列数の格納
        n_columns = len(time_list)
        # 気象情報を取得
        w_info = np.insert(df_date.iloc[:,5:-2].values, 0, items, axis=0)
        # 天気予報テーブルの作成
        table = go.Table(
            # カラムの順番を設定し各カラムの幅を調整する
            columnorder = [x for x in range(1, n_columns +1)],
            columnwidth = [40]+[50]*(n_columns -1) ,
            # ヘッダー(列名)の指定
            header=dict(
                values=time_list,
                line_color='darkslategray',
                fill_color='midnightblue',
                align='center',
                font=dict(color='white', size=14),
                height=40
            ),
            # テーブルの中身の指定
            cells=dict(
                values=w_info,
                line_color='darkslategray',
                fill=dict(color=['midnightblue']+['aliceblue']*(n_columns -1)),
                align='center',
                font=dict(color=['white']+['steelblue']*(n_columns -1), size=14),
                height=30
            )
        )
        figure.add_trace(table, row=i, col=1)

    # テーブルのタイトルを設定
    title_variable = input_value + 'の天気'
    figure.update_layout(title = dict(text = f'<b>{title_variable}', 
                                      font = dict(size=26, color='steelblue')),
                        margin={'l': 40, 'b': 30, 't': 70, 'r': 40})

    return figure

