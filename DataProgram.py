#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
import numpy as np
import datetime
from NHKlib2 import *
from sklearn.decomposition import PCA
import scipy.io as sio
import os

# a = pd.DataFrame.from_csv(u"C:\\Users\Jiao Yuhang\Documents\IntelliJProjects\股票数据\股票数据\股票数据.csv")
# # 只保留涨跌幅的列
# data = a[[i for i in a.columns if u"涨跌幅" in i]]
# del a
# # 生成日期*股票代码的矩阵
# matrix = np.array(data)
# np.savetxt(u"D:\\我的大学\机器学习\graphs\matrix.txt",matrix)
# 保存矩阵 np.savetxt('some_array',arr)


def createGlabels(matrix, window, name):
    global t0
    # 初始化label映射
    label = {}
    for i in range(len(matrix[0])):
        label[i] = i
    # get D
    d = get_D(label)
    # get number
    num = len(matrix)
    Glabels = []
    # 生成hashed label-->Glabels
    for i in range(num):
        temp = []
        # 利用滑动窗口生成图
        if i + window <= num:
            for j in range(i, i + window):
                temp.append(matrix[j])
            # 以列向量为变量，计算各个变量间的协方差矩阵cov
            cov = np.cov(np.array(temp).T)
            
            cov[range(len(cov)), range(len(cov))] = 0
            sortcov = np.array(cov).reshape((cov.size, 1))
            sortcov.sort(0)
            # 取协方差为前10%的作为连通图
            index = sortcov[int(len(sortcov) * 0.9)]
            if index == 0:
                graph = np.where(cov > index, 1, 0).astype(int)
            else:
                graph = np.where(cov >= index, 1, 0).astype(int)
            # hash each label
            if name=="CSNHK":
            	Glabel = CSNH(graph, label, d)
            else:
            	Glabel = NH(graph, label, d)
            Glabel = Glabel.values()
            sort(Glabel, d)
            Glabels.append([g for g in Glabel])
            t1 = datetime.datetime.now()
            time = t1 - t0
            print "completed glabel: " + "%s" % str(100 * (i + 1.0) / (num))[0:5] + '%' + ' total use: %s' % time
        else:
            break
    return Glabels


def dotproduct(matrix):
    return np.dot(matrix, matrix.T)
    print "done!"


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
    matrix = sio.loadmat('matrix.mat')['matrix']
    window = input("Please enter the size of window: ")
    name = raw_input("Please enter the name of kernel file(NHK or CSNHK?): ")
    t0 = datetime.datetime.now()
    Glabels = createGlabels(matrix, window, name)
    del matrix
    length = len(Glabels)
    f = open('%slabels.txt' % name, 'w')
    for i in range(length):
        for j in range(len(Glabels[0])):
            f.write(str(Glabels[i][j]) + ' ')
    f.close()
    del Glabels
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
