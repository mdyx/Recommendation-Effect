import numpy as np
import pandas as pd
import pickle

print('Please be patient, this may take up to ten minutes, thank you!')

path = 're_id.tsv'
df = pd.read_csv(path, sep = '\t', header = None, names = ['user_id', 'timestamp', 'impressions'], dtype = {'user_id': np.int32, 'timestamp': np.float64, 'impressions': str})

df = df.sort_values(by = 'timestamp')
g = df.groupby(by = ['user_id'])

data = {}

def mp(x):
    u = x['user_id']
    t = x['timestamp']
    imp = x['impressions']
    
    if u not in data:
        data[u] = []
    
    data[u].append([])
    imp = x['impressions']
    _ = imp.split(' ')
    for _x in _:
        i, c = _x.split('-')
        i = int(i)
        c = int(c)
        
        data[u][-1].append([i, c, t])
    
    return x

li = list(g)
for x in li:
    u_df = x[1]
    u_df = u_df.sort_values(by = 'timestamp')
    u_df.apply(mp, axis = 1)

user_num = max(list(data.keys())) + 1
temp = []
for u in range(user_num):
    temp.append(data[u])

with open('data.pkl', 'wb') as file:
    pickle.dump(temp, file)
