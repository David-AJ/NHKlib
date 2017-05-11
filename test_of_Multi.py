#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
import numpy as np
import datetime
from scipy.spatial import distance as ds
from NHKlib2 import *
from sklearn.decomposition import PCA
import scipy.io as sio
import os
from multiprocessing import Process,cpu_count,Value,Manager,Lock
import gc
import heapq as hq

# a = pd.DataFrame.from_csv(u"C:\\Users\Jiao Yuhang\Documents\IntelliJProjects\股票数据\股票数据\股票数据.csv")
# # 只保留涨跌幅的列
# data = a[[i for i in a.columns if u"涨跌幅" in i]]
# del a
# # 生成日期*股票代码的矩阵
# matrix = np.array(data)
# np.savetxt(u"D:\\我的大学\机器学习\graphs\matrix.txt",matrix)
# 保存矩阵 np.savetxt('some_array',arr)


def createGlabels(matrix, window, Glabels, lock, count, num, start, end):
    with lock:
        for i in range(start,end):
            temp = []
            # 利用滑动窗口生成图
            if i + window <= end:
                for j in range(i, i + window):
                    temp.append(matrix[j])
                Glabels[i] = [t for t in temp]
                count.value = count.value + 1.0
            # print "com: %f"%(count.value/num.value)


if __name__ == '__main__':
    t0 = datetime.datetime.now()
    lock = Lock()
    mgr = Manager()
    count = Value('f',0.0)
    matrix = range(100000)
    num = Value('i',len(matrix))
    window = 4
    Glabels = mgr.list(range(num.value-window+1))
    label = {}
    # for i in range(len(matrix[0])):
    #     label[i] = i
    times = cpu_count()
    length = int(np.ceil((float(num.value)/times)))
    Pool = []
    for i in range(times):
        start = i*length
        end = start + length + window -1
        if end >= num.value:
            end = num.value
            process = Process(target=createGlabels,args=(matrix, window, Glabels, lock, count, num, start, end))
            Pool.append(process)
            break
        process = Process(target=createGlabels,args=(matrix, window, Glabels, lock, count, num, start, end))
        Pool.append(process)        

    for i in range(len(Pool)):
        Pool[i].start()

    for i in range(times):
        Pool[i].join()

    # for i in range(times):
    #     start = i*length
    #     end = start + length
    #     if end >= num.value:
    #         end = num.value   
    #         print Glabels[-1]
    #     else:
    #         print Glabels[end-1]
    #         print Glabels[end]

    print count.value
    print len(Glabels)
    G = list(Glabels)
    f = open('g.txt','w')
    for i in range(len(G)):
        for j in range(len(G[i])):
            f.write(str(G[i][j]) + ' ')
    f.close()
    # # multiprocessing
    # if cpu_count() <= 3:
    #     times = cpu_count()
    # else:
    #     times = cpu_count()-1

    print "Done!"
