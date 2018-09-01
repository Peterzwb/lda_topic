# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 10:47:15 2018

@author: Administrator
"""

import newQuestion
import getResult
al=0.5
be=0.1
new_question = "关于新区OA系统中本人发起业务单的查询方法"


#new_question = "关于新区OA系统中本人发起业务单的查询方法"
def getAnswer(new_question , al , be):
    document = newQuestion.pretreQues(question=new_question)
    model,nw,nwSum,corpus,documents_tf,vocabulary,documents = getResult.Result(alpha = al , beta = be)
    answer = model.predict(new_document= document ,nw=nw , nwSum=nwSum , alpha=0.5 ,beta= 0.1)
    new_theta = answer[0]#存着三十个标签的概率，但是这个标签值没有固定的对应
#    new_z= answer[1]
    
    dic = {}
    for k in range(len(new_theta)):
        dic[k] = new_theta[k]
    topic_prob_list = sorted(dic.items(), key = lambda d:d[1], reverse = True)
    for topic_prob in topic_prob_list[0:1]:
        topic_id = topic_prob[0]
#        print("topic" + str(topic_id))
        topic_words = model.phi[topic_id]
        dic = {}
        for i in range(len(topic_words)):
            dic[i] = topic_words[i]
        word_prob_list = sorted(dic.items(), key = lambda d:d[1], reverse = True)
        topic_content = []
        for word_prob in word_prob_list[0:20]:
            topic_content.append(vocabulary[word_prob[0]])
#            print(vocabulary[word_prob[0]])
#        print("\n")
        return topic_id,topic_content
        
if __name__ == '__main__': 
    new_question = "关于新区OA系统中本人发起业务单的查询方法"
    result = getAnswer(new_question=new_question ,al=0.5 ,be=0.1)