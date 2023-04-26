import pandas as pd
import pickle
import matplotlib.pyplot as plt

df1 = pd.read_csv('MINDlarge_train/news.tsv', sep = '\t', header = None, names = ['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'titleentities', 'abstractentites'])
df1 = df1.loc[:, ['news_id', 'category', 'subcategory']]
df2 = pd.read_csv('MINDlarge_dev/news.tsv', sep = '\t', header = None, names = ['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'titleentities', 'abstractentites'])
df2 = df2.loc[:, ['news_id', 'category', 'subcategory']]

with open('i2id.pkl', 'rb') as file:
    item_index = pickle.load(file)

c_num = 0
c_index = {}

i_num = max(list(item_index.values())) + 1
i2c = [-1 for i in range(i_num)]
c_cnt = {}

def mp(x):
    global c_num
    
    i = x['news_id']
    c = x['category']
    sc = x['subcategory']
    
    if i not in item_index:
        return x
    
    i_id = item_index[i]
    if c not in c_index:
        c_index[c] = c_num
        c_num += 1
    c_id = c_index[c]
    
    if c not in c_cnt:
        c_cnt[c] = 0
    c_cnt[c] += 1
    
    i2c[i_id] = c_id
    
    return x

df = pd.concat([df1, df2])
df.apply(mp, axis = 1)

with open('i2c.pkl', 'wb') as file:
    pickle.dump(i2c, file)
print('category num: {}'.format(c_num))
