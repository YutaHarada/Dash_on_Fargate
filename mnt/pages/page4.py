# import文
import requests
import os
from module.getweather import get_info

from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc


# ページレイアウトの設定
layout = html.Div(
    dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.Div(
                        [
                            dbc.Button(
                                "CLICK",
                                id="submit-button",
                                color="primary",
                                className="mb-3",
                                n_clicks=0
                                ),
                            html.Div(
                                id="container-button-basic",
                                style={"color": "blue"}
                                )
                        ],
                        style={
                            "textAlign": "center",
                            "border": "1px solid #ccc",
                            "padding": "20px",
                            "box-shadow": "0px 0px 10px dimgray",
                            "background-color": "lightblue"
                            }
                    ),
                    width=6
                ),
                className="justify-content-center align-items-center",
                style={"height": "50vh"}
            ),
        ],
        fluid=True
    )
)


@callback(
    Output('container-button-basic', 'children'),
    [Input('submit-button', 'n_clicks')]
)
def update_output(n_clicks):
    if n_clicks > 0:
        # ここでPythonスクリプトを実行
        result = get_info()
        # APIにアクセス
        url = os.getenv('API_URL')
        response = requests.post(
            url, json={'feature': result}
            )
        if response.ok:
            return f'{response.json()["prediction"]}'
        else:
            return 'APIからエラーレスポンスが返されました'
    else:
        return 'ボタンを押してください！'
