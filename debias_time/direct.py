def i2i(v, j, iu_data):
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
    
    tt = [[], []]
    rec_num1, click_num1, rec_num2, click_num2 = 0, 0, 0, 0
    for idx2 in range(len(iu_data[j])):
        ju = iu_data[j][idx2][0]
        
        if ju in cu:
            vt = iu_data[v][cu[ju]][1][1]
            
            for c, jt in iu_data[j][idx2][1:]:
                if jt > vt:
                    tt[0].append(jt)
                    rec_num1 += 1
                    click_num1 += c
                else:
                    tt[1].append(jt)
                    rec_num2 += 1
                    click_num2 += c
        else:
            for c, jt in iu_data[j][idx2][1:]:
                tt[1].append(jt)
                rec_num2 += 1
                click_num2 += c
    
    return rec_num1, click_num1, rec_num2, click_num2, tt

def cal_effect(v, j, iu_data):
    rec_num1, click_num1, rec_num2, click_num2, tt = i2i(v, j, iu_data)
    
    if rec_num1 > 0:
        rate1 = float(click_num1) / rec_num1
    if rec_num2 > 0:
        rate2 = float(click_num2) / rec_num2
    
    cnt = 0
    effect = 0.
    # exclude (v, j) pair with too few samples
    if rec_num1 >= 20 and rec_num2 >= 20:
        effect = rate1 - rate2
        cnt = 1
    
    return cnt, effect, tt
