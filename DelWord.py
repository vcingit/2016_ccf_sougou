#encoding=utf-8
def DeleteStopWord(originFilePath,trainFilePath):
	import jieba
	import jieba.posseg
	import sys

	reload(sys)
	sys.setdefaultencoding('utf8')

	originFile = open(originFilePath,"r")#初始的训练集文件
	trainFile=open(trainFilePath,"w")#处理后的训练集文件

	line = originFile.readline()
	usefulWord=['n','v']#保存词性
	q=0#行数

	while line:
		if q%1==0:
			print 'deal with line:',q
		q+=1

		inputStr = line.split("\t")
		count=0#记录空格
		userSaveWord=[]#记录用户的有效单词
		context=' '.join(inputStr[0:4])#保存用户标签信息

		for i in inputStr[4:]:
			words=jieba.posseg.cut(i)
			for w in words:
				if w.word==' ':
					count+=1
					continue
				for u in usefulWord:
					if w.flag==u:
						userSaveWord.append(w.word.encode('UTF-8'))
						break
					else:
						continue
						
		context+=' '+str(count)+' '+' '.join(userSaveWord[:])+'\n'
		trainFile.write(context)
		line = originFile.readline()