# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 15:46:28 2018

@author: Administrator
"""


import jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs
#import logging


class getData:
    def __init__(self):
        self.path = r"G:\项目1—人工智能客服\lda\data\data.txt"
        self.stopword = r"G:\项目1—人工智能客服\lda\data\stop_word.txt"
        
    def read_text(self):
        path = self.path
        text = codecs.open(path , "r")
        line = text.readline()
        textData = []
        while line:
            textData.append(line)
            line = text.readline()
        for i in range(0 , len(textData)):
            textData[i] = textData[i].lower() 

        textData = "".join(textData)
        return textData
    
    def read_stopword(self):
        path = self.stopword
        stopwords = codecs.open(path,'r').readlines()
        stopwords = [ w.strip() for w in stopwords ]

        return stopwords

         
if __name__ == '__main__':     
    getdata = getData()
    try_1 = getdata.read_text()    
            