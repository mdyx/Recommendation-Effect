import pickle

print('Please be patient, this may take up to ten minutes, thank you!')

with open('data.pkl', 'rb') as file:
    data = pickle.load(file)

iu_data = {}
for u in range(len(data) - 1, -1, -1):
    for l in range(len(data[u])):
        for idx in range(len(data[u][l])):
            i, c, t = data[u][l][idx]
            
            if i not in iu_data:
                iu_data[i] = []
            temp = iu_data[i]
            if not (len(temp) > 0 and temp[-1][0] == u):
                temp.append([u])
            temp[-1].append([c, t])
    del data[u]
del data

# sort
temp = []
item_num = max(list(iu_data.keys())) + 1
for i in range(item_num):
    for idx in range(len(iu_data[i])):
        u = iu_data[i][idx][0]
        _ = iu_data[i][idx][1:]
        _.sort(key = lambda x: x[1])
        iu_data[i][idx] = [u] + _
    temp.append(iu_data[i])
    del iu_data[i]
del iu_data

with open('iu_data.pkl', 'wb') as file:
    pickle.dump(temp, file)
