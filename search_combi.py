import pandas as pd

input1 = 'モコロン'
input2 = 'ペンタマ'

df_trans = pd.read_csv('csv/pal_tr.csv')
print(df_trans.head())

dict_JP_to_EN = df_trans.set_index('nameJP')['nameEN'].to_dict()
dict_EN_to_JP = df_trans.set_index('nameEN')['nameJP'].to_dict()
print(dict_EN_to_JP.get(input2))

# 英語名取得
parent1 = dict_JP_to_EN.get(input1)
parent2 = dict_JP_to_EN.get(input2)

# 検索
df_combi = pd.read_csv('csv/palEN_combination.csv',index_col='pal').dropna()
child = df_combi.at[parent1,parent2]

print('親',dict_EN_to_JP.get(parent1),dict_EN_to_JP.get(parent2),'子',dict_EN_to_JP.get(child))

# 逆検索
input3 = 'カバネドリ'
child1 = dict_JP_to_EN.get(input3)

# 検索する要素
target_element = child1

# DataFrameから要素を検索して、行と列を表示
result_indices = df_combi.index[df_combi.eq(target_element).any(axis=1)].tolist()
result_columns = df_combi.columns[df_combi.eq(target_element).any()].tolist()

# 検索対象の要素
filter_parent = 'アズレーン'

# DataFrameから要素を検索して、行と列の組み合わせをリストで取得
result_indices = df_combi.index[df_combi.eq(target_element).any(axis=1)].tolist()

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
# 結果を表示
print(f"検索対象の要素: {target_element}")
print(f"該当する行と列の組み合わせ: {result_combinations}")

df = pd.DataFrame(result_combinations_JP).to_dict('records')
list = [row[1] for row in df]
print(list)