import random

def i2i(v, j, iu_data, split_cnt):
    j_data = []
    for u_data in iu_data[j]:
        j_data += u_data[1:]
    # in order to random stratify, we first random sort the samples
    j_data.sort(key = lambda x: random.random())
    
    cnt = -1
    times = []
    sample2s = {}
    for c, t in j_data:
        cnt += 1
        sample2s[(c, t)] = cnt // split_cnt
    
    l = (cnt // split_cnt) + 1
    rec_num1 = [0 for i in range(l)]
    click_num1 = [0 for i in range(l)]
    rec_num2 = [0 for i in range(l)]
    click_num2 = [0 for i in range(l)]
    
    idx1 = 0
    idx2 = 0
    cu = {}
    # users have been sorted in descending order
    while idx1 < len(iu_data[v]) and idx2 < len(iu_data[j]):
        vu = iu_data[v][idx1][0]
        ju = iu_data[j][idx2][0]
        if vu > ju:
            idx1 += 1
            continue
        if vu < ju:
            idx2 += 1
            continue
        cu[ju] = idx1
        idx1 += 1
        idx2 += 1
    
    tt = [[[], []] for i in range(l)]
    for idx2 in range(len(iu_data[j])):
        ju = iu_data[j][idx2][0]
        
        if ju in cu:
            vt = iu_data[v][cu[ju]][1][1]
            
            for c, jt in iu_data[j][idx2][1:]:
                idx = sample2s[(c, jt)]
                if jt > vt:
                    rec_num1[idx] += 1
                    click_num1[idx] += c
                    tt[idx][0].append(jt)
                else:
                    rec_num2[idx] += 1
                    click_num2[idx] += c
                    tt[idx][1].append(jt)
        else:
            for c, jt in iu_data[j][idx2][1:]:
                idx = sample2s[(c, jt)]
                
                rec_num2[idx] += 1
                click_num2[idx] += c
                tt[idx][1].append(jt)
    
    return l, rec_num1, click_num1, rec_num2, click_num2, tt

def cal_effect(v, j, iu_data, split_cnt):
    l, rec_num1, click_num1, rec_num2, click_num2, tt = i2i(v, j, iu_data, split_cnt)
    
    rate1 = [0. for _ in range(l)]
    for t in range(l):
        if rec_num1[t] > 0:
            rate1[t] = float(click_num1[t]) / rec_num1[t]
    rate2 = [0. for _ in range(l)]
    for t in range(l):
        if rec_num2[t] > 0:
            rate2[t] = float(click_num2[t]) / rec_num2[t]
    
    effect = []
    cnt = []
    tt_ = []
    for t in range(l):
        # exclude subgroups with too few samples
        if rec_num1[t] >= 20 and rec_num2[t] >= 20:
            effect.append(rate1[t] - rate2[t])
            cnt.append(rec_num1[t] + rec_num2[t])
            tt_.append(tt[t])
    res = 0.
    sum_cnt = sum(cnt)
    for i in range(len(cnt)):
        res += (float(cnt[i]) / sum_cnt) * effect[i]
    
    return len(cnt), res, tt_
