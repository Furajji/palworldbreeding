import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(__name__)

# サンプルのDataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 22],
    'Country': ['USA', 'Canada', 'UK']
})

# レイアウト
app.layout = html.Div([
    dcc.Input(id='input-column', type='text', placeholder='Enter column name'),
    dash_table.DataTable(
        id='data-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
    ),
])

# コールバック
@app.callback(
    Output('data-table', 'data'),
    [Input('input-column', 'value')]
)
def update_data_table(column_name):
    if column_name is not None and column_name in df.columns:
        # 指定された列でデータをフィルタリング
        filtered_df = df[[column_name]]
        return filtered_df.to_dict('records')
    else:
        # 入力が不正な場合は元のデータを表示
        return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
