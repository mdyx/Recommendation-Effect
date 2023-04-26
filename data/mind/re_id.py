import time
import pandas as pd
import pickle
import datetime

print('Please be patient, this may take up to ten minutes, thank you!')

item_num = 0
item_index = {}
user_num = 0
user_index = {}

def mp(x):
    global item_num
    global user_num
    
    u = x['user_id']
    if u not in user_index:
        user_index[u] = user_num
        user_num += 1
    u_idx = user_index[u]
    
    imp = x['impressions']
    _ = imp.split(' ')
    res = ''
    for _x in _:
        i, c = _x.split('-')
        
        if i not in item_index:
            item_index[i] = item_num
            item_num += 1
        i_idx = item_index[i]
        
        res += ' {}-{}'.format(str(i_idx), c)
    
    x['user_id'] = u_idx
    x['time'] = time.mktime(datetime.datetime.strptime(x['time'], '%m/%d/%Y %I:%M:%S %p').timetuple())
    x['impressions'] = res[1:]
    
    return x

path = 'behaviors.tsv'
df = pd.read_csv(path, sep = '\t', header = None, names = ['impression_id', 'user_id', 'time', 'history', 'impressions'])

df = df.apply(mp, axis = 1)

del df['impression_id']
del df['history']

df.to_csv('re_id.tsv', sep = '\t', index = None, header = None)
with open('i2id.pkl', 'wb') as file:
    pickle.dump(item_index, file)
print('user number: {}'.format(user_num))
print('item number: {}'.format(item_num))
