# import文
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, callback

import requests

from module.getweather import get_info


layout = html.Div(
    dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.Div(
                        [
                            dbc.Button("クリックしてね",
                                       id="submit-button",
                                       color="primary",
                                       className="mb-3",
                                       n_clicks=0),
                            html.Div(id="container-button-basic")
                        ],
                        style={"textAlign": "center",
                               "border": "1px solid #ccc",
                               "padding": "20px"}
                    ),
                    width=6
                ),
                className="justify-content-center align-items-center",
                style={"height": "100vh"}
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
        # curlコマンドでAPIに送信
        response = requests.post(
            "http://localhost:5000/predict",
            json={'feature': result})
        if response.ok:
            return f'{response.json()["prediction"]}'
        else:
            return 'APIからエラーレスポンスが返されました'
    else:
        return 'ボタンを押してください!'
