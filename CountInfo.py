#coding=utf-8
from numpy import *
def CountUserRate(originFilePath,trainFilePath):

	originFile = open(originFilePath,"r")#初始的训练集文件
	trainFile=open(trainFilePath,"w")#清洗后的训练集文件

	age=[0,0,0,0,0,0]
	sex=[0,0]
	edu=[0,0,0,0,0,0]

	line = originFile.readline()
	while line:
		datas = line.split(" ")
		a=datas[1];s=datas[2];e=datas[3]
		#print a,s,e
		age[int(a)-1]+=1;sex[int(s)-1]+=1;edu[int(e)-1]+=1
		line = originFile.readline()

	trainFile.write(str(age)+"\n")
	trainFile.write(str(sex)+"\n")
	trainFile.write(str(edu)+"\n")

	print "age:",age
	print "sex:",sex
	print "edu:",edu