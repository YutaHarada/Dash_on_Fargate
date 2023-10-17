# import文
import sys
from module.boto3 import get_csv

import pandas as pd

from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

# boto3用認証情報の取得
credentials = sys.argv
# DataFrameオブジェクトの生成
df = pd.read_csv(get_csv(credentials))

# ドロップダウンに表示するラベルと紐づく値を作成
dates = [{'label': date, 'value': date} for date in df['jst_date'].unique()]
times = [{'label': time, 'value': time} for time in df['jst_time'].unique()]
# ページレイアウトの設定

# サイドバーの設定
sidebar = html.Div([
    html.Div([
        html.H2([
            "Wheather",
            html.Br(),
            "Map"
    ]),
    ], style={'font-weight': 700,'margin-bottom': '20px','margin-top': '20px'}),
    
    html.Hr(style={'color': 'midnightblue', 'borderWidth': '2px', 'borderStyle': 'dashed'}),
    
    html.Div([
        html.Div([
            html.P('1.日付を選択してください。'),
            html.Div(
                dcc.Dropdown(
                    id='dropdown_3_1', 
                    options = dates, 
                    # value = dates[0],
                    value = dates[0]['value'],
                    multi=False,
                    placeholder='日付'
                ),
                style={'width': '100%', 'display': 'inline-block','margin-right': 10}
            )
        ]),
        html.Div([
            html.P('2.時刻を選択してください。'),
            html.Div(
                dcc.Dropdown(
                    id='dropdown_3_2', 
                    options = times, 
                    value = times[0]['value'],
                    multi=False,
                    placeholder='時刻'
                ),
                style={'width': '100%', 'display': 'inline-block','margin-right': 10}
            )
        ]),
        html.Div(
            html.Button(id='button', n_clicks=0, children='apply',
                        style={'margin-top': '16px'},
                        className='bg-dark text-white'))
    ]),
    html.Hr()
])

# コンテンツの設定
content = html.Div([
    html.Div([
        dcc.Graph(id='output-map', style={'width': '150vh', 'height': '170vh'})
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
    Output('output-map', 'figure'),
    Input('button', 'n_clicks'),
    State('dropdown_3_1', 'value'),
    State('dropdown_3_2', 'value'))
def update_graph(n_clicks, input_date, input_time):
    # 入力値に応じたDataFrameを抽出
    df_input_dt = df.query('jst_date == @input_date and jst_time == @input_time')
    
    # 日本地図の表示
    figure = go.Figure(go.Scattermapbox(
        lat = df_input_dt['lat'],
        lon = df_input_dt['lon'],
        mode = 'markers+text',
        name = '',
        marker=go.scattermapbox.Marker(
        size=14,
        color=df_input_dt['weather_color']  
        ),
        text = df_input_dt['name'],
        customdata = df_input_dt['description'],
        hovertemplate = "%{text} <br>天気: %{customdata}", 
        hoverlabel=dict(
            bgcolor="aliceblue",
            bordercolor="midnightblue",
            font=dict(
                family="Courier New, monospace",
                size=16,
                color=df_input_dt['weather_color']
            )
        ),
        textposition='bottom right',
        textfont=dict(family="Courier New, monospace", color='white', size=12)
    ))
    
    figure.update_layout(
        hovermode='closest',
        mapbox=dict(
            center=go.layout.mapbox.Center(
                lat = 36.2488,
                lon = 138.4768
            ),
            pitch=0,
            zoom=5.5
        )
    )
    
    figure.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
    return figure
