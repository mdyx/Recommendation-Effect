import numpy as np
import pickle
import scipy.stats as stats
import random
import argparse
import sys
import direct
import matwd
import matwde
import sam
import warnings
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--data', default = 'mind', type = str)
parser.add_argument('--m_model', default = 'mat', type = str)
parser.add_argument('--s_len', default = 1000, type = int)

args = parser.parse_args()
data_dir = '../data/{}'.format(args.data)

# read
with open('{}/data.pkl'.format(data_dir), 'rb') as file:
    data = pickle.load(file)
with open('{}/iu_data.pkl'.format(data_dir), 'rb') as file:
    iu_data = pickle.load(file)
with open('{}/i2c.pkl'.format(data_dir), 'rb') as file:
    i2c = pickle.load(file)
if args.m_model == 'matwde':
    user_embedding = np.loadtxt('{}/user_embedding.txt'.format(data_dir), dtype = np.float32)
print('read finished')

# pre-processing
i_num = len(iu_data)

c_num = max(i2c) + 1
c2i = [[] for c in range(c_num)]
for i in range(len(i2c)):
    c = i2c[i]
    c2i[c].append(i)

i_click = []
i_rec = []
i_rate = []
for i in range(i_num):
    rec, click = 0, 0
    for u_data in iu_data[i]:
        for c, t in u_data[1:]:
            rec += 1
            click += c
    i_click.append(click)
    i_rec.append(rec)
    i_rate.append(float(click) / rec)

u_click = []
u_rec = []
u_rate = []
c_u_rate = [[] for cate in range(c_num)]
for u in range(len(data)):
    rec, click = 0, 0
    c_rec, c_click = [0 for cate in range(c_num)], [0 for cate in range(c_num)]
    for l in range(len(data[u])):
        for i, c, t in data[u][l]:
            rec += 1
            click += c
            c_rec[i2c[i]] += 1
            c_click[i2c[i]] += c
    
    u_click.append(click)
    u_rec.append(rec)
    u_rate.append(float(click) / rec)
    for cate in range(c_num):
        if args.m_model == 'rm':
            c_u_rate[cate].append(random.random())
        elif args.m_model == 'matwdr':
            if c_rec[cate] == 0:
                c_u_rate[cate].append(0.)
            else:
                c_u_rate[cate].append(u_rate[u])
        elif args.m_model == 'matwdvr':
            if c_rec[cate] == 0:
                c_u_rate[cate].append(0.)
            else:
                c_u_rate[cate].append(c_click[cate] / c_rec[cate])
        elif args.m_model == 'mat' or args.m_model == 'sam':
            if c_rec[cate] == 0:
                c_u_rate[cate].append(0.)
            else:
                c_u_rate[cate].append((c_click[cate] / c_rec[cate]) + u_rate[u])
del data

with open('{}/i_data.pkl'.format(data_dir), 'rb') as file:
    i_data = pickle.load(file)
print('pre-processing finished')

# experiment
x_list = []
max_test_num = 5000
test_num = 0
while test_num < max_test_num:
    v = random.randint(0, i_num - 1)
    j = random.randint(0, i_num - 1)
    if v == j:
        continue
    
    if args.m_model == 'direct':
        cnt, effect, u1, u2 = direct.cal_effect(v, j, iu_data)
    elif args.m_model == 'rm' or args.m_model == 'matwdr' or args.m_model == 'matwdvr' or args.m_model == 'mat':
        cnt, effect, u1, u2 = matwd.cal_effect(v, j, iu_data, c_u_rate[i2c[v]])
    elif args.m_model == 'matwde':
        cnt, effect, u1, u2 = matwde.cal_effect(v, j, iu_data, user_embedding)
    elif args.m_model == 'sam':
        cnt, effect, u1, u2 = sam.cal_effect(v, j, i_data, iu_data, c_u_rate[i2c[v]], args.s_len)
    else:
        print('please choose the \'m_model\' in [direct, rm, matwdr, matwdvr, matwde, mat, sam]')
        sys.exit()
    
    if cnt > 0:
        test_num += 1
        if args.m_model != 'sam':
            x_list.append([[u_rate[u] for u in u1], [u_rate[u] for u in u2]])
        # the sam stratifies the samples, there are several subgroups
        else:
            for t in range(len(u1)):
                x_list.append([[u_rate[u] for u in u1[t]], [u_rate[u] for u in u2[t]]])
        
        if test_num % 10 == 0:
            print('{}/{}'.format(test_num, max_test_num))

# result
all_cnt = 0
ls01, ls05, ls1 = 0, 0, 0
for x1, x2 in x_list:
    p = stats.ttest_ind(x1, x2, equal_var = False)[1]
    all_cnt += 1
    if p < 0.01:
        ls01 += 1
    elif p < 0.05:
        ls05 += 1
    elif p < 0.1:
        ls1 += 1
ls1 = ls01 + ls05 + ls1
ls05 = ls01 + ls05

def turn(x):
    return '{:.2f}%'.format(100. * x)

print('P<0.01: {}'.format(turn(ls01 / all_cnt)))
print('P<0.05: {}'.format(turn(ls05 / all_cnt)))
print('P<0.1: {}'.format(turn(ls1 / all_cnt)))
