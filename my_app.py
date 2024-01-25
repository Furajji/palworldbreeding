import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Dashアプリケーションの初期化
my_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
my_app.title = 'パルワールド　配合検索'
server = my_app.server

# CSVファイルからデータ読み込み
df_trans = pd.read_csv('csv/pal_tr.csv')
df_combi = pd.read_csv('csv/palEN_combination.csv', index_col='pal').dropna()

# 辞書の作成
dict_JP_to_EN = df_trans.set_index('nameJP')['nameEN'].to_dict()
dict_EN_to_JP = df_trans.set_index('nameEN')['nameJP'].to_dict()

# レイアウトの作成
my_app.layout = dbc.Container([
    dbc.Row([
                dbc.Col(
                    html.H1("パルワールド　配合検索",className="text-center"),
                    style={"background-color": "pink"}
                    )
            ],
            className="h-30"
        ),
    dbc.Row([
        html.H4("親からの配合検索"),
        dbc.Col([
            html.Label('親1:'),
            dcc.Dropdown(
                id='parent1-dropdown',
                options=[{'label': key, 'value': key} for key in df_trans['nameJP']],
                style={'width': '200px'}  # ドロップダウンの幅を調整
            ),
            html.Label('親2:'),
            dcc.Dropdown(
                id='parent2-dropdown',
                options=[{'label': key, 'value': key} for key in df_trans['nameJP']],
                style={'width': '200px'}  # ドロップダウンの幅を調整
            ),
        ], width=3),
        dbc.Col([
            html.Label('生まれる子:'),
            html.Div(id='child-output', style={'border': '1px solid #ccc', 'padding': '10px'}),
        ], width=7),
    ], className='mb-3', style={'background-color': '#f2f2f2', 'padding': '15px'}),

    dbc.Row([
        html.H4("子からの配合逆引き検索"),
        dbc.Col([
           dbc.Col([
            html.Label('検索対象の子:'),
            dcc.Dropdown(
                id='search-child-dropdown',
                options=[{'label': key, 'value': key} for key in df_trans['nameJP']],
                style={'width': '200px'}
            )], width=3),
            dbc.Col([
                html.Label('絞り込みの親(片方の親を指定して検索):'), 
                dcc.Dropdown(
                    id='filter-parent-dropdown',
                    options=[{'label': key, 'value': key} for key in df_trans['nameJP']],
                    style={'width': '200px'}
                ),
            html.Button('検索', id='search-button', n_clicks=0, style={'margin-top': '10px'}),
            ], width=3),
        ]),
    ], className='mb-3', style={'background-color': '#e6f7ff', 'padding': '15px'}),

    dbc.Col([
        html.Label('検索結果:'),
        html.Div(id='search-output', style={'border': '1px solid #ccc', 'padding': '10px'}),
    ]),

], fluid=True)

# コールバックの作成
@my_app.callback(
    Output('child-output', 'children'),
    [Input('parent1-dropdown', 'value'),
     Input('parent2-dropdown', 'value')],
)
def update_output(parent1, parent2):
    # 親1か親2がNoneの場合
    if parent1 is None or parent2 is None:
        return '親1と親2を選択してください'
    # 辞書を使って子の取得
    child = df_combi.at[dict_JP_to_EN[parent1], dict_JP_to_EN[parent2]]

    return f'{dict_EN_to_JP.get(child)}'

@my_app.callback(
    Output('search-output', 'children'),
    [Input('search-button', 'n_clicks'),
    State('search-child-dropdown', 'value'),
    State('filter-parent-dropdown', 'value')] 
)
def search_combinations(n_clicks, search_child, filter_parent):

    if search_child == None:
        return ''
    
    # 検索対象の要素
    target_element = dict_JP_to_EN[search_child]

    # 特定の要素を検索して位置をリストに格納する関数を定義します
    def find_all_element_positions_df(df, target_element):
        positions = []
        for column in df.columns:
            for index, element in enumerate(df[column]):
                if element == target_element:
                    positions.append((df_combi.index[index], column))
        return positions if positions else None  # ターゲットが見つからなかった場合はNoneを返す
    
    positions = find_all_element_positions_df(df_combi, target_element)

    def get_message(filter_parent, positions):
        # 特定の親が指定された場合、それを含む組み合わせのみに絞り込む
        message = ""
        if filter_parent is not None:
            filter_parent_EN = dict_JP_to_EN[filter_parent]
            the_other = [p2 for p1, p2 in positions if p1 == filter_parent_EN]
            if len(the_other) == 0:
                message = "候補が見つかりません"
            else:
                message = [f"({dict_EN_to_JP[p]})" for p in the_other]
        else:
            # タプル内の要素をソートして重複を取り除く
            unique_positions = set(tuple(sorted(pair)) for pair in positions)

            # セットをリストに変換する
            unique_positions_list = list(unique_positions)
            if len(unique_positions_list) == 0:
                message = "候補が見つかりません"
            else:
                message = [f"({dict_EN_to_JP[p1]},{dict_EN_to_JP[p2]})," for p1,p2 in unique_positions_list]
        return message

    message = get_message(filter_parent,positions)
    return message

if __name__ == '__main__':
    my_app.run_server(debug=True)
