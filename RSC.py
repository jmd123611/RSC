import heapq
from numpy import random as rd
import numpy as np
import scipy.stats as stats
import collections
import time
import random
import copy
import  math
'''def purity(cluster, label):
    cluster = np.array(cluster)
    label = np. array(label)
    indedata1 = {}
    for p in np.unique(label):
        indedata1[p] = np.argwhere(label == p)
    indedata2 = {}
    for q in np.unique(cluster):
        indedata2[q] = np.argwhere(cluster == q)

    count_all = []
    for i in indedata1.values():
        count = []
        for j in indedata2.values():
            a = np.intersect1d(i, j).shape[0]
            count.append(a)
        count_all.append(count)
    return sum(np.max(count_all, axis=0))/len(cluster)
def true_label():
    file_path1='C:/dasixia/dataset/activity.txt'
    true_labels=[]
    file=open(file_path1)
    for line in file:
        data=line.split(' ')
        true_labels.append((data[0]))
    return true_labels'''
qq=50
w=30
numP=200
minNumP=70
k=2
file_path=''
data=[]

with open(file_path) as file_object:
    for line in file_object:
        line=line.replace('\n','')
        data.append(line.split(' '))
flag=0
maxl=8
len_data=len(data)

#all_label=[]


ini_clu = [i for i in range(len_data)]


def if_or_not(str1, str2):
    flag = 1
    remain_str = copy.deepcopy(str2)
    for i in range(len(str1)):
        if str1[i] in remain_str:
            index = remain_str.index(str1[i])
            remain_str = remain_str[index + 1:]
                # print(remain_str)
        else:
            flag = 0
    return flag


time_start = time.time()
while flag == 0:
    save_pat = []
    thirty_pattern = []
    for i in range(numP):
        x = random.randint(0, len_data - 1)
        if len(data[x]) >= maxl:
            start_pos = random.randint(0, len(data[x]) - maxl)
            random_sel_pattern = data[x][start_pos:start_pos + maxl]
            thirty_pattern.append(random_sel_pattern)
    # print(thirty_pattern)
    portion = 0
    for i in range(len(thirty_pattern)):
        sum_num = 0
        for j in range(len_data):
            if if_or_not(thirty_pattern[i], data[j]):
                sum_num = sum_num + 1
        # print("当前pattern的support：",thirty_pattern[i],sum_num)
        if sum_num >= 0.2 * len_data and sum_num <= 0.8 * len_data:
            portion = portion + 1
            save_pat.append(thirty_pattern[i])
    # print("满足的pattern数量：",portion)
    if maxl == 1:
        break
    if portion >= minNumP:
        flag = 1
    else:
        maxl = maxl - 1
print("符合要求的pattern集合", len(save_pat), save_pat)
print("最终选取pattern长度：", maxl)


def div_cluster(clu_seqid):  # clu_seqid:记录数据的索引 例如[1,5,7,9]
    index_rd = random.randint(0, len(save_pat) - 1)
    # sp.append(save_pat[rd])
    # print("ten pattern",sp)

    clu1 = []
    clu2 = []
    for i in range(len(clu_seqid)):
        if if_or_not(save_pat[index_rd], data[clu_seqid[i]]) == 1:
            clu1.append(clu_seqid[i])
            # label[clu_seqid[i]]=0
        else:
            clu2.append(clu_seqid[i])
            # label[clu_seqid[i]] = 1
    # label = [0 for i in range(len_data)]
    '''for i in range(len(clu_seqid)):
        support = 0
        for j in range(len(sp)):
            if if_or_not(sp[j],data[clu_seqid[i]])==1:
                support = support + 1
        if support >= 5:
            clu1.append(clu_seqid[i])
            #label[clu_seqid[i]]=0
        else:
            clu2.append(clu_seqid[i])
            #label[clu_seqid[i]] = 1'''
    # print(clu1,clu2)
    # print(label)
    # print(purity(label,true_label()))
    # all_label.append(purity(label,true_label()))
    return clu1, clu2

adj = [[0 for i in range(len_data)] for j in range(len_data)]
    # 应该从这里循环
    # time_start = time.time()
for q in range(qq):
    print("ite:", q)
    clu1, clu2 = div_cluster(ini_clu)
    all_clu = []
    all_clu.append(clu1)
    all_clu.append(clu2)
    # depth_clu=[1,1]
    length_clu = [len(clu1), len(clu2)]
    # print("chushi:", all_clu)
    for i in range(k - 2):
        print("cluster number:", 2 + i + 1)
        # print(depth_clu)
        # print(length_clu)
        # print(all_clu)
        ind = length_clu.index(max(length_clu))
        max_clu = all_clu[ind]
        # print("最大size的cluster：",max_clu)
        new_clu1, new_clu2 = div_cluster(max_clu)
        # depth_num=depth_clu[all_clu.index(max_clu)]
        # del depth_clu[ind]
        del length_clu[ind]
        del all_clu[ind]
        # print(depth_clu)
        # print(length_clu)
        # print(all_clu)
        all_clu.append(new_clu1)
        # depth_clu.append(depth_num+1)
        length_clu.append(len(new_clu1))
        all_clu.append(new_clu2)
        # depth_clu.append(depth_num + 1)
        length_clu.append(len(new_clu2))
        # print(depth_clu)
        # print(length_clu)
        # print(all_clu)
        # clu1 = copy.deepcopy(new_clu1)
        # clu2 = copy.deepcopy(new_clu2)
        # new_clu1 = []
        # new_clu2 = []
    # print(len(all_clu))
    # rint("深度:",depth_clu)
    for i in range(len(all_clu)):
        for j in range(len(all_clu[i]) - 1):
            for z in range(j + 1, len(all_clu[i])):
                # print(all_clu[i][j],all_clu[i][z])
                # adj[all_clu[i][j]][all_clu[i][z]]=adj[all_clu[i][j]][all_clu[i][z]]+depth_clu[i]
                adj[all_clu[i][j]][all_clu[i][z]] = adj[all_clu[i][j]][all_clu[i][z]] + 1
    # print(adj)
time_end = time.time()
time_c = time_end - time_start
    # print(adj)
print('time cost', time_c, 's')
edge_num = 0
for i in range(len_data):
    for j in range(i + 1, len_data):
        # print(adj[i][j])
        if adj[i][j] >= w:
            edge_num = edge_num + 1
    print("edge_num:", edge_num)
for i in range(len_data):
    for j in range(i):
        adj[i][j] = adj[j][i]
    # print(adj)

output = []
output.append([len_data, edge_num])

    # output：metis的输入 row：每一行
for i in range(len_data):
    row = []
    for j in range(len_data):
        if adj[i][j] >= w:
            row.append(j)
            row.append(adj[i][j])

    output.append(row)

    # print(output)
with open(''%o, 'w') as f:
    for i in output:
        for j in i:
            f.write(str(j))
            f.write(' ')
        f.write('\n')
    f.close()
#print(all_label)