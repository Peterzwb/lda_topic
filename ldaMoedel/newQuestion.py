# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 14:48:41 2018

@author: Administrator
"""

#也就是说如果这个新问题分出来的词在总词表里面的话就可以直接进行分类，
#如果这个新问题分出来的词有一些不在总词表里面，则就要从新进行训练。
#也就是说本身训练的数据量一定要大。

#她的思路就是使用mcmc对每个topic的密度函数进行拟合
#然后再用问题的密度函数放进去比较来判断是哪一类。

import jieba 
import getData
import textBuild
import textBuild


def pretreQues(question):
    new_question = question
    corpus, documents_tf = textBuild.unknown()
    vocabulary, documents = textBuild.clean_words(corpus, documents_tf=documents_tf)
    getdata = getData.getData()
    stop_words = getdata.read_stopword()
    vocabulary
    que_list = jieba.cut(new_question) # 可能需要事先添加一些符合业务场景的专有词,不然结巴分词无法识别
    que_list = " ".join(que_list)
    que_list = que_list.split(" ")
    List = []
    for word in que_list:
        if not(word.strip() in stop_words) and len(word.strip()) > 1:
            List.append(word.lower())
                   
    isin = []      
    for word in List:
        if word in vocabulary:
    #        print(True)
            isin.append(0)
        else:
    #        print(False)
            isin.append(1)
#    print(isin)
    if sum(isin) == 0:
        new_document = []
        for word in List:
            word_loc = vocabulary.index(word)
            new_document.append(word_loc)
        return new_document
    else:
        print("词库无法匹配")
    
if __name__ == '__main__': 
    
    new_question = "关于新区OA系统中本人发起业务单的查询方法"
    document = pretreQues(question=new_question)
        
        
    
        
