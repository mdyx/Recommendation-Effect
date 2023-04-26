import bisect

def i2i(v, j, i_data, iu_data, split_cnt):
    j_data = i_data[j]
    
    cnt = 0
    times = []
    for c, t in j_data:
        if cnt % split_cnt == 0:
            times.append(t)
        cnt += 1
    
    l = len(times)
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
            t = iu_data[v][cu[ju]][1][1]
            vt = bisect.bisect(times, t) - 1
            
            for c, t in iu_data[j][idx2][1:]:
                jt = bisect.bisect(times, t) - 1
                
                if jt > vt:
                    rec_num1[jt] += 1
                    click_num1[jt] += c
                    tt[jt][0].append(t)
                elif jt < vt:
                    rec_num2[jt] += 1
                    click_num2[jt] += c
                    tt[jt][1].append(t)
        else:
            for c, t in iu_data[j][idx2][1:]:
                jt = bisect.bisect(times, t) - 1
                
                rec_num2[jt] += 1
                click_num2[jt] += c
                tt[jt][1].append(t)
    
    return l, rec_num1, click_num1, rec_num2, click_num2, tt

def cal_effect(v, j, i_data, iu_data, split_cnt):
    l, rec_num1, click_num1, rec_num2, click_num2, tt = i2i(v, j, i_data, iu_data, split_cnt)
    
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
