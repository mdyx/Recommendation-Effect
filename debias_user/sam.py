import bisect

def i2i(v, j, i_data, iu_data, x, split_cnt):
    j_data = i_data[j]
    
    cnt = 0
    times = []
    for c, t in j_data:
        if cnt % split_cnt == 0:
            times.append(t)
        cnt += 1
    
    l = len(times)
    user1 = [[] for i in range(l)]
    click1 = [[] for i in range(l)]
    user2 = [[] for i in range(l)]
    user2_ = [[] for i in range(l)]
    click2 = [[] for i in range(l)]
    
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
    
    for idx2 in range(len(iu_data[j])):
        ju = iu_data[j][idx2][0]
        
        if ju in cu:
            t = iu_data[v][cu[ju]][1][1]
            vt = bisect.bisect(times, t) - 1
            
            for c, t in iu_data[j][idx2][1:]:
                jt = bisect.bisect(times, t) - 1
                
                if jt > vt:
                    user1[jt].append(ju)
                    click1[jt].append(c)
                elif jt < vt:
                    user2[jt].append(ju)
                    click2[jt].append(c)
        else:
            for c, t in iu_data[j][idx2][1:]:
                jt = bisect.bisect(times, t) - 1
                
                user2[jt].append(ju)
                click2[jt].append(c)
    
    rec_num1, click_num1 = [0 for i in range(l)], [0 for i in range(l)]
    rec_num2, click_num2 = [0 for i in range(l)], [0 for i in range(l)]
    for t in range(l):
        # sort
        ucx = [[user2[t][idx], click2[t][idx], x[user2[t][idx]]] for idx in range(len(user2[t]))]
        ucx.sort(key = lambda x: x[2])
        tx = [x for u, c, x in ucx]
        
        # binary search
        for idx1 in range(len(user1[t])):
            u1, c1 = user1[t][idx1], click1[t][idx1]
            x1 = x[u1]
            
            match_idx = bisect.bisect_left(tx, x1)
            if match_idx == len(ucx):
                match_idx -= 1
            elif match_idx > 0:
                if abs(x1 - tx[match_idx - 1]) < abs(x1 - tx[match_idx]):
                    match_idx = match_idx - 1
            
            rec_num1[t] += 1
            click_num1[t] += c1
            if len(ucx) > 0:
                rec_num2[t] += 1
                click_num2[t] += ucx[match_idx][1]
                user2_[t].append(ucx[match_idx][0])
    
    rec_all = [len(user1[t]) + len(user2[t]) for t in range(l)]
    
    return l, rec_num1, click_num1, rec_num2, click_num2, rec_all, user1, user2_

def cal_effect(v, j, i_data, iu_data, x, split_cnt):
    l, rec_num1, click_num1, rec_num2, click_num2, rec_all, u1, u2 = i2i(v, j, i_data, iu_data, x, split_cnt)
    
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
    u1_, u2_ = [], []
    for t in range(l):
        # exclude subgroups with too few samples
        if rec_num1[t] >= 20 and rec_num2[t] >= 20:
            effect.append(rate1[t] - rate2[t])
            cnt.append(rec_all[t])
            u1_.append(u1[t])
            u2_.append(u2[t])
    res = 0.
    sum_cnt = sum(cnt)
    for i in range(len(cnt)):
        res += (float(cnt[i]) / sum_cnt) * effect[i]
    
    return len(cnt), res, u1_, u2_
