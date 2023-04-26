import pickle

print('Please be patient, this may take up to ten minutes, thank you!')

with open('data.pkl', 'rb') as file:
    data = pickle.load(file)

click_cnt = 0
i_data = {}
user_num = len(data)
for u in range(len(data) - 1, -1, -1):
    for l in range(len(data[u])):
        for idx in range(len(data[u][l])):
            i, c, t = data[u][l][idx]
            
            if i not in i_data:
                i_data[i] = []
            click_cnt += c
            i_data[i].append([c, t])
    del data[u]

temp = []
item_num = max(list(i_data.keys())) + 1
for i in range(item_num):
    i_data[i].sort(key = lambda x: x[1])
    temp.append(i_data[i])
    del i_data[i]

with open('i_data.pkl', 'wb') as file:
    pickle.dump(temp, file)
