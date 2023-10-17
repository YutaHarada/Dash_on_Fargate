# import文
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from pages import page1, page2, page3

# Dashのappの初期化
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.MORPH])

# ページ上部に表示するナビゲーションバーを作成
navbar = html.Div([
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("5days info", href="/page1")),
                    dbc.NavItem(dbc.NavLink("Temp trends", href="/page2")),
                    dbc.NavItem(dbc.NavLink("Wheather map", href="/page3"))
                ],
                color = 'midnightblue',
                brand="Wheather Forecast",
                id = 'navibar'
            ),
            html.Div([
                html.P('参照情報:'),
                html.A('OpenWeather ', href='https://openweathermap.org/', target='_blank')
            ], style = {'margin-left': '40px'})
        ])

# グラフの描画範囲などの指定
content = html.Div([
                    html.Div(id="page-content", 
                             style={"padding": "1rem 1.5rem","width":"100%","height":"100%"})
                ])

# 全体のレイアウト指定
app.layout = html.Div([
                        dcc.Location(id='url', refresh=False),
                        navbar,
                        content
                    ])
# コールバック関数。ナビゲーションバーでクリックされたページに応じたグラフを表示する。
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if (pathname == '/page1')|(pathname == '/'): 
        return_content = page1.layout
    elif (pathname == '/page2'):
        return_content = page2.layout
    elif (pathname == '/page3'):
        return_content = page3.layout
    else:
        return_content = '404 not found'

    return [return_content]


# アプリケーションの起動
# セキュリティグループなどでアクセス制限を実施する必要あり。
if __name__ == '__main__':
    app.run_server(
        port=8050,
        host='0.0.0.0'
    )
