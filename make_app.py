import pandas as pd
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# CSVファイルからデータ読み込み
df_trans = pd.read_csv('csv/pal_tr.csv')
df_combi = pd.read_csv('csv/palEN_combination.csv', index_col='pal').dropna()

# 辞書の作成
dict_JP_to_EN = df_trans.set_index('nameJP')['nameEN'].to_dict()
dict_EN_to_JP = df_trans.set_index('nameEN')['nameJP'].to_dict()

# Dashアプリケーションの初期化
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# レイアウトの作成
app.layout = dbc.Container([
    dbc.Row(
            [
                dbc.Col(
                    html.H1("パルワールド　配合検索",className="text-center"),
                    style={"background-color": "pink"}
                    )
            ],
            className="h-30"
        ),
    dbc.Row([
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
        dbc.Col([
           dbc.Col([
            html.Label('検索対象の子:'),
            dcc.Dropdown(
                id='search-child-dropdown',
                options=[{'label': key, 'value': key} for key in df_trans['nameJP']],
                style={'width': '200px'}
            )], width=3),
            dbc.Col([
                html.Label('絞り込みの親:'),  # 新しいドロップダウン
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
@app.callback(
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

@app.callback(
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

    # DataFrameから要素を検索して、行と列の組み合わせをリストで取得
    result_indices = df_combi.index[df_combi.eq(target_element).any(axis=1)].tolist()
    result_columns = df_combi
    
    # 特定の親が指定された場合、それを含む組み合わせのみに絞り込む
    if filter_parent is not None:
        filter_parent_element = dict_JP_to_EN[filter_parent]
        result_indices = [row for row in result_indices if row == filter_parent_element]

    result_columns = df_combi
    # 組み合わせのリストを作成
    # 指定したtarget_elementを含む組み合わせを除外
    result_combinations = list(
        set((row, col) for row in result_indices for col in result_columns)
        - {(target_element, col) for col in result_columns}  # target_element を左に含む組み合わせを除外
        - {(row, target_element) for row in result_indices}  # target_element を右に含む組み合わせを除外
        - {(target_element, target_element)}  # target_element を両方にもつ組み合わせを除外
    )
    result_combinations_JP = [(dict_EN_to_JP[i],dict_EN_to_JP[j]) for i,j in result_combinations]
    
    # Concatenate the two messages into a single string
    message = f"{result_combinations_JP}"

    if filter_parent is not None:
        result_dict = pd.DataFrame(result_combinations_JP).to_dict('records')
        pallist = [row[1] for row in result_dict]
        message = f"{pallist}"
    
    return message

if __name__ == '__main__':
    app.run_server(debug=True)
