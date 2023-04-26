import numpy as np
import bisect
import mkl
mkl.get_max_threads()
import faiss

def i2i(v, j, iu_data, x):
    user1 = []
    click1 = []
    user2 = []
    click2 = []
    user2_ = []
    
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
            vt = iu_data[v][cu[ju]][1][1]
            
            for c, jt in iu_data[j][idx2][1:]:
                if jt > vt:
                    user1.append(ju)
                    click1.append(c)
                elif jt < vt:
                    user2.append(ju)
                    click2.append(c)
        else:
            for c, jt in iu_data[j][idx2][1:]:
                user2.append(ju)
                click2.append(c)
    
    rec_num1, click_num1 = 0, 0
    rec_num2, click_num2 = 0, 0
    
    if len(user1) != 0 and len(user2) != 0:
        xb = x[user2]
        xq = x[user1]
        
        xb = xb / np.linalg.norm(xb, axis = 1, keepdims = True)
        xq = xq / np.linalg.norm(xq, axis = 1, keepdims = True)
        
        index = faiss.IndexFlatL2(200)
        index.add(xb)
        
        D, I = index.search(xq, 1)
        
        for idx1 in range(len(I)):
            idx2 = I[idx1][0]
            
            rec_num1 += 1
            click_num1 += click1[idx1]
            rec_num2 += 1
            click_num2 += click2[idx2]
            user2_.append(user2[idx2])
    
    return rec_num1, click_num1, rec_num2, click_num2, user1, user2_

def cal_effect(v, j, iu_data, x):
    rec_num1, click_num1, rec_num2, click_num2, user1, user2 = i2i(v, j, iu_data, x)
    
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
    
    return cnt, effect, user1, user2
