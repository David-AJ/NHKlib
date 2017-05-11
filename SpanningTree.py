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


def createGlabels(t0, matrix, window, name, Glabels, lock, count, num, start, end ):
    # 初始化label映射
    label = {}
    for i in range(len(matrix[0])):
        label[i] = i
    # get D
    d = get_D(label)
    # 生成hashed label-->Glabels
    for i in range(start,end):
        # 利用滑动窗口生成图
        if i + window <= end:
            temp = matrix[i:i+window,:]
            # 以列向量为变量，计算各个变量间的欧氏距离矩阵dist
            dist = ds.cdist(temp.T,temp.T,'euclidean')
            # 利用dist矩阵构造最小生成树
            graph = prim(dist)
            graph = np.where(graph>0, 1, 0).astype(int)
            # hash each label
            if name=="CSNHK":
            	Glabel = CSNH(graph, label, d)
            else:
            	Glabel = NH(graph, label, d)
            Glabel = Glabel.values()
            sort(Glabel, d)
            with lock:
                Glabels[i] = [g for g in Glabel]
            t1 = datetime.datetime.now()
            time = t1 - t0
            with lock:
                count.value = count.value+1.0
            print "completed glabel: " + "%s" % str(100 * (count.value) / (num))[0:5] + '%' + ' total use: %s' % time
        else:
            break


def prim(G):
    n = G.shape[0]
    G[range(n),range(n)] = np.inf
    visited = [False for i in range(n)]
    R = np.zeros((n,n))
    nodes = range(n)
    Heap = []
    for i in range(n):
        hq.heappush(Heap,[G[0][i],0,i])
    visited[0] = True
    nodes.remove(0)
    while nodes:
        weight,node1,node2 = hq.heappop(Heap)
        if not visited[node2]:
            R[node1,node2] = R[node2,node1] = weight
            nodes.remove(node2)
            visited[node2] = True
            for i in range(n):
                if not visited[i]:
                    hq.heappush(Heap,[G[node2][i],node2,i])
    return R


def creatKernel(Glabels):
    global t0
    num = len(Glabels)
    kernel_matrix = np.eye(num)
    count = 0
    for i in range(num):
        for j in range(i + 1, num):
            count += 1
            kernel_matrix[i][j] = kernel_matrix[j][
                i] = Compare_Labels(Glabels[i], Glabels[j])
        t1 = datetime.datetime.now()
        time = t1 - t0
        print "completed: " + "%s" % str(100 * (i + 1.0) / num)[0:5] + '%' + ' total use: %s' % time
    return kernel_matrix

if __name__ == '__main__':
    # get matrix, window, name, number
    matrix = sio.loadmat('matrix.mat')['matrix']
    window = input("Please enter the size of window: ")
    name = raw_input("Please enter the name of kernel file(NHK or CSNHK?): ")
    num = len(matrix)

    # multiprocessing data
    # counter, Glabels, lock
    count = Value('f',0.0)
    mgr = Manager()
    Glabels = mgr.list(range(num-window+1))
    lock = Lock()

    #### multiprocessing start
    # if cpu_count() <= 3:
    #     times = cpu_count()
    # else:
    #     times = cpu_count()-1
    times = cpu_count()
    length = int(np.ceil((float(num)/times)))
    # get start time
    t0 = datetime.datetime.now()
    Pool = []
    for i in range(times):
        start = i*length
        end = start + length + window -1
        if end >= num:
            end = num
            process = Process(target=createGlabels,args=(t0, matrix, window, name, Glabels, lock, count, num, start, end,))
            Pool.append(process)
            break
        process = Process(target=createGlabels,args=(t0, matrix, window, name, Glabels, lock, count, num, start, end,))
        Pool.append(process)        

    for i in range(len(Pool)):
        Pool[i].start()

    for i in range(len(Pool)):
        Pool[i].join()
    #### multiprocessing end

    G = list(Glabels)
    del matrix
    del Glabels
    gc.collect()
    length = len(G)
    f = open('%slabels.txt' % name, 'w')
    for i in range(length):
        for j in range(len(G[0])):
            f.write(str(G[i][j]) + ' ')
    f.close()
    np.save('%slabels.txt' % name,np.array(G))
    del G
    gc.collect()
    os.system('compare_labels.exe %s %s' %(name+'labels.txt',name+'ernel.txt'))
    print 'kernel matrix loading...'
    kernel_matrix = np.loadtxt(name+'ernel.txt')
    pca = PCA(n_components=3)
    print 'PCA...'
    graphPCA = pca.fit_transform(kernel_matrix)
    sio.savemat(name+'ernel',{name+'ernel':kernel_matrix})
    sio.savemat(name+'PCA',{'graphPCA':graphPCA})
    # sio.savemat('/root/data/'+name+'ernel',{name+'ernel':kernel_matrix})
    # sio.savemat('/root/data/'+'graphPCA',{name+'PCA':graphPCA})
    print "Done!"
