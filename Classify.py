# coding:utf-8
import sys
from numpy import *
import os
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn import svm
import matplotlib.pyplot as plt   #导入pyplot子库
import random as r
import math as m

reload(sys)
sys.setdefaultencoding('utf8')

class Clf(object):
	#全局变量 训练集，标签集，每个训练样本的词频矩阵，词袋
	corpus,target,wordList,wordCount=[],[],[],None
	#总样本数，测试样本数
	allNum,testNum=1000,200

	def __init__(self, allNum, testNum):
		self.allNum = allNum
		self.testNum = testNum

	def LoadData(self,allNum=1000):#返回训练集，标签，词频矩阵，词袋

		originFile = open("newtrain.csv","r")#初始的训练集文件

		line = originFile.readline()
		q=0

		while line and q<allNum:
			tmpDatas=line.split(' ')
			datas=' '.join(tmpDatas[5:])
			self.corpus.append(datas)
			self.target.append(tmpDatas[2])

			q+=1
			line = originFile.readline()

		vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
		self.wordCount=vectorizer.fit_transform(self.corpus)#将文本转为词频矩阵
		self.wordList=vectorizer.get_feature_names()#获取词袋模型中的所有词语

		originFile.close()


	def chi(self,k=200):#返回被选的k个特征构成的用户矩阵

		res=SelectKBest(chi2, k).fit_transform(self.wordCount.toarray(), self.target)
		return res


	def test(self,k=1,c=1):#得到预测正确数与错误数

		res=self.chi(k)#特征降维后的词频矩阵

		X=res[:-self.testNum]#测试集

		y=self.target[:-self.testNum]#测试集的结果标签
		clf = svm.SVC(c)
		clf.fit(X, y)
		result = clf.predict(res[-self.testNum:])#预测
		
		yes=0
		no=0
		for i in range(len(result)):
			if self.target[i+self.allNum-self.testNum] == result[i]:
				yes+=1
			else:
				no+=1
		
		return yes,no

	def CalScore(self,k,c):
		yes,no=0,0
		yes,no=self.test(k,c)
		score=yes*1.0/(yes+no)
		return yes,no,score

	def Annealing(self,minTemp=0,minScore=100,KSTEP=5,CSTEP=2):
		#搜索的最大范围
		KMAX,CMAX=2000,1000

		#冷却表参数
		MarkovLength = 10000;         #马可夫链长度
		DecayScale = 0.98             #衰减参数
		Temperature = 100             #初始温度
		PreK,NextK=0,0                #prior and next value of x 
		PreC,NextC=0.0,0.0            #prior and next value of y 
		BestK,BestC=0,0.0             #最终解
		PreScore,BestScore,Score=0.0,0.0,0.0#历史成绩，最好成绩，当前成绩
		maxValue=1000000

		#随机选点
		PreK=1#K值
		PreC=0#C值
		PreBestK = BestK = PreK
		PreBestC = BestC = PreC

		yes,no=0,0
		i=0
		#温度过低或分数达到要求时停止
		while Temperature>minTemp and BestScore<minScore:

			Kstep,Cstep=maxValue,maxValue
			NextK,NextC=PreK+Kstep,PreC+Cstep

			#如果下一步越界了，重新定步长
			while NextK>KMAX or NextK<=0 or NextC>CMAX or NextC<0:
				Kstep=r.randint(0,KSTEP)-KSTEP/2
				Cstep=CSTEP*(r.random()-0.5)
				NextK,NextC=PreK+Kstep,PreC+Cstep

			yes,no,Score=self.CalScore(NextK,NextC)
			print "i:",i,"k:",NextK,"c:",NextC,"correct:",Score,"pre:",PreScore,"T:",Temperature,
			if Score > PreScore :#比上一个解更好，接受
				if Score>BestScore:#比最好解还好，替换
					BestScore=Score
					BestK=NextK
					BestC=NextC
				PreK=NextK
				PreC=NextC
				PreScore=Score
				print "accept1"
			else:#比上一个解差
				change=1000.0*(Score-PreScore)/Temperature#降低的数值(转化为正数)
				#print change,m.exp(change),
				if m.exp(change) >r.random():#概率接受较差解
					PreK=NextK
					PreC=NextC
					PreScore=Score
					print "accept2"
				else:#不接受
					print "refuse"
					pass
			Temperature*=DecayScale
			i+=1

		return BestK,BestC,BestScore
