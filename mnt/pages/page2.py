# import文
import sys
from module.boto3 import get_csv

import pandas as pd

from dash import dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc

# boto3用認証情報の取得
credentials = sys.argv
# DataFrameオブジェクトの生成
df = pd.read_csv(get_csv(credentials))
df['datetime'] = df['jst_date'] + ' ' + df['jst_time']

# ドロップダウンに表示するラベルと紐づく値を作
city_names = [{'label': city, 'value': city} for city in df['name'].unique()]

# ページレイアウトの設定

# サイドバーの設定
sidebar = html.Div([
    html.Div([
        html.H2([
            "Temperature",
            html.Br(),
            "Trends"
    ]),
    ], style={'font-weight': 700,'margin-bottom': '20px','margin-top': '20px'}),
    
    html.Hr(style={'color': 'midnightblue', 'borderWidth': '2px', 'borderStyle': 'dashed'}),
    
    html.Div([
        html.P('都市名を選択してください。'),
        html.Div(
            dcc.Dropdown(
                id='dropdown_2', 
                options=city_names, 
                value = '東京都',
                multi=True,
                placeholder='都市名'
            ),
            style={'width': '100%', 'display': 'inline-block','margin-right': 10}
        )
    ])
])

# コンテンツの設定
content = html.Div([
    html.Div([
        dcc.Graph(id='output-line_1',style={'width': '150vh', 'height': '50vh'}),
        dcc.Graph(id='output-line_2',style={'width': '150vh', 'height': '50vh'})
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
    Output('output-line_1', 'figure'),
    Output('output-line_2', 'figure'),
    Input('dropdown_2', 'value'))
def update_graph(input_value):
    # 入力値に応じたDataFrameを抽出
    df_input_city = df.query('name in @input_value')
    
    figures = []
    y_values = ['temp_max', 'temp_min']
    titles = ['最高気温', '最低気温']
    colors = ['orangered', 'steelblue']
    
    for i in range(2):
        fig = px.line(df_input_city, 
                      x='datetime', 
                      y=y_values[i], 
                      color='name',
                      markers=True, 
                      hover_data = ['description'])
        
        # fig.update_traces(hovertemplate=None)
        
        fig.update_layout(title = dict(text = f'<b>{titles[i]}', 
                                      font = dict(size=26, color=colors[i])),
                          hovermode = 'x unified',
                          xaxis_title = '日時',
                          yaxis_title = '気温')
        
        figures.append(fig)

    return figures
