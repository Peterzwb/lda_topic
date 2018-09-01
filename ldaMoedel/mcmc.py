# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 12:23:58 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 12:26:21 2018

@author: Administrator
"""

#coding=utf-8
from __future__ import division
import random
import copy
import trainModel
import textBuild

corpus, documents_tf = textBuild.unknown()
vocabulary, documents = textBuild.clean_words(corpus, documents_tf=documents_tf) 
#
#corpus, documents_tf = textBuild.unknown()
#vocabulary, documents = textBuild.clean_words(corpus, documents_tf=documents_tf)


class ldaModel:
    def __init__(self, documents = None, V = 0):
        self.documents = documents
        self.V = V # 词的总数
        self.K = 0 # 主题总数
        self.iterations = 10000 # Gibbs抽样迭代次数
        self.burnIn = 2000
        self.interval = 100 # Gibbs抽样的预烧期
        self.theta = None # 文档-主题分布律矩阵
        self.phi = None # 主题-词分布律矩阵
        self.Z = [] # 文档中词的主题
 
    # 配置参数
    def configure(self, iterations, burnIn, interval):
        self.iterations = iterations
        self.burnIn = burnIn
        self.interval = interval
        
    # Gibbs抽样
    def gibbsSampling(self, K, alpha, beta):
        V = len(vocabulary)#词个数
        K = 30#主题个数
        M = len(documents)#文档的数目
        numStats = 0
        nw = [[0 for col in range(V)] for row in range(K)]#K行V列
        #推测nw应该是每个主题的分布
        nwSum = [0 for row in range(K)]#K行
        #推测nwSum应该是每个主题的id
        nd = [[0 for col in range(K)] for row in range(M)]#M行K列
        #推测nd应该是每个文档属于各个主题的概率
        ndSum = [0 for row in range(M)]#M行
        #推测是各个文档的id
        thetaSum = [[0 for col in range(K)] for row in range(M)]#M行K列
        #具体未知
        phiSum = [[0 for col in range(V)] for row in range(K)]#K行V列
        #具体未知
        initialState(nw, nwSum, nd, ndSum)
        
        iterations = 10000
        for i in range(iterations):
            for m in range(M):
                for n in range(len(documents[m])):
                    k = Z[m][n]
                    t = documents[m][n]
                    nw[k][t] = nw[k][t] - 1
                    nwSum[k] = nwSum[k] -1
                    nd[m][k] = nd[m][k] - 1
                    ndSum[m] = ndSum[m] -1
                    k1 = reSampling(m, t, alpha, beta, nw, nwSum, nd, ndSum)
                    self.Z[m][n] = k1
                    nw[k1][t] = nw[k1][t] + 1
                    nwSum[k1] = nwSum[k1] + 1
                    nd[m][k1] = nd[m][k1] + 1
                    ndSum[m] = ndSum[m] + 1
            if ((i > self.burnIn) and ((i - self.burnIn) % self.interval == 0)):
                for m in range(len(self.documents)):
                    for k in range(self.K):
                        # thetaSum[m][k] += (nd[m][k] + alpha) / (ndSum[m] + alpha * self.K)
                        thetaSum[m][k] = (nd[m][k] + alpha) / (ndSum[m] + alpha * self.K)
                for k in range(self.K):
                    for t in range(self.V):
                        # phiSum[k][t] += (nw[k][t] + beta) / (nwSum[k] + beta * self.V)
                        phiSum[k][t] = (nw[k][t] + beta) / (nwSum[k] + beta * self.V)
                # numStats = numStats + 1
        numStats = numStats + 1
        self.updatePara(thetaSum, phiSum, numStats)
        return nw, nwSum # 返回值,在预测新文档的主题分布时需要用到这两个量
        
    def initialState(nw, nwSum, nd, ndSum):
        M = len(documents)
        theta = [[0 for col in range(K)] for row in range(M)]#M行K列
        #具体未知
        phi = [[0 for col in range(V)] for row in range(K)]#K行V列
        #具体未知
        Z = []
        for m in range(M):
            N = len(documents[m])#返回每个文档的长度
            Z.append([])
            for n in range(N):
                k = random.choice(range(K)) # 随机生成第m篇文档中第n个词的主题编号
                #随机的问题出在这里
                #随机生成K个主题中随便取一个
                Z[m].append(k)#存的是每次抽取的主题id
                t = documents[m][n]#取出该篇文档的第n个词
                nw[k][t] = nw[k][t] + 1#在第k个主题中的这个词位置上加一
                nwSum[k] = nwSum[k] + 1#具体未知
                nd[m][k] = nd[m][k] + 1#在第m个文档的这个词的位置上加一
                ndSum[m] = ndSum[m] + 1#具体未知
                
    def reSampling(m, t, alpha, beta, nw, nwSum, nd, ndSum):
        p = [0 for i in range(self.K)]
        for k in range(self.K):
            p[k] = (nw[k][t] + beta) * (nd[m][k] + alpha) / ((nwSum[k] + beta*self.V) * (ndSum[m] + alpha*self.K))
        for i in range(1, self.K):
            p[i] = p[i] + p[i-1]
        u = random.random() * p[self.K - 1]
        k1 = 0
        for i in range(self.K):
            if (u <= p[i]):
                k1 = i
                break
        return k1
    
    def updatePara(self, thetaSum, phiSum, numStats):
        for m in range(len(self.documents)):
            for k in range(self.K):
                self.theta[m][k] = thetaSum[m][k] / numStats
        for k in range(self.K):
            for t in range(self.V):
                self.phi[k][t] = phiSum[k][t] / numStats
 
    def get_top_words(self, vocabulary, N):
        topics_dic = {}
        words = {}
        k = -1
        print(type(self.phi))#这个phi是一个嵌套列表
        for topic_words in self.phi:
            
            k += 1
            dic = {}
            for i in range(len(topic_words)):
                dic[i] = topic_words[i]
            word_prob_list = sorted(dic.items(), key = lambda d:d[1], reverse = True)
            topics_dic["topic" + str(k)] = word_prob_list
#            print("topic"+str(k))
            word = []
            for word_prob in word_prob_list[0:N]:
                word.append(vocabulary[word_prob[0]])
#                print(vocabulary[word_prob[0]])               
#            print("\n")
            words["topic_words"+str(k)] = word
        return topics_dic,words
 
    def get_top_topics(self, corpus):
        docs_dic = {}
        m = -1
        for doc_topics in self.theta:
            m += 1
            dic = {}
            for k in range(len(doc_topics)):
                dic[k] = doc_topics[k]
            topic_prob_list = sorted(dic.items(), key = lambda d:d[1], reverse = True)
            docs_dic[(corpus.keys())[m]] = topic_prob_list
            for topic_prob in topic_prob_list[0:10]:
                print("topic" + topic_prob[0])
            print("\n")
        return docs_dic
 
    def predict(self, new_document, nw, nwSum, alpha, beta):
        # 预测新文档的主题分布
        # new_document是由词在总词表中的编号构成的列表,按出现顺序排列
        new_theta = [0 for col in range(self.K)]
        # new_phi = [0 for col in range(self.V)]
        new_nd = [0 for col in range(self.K)]
        new_ndSum = 0
        new_nw = copy.deepcopy(nw)
        new_nwSum = copy.deepcopy(nwSum)
        N = len(new_document)
        new_z = []
        for n in range(N):#遍历新文档中的词
            k = random.choice(range(self.K))
            new_z.append(k)
            t = new_document[n]
            new_nw[k][t] = new_nw[k][t] + 1
            new_nwSum[k] = new_nwSum[k] + 1
            new_nd[k] = new_nd[k] + 1
            new_ndSum = new_ndSum + 1
        for i in range(self.iterations):
            for n in range(N):
                k = new_z[n]
                t = new_document[n]
                new_nw[k][t] = new_nw[k][t] - 1
                new_nwSum[k] = new_nwSum[k] - 1
                new_nd[k] = new_nd[k] - 1
                new_ndSum = new_ndSum - 1
                p = [0 for i in range(self.K)]
                for j in range(self.K):
                    p[j] = (new_nw[j][t] + beta) * (new_nd[j] + alpha) / ((new_nwSum[j] + beta*self.V) * (new_ndSum + alpha*self.K))
                for j in range(1, self.K):
                    p[j] = p[j] + p[j-1]
                u = random.random() * p[self.K - 1]
                k1 = 0
                for j in range(self.K):
                    if (u <= p[j]):
                        k1 = j
                        break
                new_z[n] = k1
                new_nw[k1][t] = new_nw[k1][t] + 1
                new_nwSum[k1] = new_nwSum[k1] + 1
                new_nd[k1] = new_nd[k1] + 1
                new_ndSum = new_ndSum + 1
        for k in range(self.K):
            new_theta[k] += (new_nd[k] + alpha) / (new_ndSum + alpha * self.K)
        # for t in range(self.V):
        #     new_phi[t] += (new_nw[k][t] + beta) / (new_nwSum[k] + beta * self.V)
        return new_theta, new_z

        
if __name__ == '__main__':  
    alpha = 0.5
    beta = 0.1
    
    corpus, documents_tf = textBuild.unknown()
    vocabulary, documents = textBuild.clean_words(corpus, documents_tf=documents_tf)
    

    new_lda = ldaModel(documents = documents, V = len(vocabulary))
    new_lda.configure(300, 100, 5)
    nw, nwSum = new_lda.gibbsSampling(30, alpha, beta) #  取30个主题
    
#    a,b = new_lda.get_top_words(vocabulary,20)