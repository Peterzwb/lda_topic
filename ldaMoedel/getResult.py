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



if __name__ == '__main__':  
    model,nw,nwSum,corpus,documents_tf,vocabulary,documents = Result(alpha = 0.5 , beta = 0.1)

