# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:43:50 2018

@author: Administrator
"""
from __future__ import division
from getData import getData
import jieba 


def originData():
    getdata = getData()
    data = getdata.read_text()
    stop_words = getdata.read_stopword()
    doc_content = data
    dict_data = doc_content.split("\n")
    dict_data.remove("")
    return dict_data,stop_words

          
def extract_structed_data(corpus, documents_tf, doc_name, doc_content, stop_words):
    
    # corpus是个字典,key是文档名,value是该文档中所有词(允许重复)构成的列表
    # documents_tf是个字典,key是文档名,value是以词为key,以tf值为key的字典
    # doc_name是文档名
    # doc_content是文档的内容(可能需要作编码转换,以及删除一些非文字符号)
    words_list = jieba.cut(doc_content) # 可能需要事先添加一些符合业务场景的专有词,不然结巴分词无法识别
    corpus[doc_name] = []
    documents_tf[doc_name] = {}
    for word in words_list:
        if not(word.strip() in stop_words) and len(word.strip()) > 1:
            corpus[doc_name].append(word)
            documents_tf[doc_name].setdefault(word, 0)
            documents_tf[doc_name][word] += 1

          
def unknown():  
    dict_data,stop_words = originData()
    corpus = {}
    documents_tf = {}
    
    # 提取article_crawler_result_1.txt中存储的前20篇文档,大数据相关文章
    for i in range(0 , len(dict_data)):
        name = "问题"
        doc_name = name + str(i)
        doc_content = dict_data[i]
        extract_structed_data(corpus, documents_tf, doc_name, doc_content, stop_words)
    return corpus, documents_tf

## 将每篇文章中出现次数低于5的词全部剔除
def clean_words(corpus, documents_tf):
    # documents是LDA模型的输入参数之一
    # vocabulary是清理文档中的低频词之后得到的词语列表
    # m是文档在corpus.keys()中的索引
    # documents[m][n]的值是第m个文档中第n个词在vocabulary中的索引
    # tf_min是词在文档中出现次数的临界值
    # 在文档中出现次数太少的词对于阐述文档的主题没有意义,将这些词剔除
    key_1 = list(documents_tf.keys())
    key_1.sort()
    vocabulary = []
#    print(key_1)
    for doc_name in key_1:
        key_2 = list(documents_tf[doc_name].keys())
        key_2.sort()
        for word in key_2:
            if not (word in vocabulary):
                vocabulary.append(word)#去重
    # 构建documents矩阵
    documents = []
    m = -1
#    print(key)
    for doc_name in key_1:
        documents.append([])
        m += 1
        for word in corpus[doc_name]:
            if word in vocabulary:
                documents[m].append(vocabulary.index(word))
    return vocabulary, documents


if __name__ == '__main__':  
    corpus, documents_tf = unknown()
    vocabulary, documents = clean_words(corpus, documents_tf=documents_tf)
    
#    a = list(documents_tf.keys())