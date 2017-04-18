#encoding=utf-8
import random as r
import math as m
import Classify as p3

#搜索的最大步长和最大范围
KSTEP,CSTEP=5,2
KMAX,CMAX=2000,1000

#冷却表参数
MarkovLength = 10000;         #马可夫链长度
DecayScale = 0.95             #衰减参数
Temperature = 100             #初始温度
PreK,NextK=0,0                #prior and next value of x 
PreC,NextC=0.0,0.0            #prior and next value of y 
BestK,BestC=0,0.0             #最终解
preScore,BestScore,Score=0.0,0.0,0.0#历史成绩，最好成绩，当前成绩
minTemp,minScore=0,100        #最低温度，最低成绩

maxValue=1000000

allNum,testNum=2000,400
clf=p3.Clf(allNum,testNum)
clf.LoadData(allNum)

def SetValue(a1,a2,a3,a4):
      minTemp=a1
      minScore=a2
      KSTEP=a3
      CSTEP=a4

def CalScore(k,c):#计算得分
      global clf
      yes,no=0,0
      yes,no=clf.test(k,c)
      score=yes*1.0/(yes+no)
      return yes,no,score

def printScore():
      print "k:",PreK,"c:",PreC,"correct:",Score

def RunAnn():
      global Temperature,PreScore,BestScore,Score
      global PreK,NextK,PreC,NextC,BestK,BestC
      #随机选点
      PreK=1#K值
      PreC=0#C值
      PreBestK = BestK = PreK
      PreBestC = BestC = PreC

      yes,no=0,0
      #温度过低或分数达到要求时停止
      while Temperature>minTemp and BestScore<minScore:

            Kstep,Cstep=maxValue,maxValue
            NextK,NextC=PreK+Kstep,PreC+Cstep
            
            #如果下一步越界了，重新定步长
            while NextK>KMAX or NextK<0 or NextC>CMAX or NextC<0:
                  Kstep=r.randint(0,KSTEP)-KSTEP/2
                  Cstep=CSTEP*(r.random()-0.5)
                  NextK,NextC=PreK+Kstep,PreC+Cstep

            yes,no,Score=CalScore(NextK,NextC)
            if Score > preScore :#比上一个解更好，接受
                  if Score>BestScore:#比最好解还好，替换
                        BestScore=Score
                        BestK=NextK
                        BestC=NextC
                  PreK=NextK
                  PreC=NextC
                  printScore()
            else:#比上一个解差
                  change=-1.0*(Score-preScore)/Temperature#降低的数值(转化为正数)
                  if m.exp(change) >r.random():#概率接受较差解
                        PreK=NextK
                        PreC=NextC
                        printScore()
                  else:#不接受
                        pass
            Temperature*=DecayScale
            print Temperature,BestScore,
      return BestK,BestC,BestScore