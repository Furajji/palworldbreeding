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
input3 = 'リリクイン'
child1 = dict_JP_to_EN.get(input3)

# 検索する要素
target_element = child1

# 特定の要素を検索して位置をリストに格納する関数を定義します
def find_all_element_positions_df(df, target_element):
    positions = []
    for column in df.columns:
        for index, element in enumerate(df[column]):
            if element == target_element:
                positions.append((df_combi.index[index], column))
    return positions if positions else None  # ターゲットが見つからなかった場合はNoneを返す

positions = find_all_element_positions_df(df_combi, target_element)
print(positions)

# 検索対象の要素
filter_parent = 'ゴリレイジ'

def narrow_list(filter_parent, positions):
    # 特定の親が指定された場合、それを含む組み合わせのみに絞り込む
    if filter_parent is not None:
        filter_parent_EN = dict_JP_to_EN[filter_parent]
        the_other = [p2 for p1, p2 in positions if p1 == filter_parent_EN]
        if len(the_other) == 0:
            the_other = "候補が見つかりません"
        return the_other
    else:
        # タプル内の要素をソートして重複を取り除く
        unique_positions = set(tuple(sorted(pair)) for pair in positions)

        # セットをリストに変換する
        unique_positions_list = list(unique_positions)
        if len(unique_positions_list) == 0:
            unique_positions_list = "候補が見つかりません"
        return unique_positions_list

message = narrow_list(filter_parent,positions)



# 結果を表示
print(f"検索対象の要素: {target_element}")
print(f"{message}")
