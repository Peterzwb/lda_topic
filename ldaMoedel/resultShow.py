# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 10:44:06 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:43:50 2018

@author: Administrator
"""

import trainModel
import textBuild

def Result(alpha , beta):
    corpus, documents_tf = textBuild.unknown()
    vocabulary, documents = textBuild.clean_words(corpus, documents_tf=documents_tf)    
#    alpha = 0.5
#    beta = 0.1
    new_lda = trainModel.ldaModel(documents = documents, V = len(vocabulary))
    new_lda.configure(300, 100, 5)
    nw, nwSum = new_lda.gibbsSampling(30, alpha, beta) #  取30个主题
    return new_lda,nw,nwSum,corpus,documents_tf,vocabulary,documents

class showResult:
    
    
    def __init__(self, words_num):
        model,nw,nwSum,corpus,documents_tf,vocabulary,documents = Result(alpha = 0.5 , beta = 0.1)
        self.alpha = 0.5
        self.beta = 0.1
        self.model = model
        self.nw = nw
        self.nwSum = nwSum
        self.corpus = corpus
        self.documents_tf = documents_tf
        self.vocabulary = vocabulary
        self.documents = documents
        self.words_num = words_num
    
    def topicWords(self):
        topics_words_pro,topic_words = self.model.get_top_words(self.vocabulary, self.words_num)
#        return topics_words_pro,topic_words
#        print("主题词概率:")
#        print(topics_words_pro)
        print("主题词:")
        index = list(topic_words.keys())
        for id_topic in index:
            print("{topic_name} , {topic_content}".format(topic_name = id_topic , topic_content = topic_words[id_topic]))
    
    def questionCorr(self,id_num):
        model = self.model
        document_id = id_num
        print(str(list(self.documents_tf.keys())[document_id]))
        dic = {}
        for k in range(len(model.theta[document_id])):
            dic[k] = model.theta[document_id][k]
        topic_prob_list = sorted(dic.items(), key = lambda d:d[1], reverse = True)
        for topic_prob in topic_prob_list[0:1]:
            topic_id = topic_prob[0]      
            topic_words = model.phi[topic_id]
            dic = {}
            for i in range(len(topic_words)):
                dic[i] = topic_words[i]
            word_prob_list = sorted(dic.items(), key = lambda d:d[1], reverse = True)
            topic = []
            for word_prob in word_prob_list[0:20]:
                topic.append(self.vocabulary[word_prob[0]])
            print("原问题是:")
            print(self.corpus[list(self.documents_tf.keys())[document_id]])
            print("匹配到的主题是")
            print("topic" + str(topic_id))
            print(topic)
  


if __name__ == '__main__':  

    show = showResult(words_num=30)
    show.topicWords()
    show.questionCorr(id_num=11)
#    show.questionCorr(id_num=22)
    