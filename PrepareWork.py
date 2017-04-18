#coding=utf-8
def InitOriginFile(originFilePath,trainFilePath):
	originFile = open(originFilePath,"r")#初始的训练集文件
	trainFile=open(trainFilePath,"w")#清洗后的训练集文件
	line = originFile.readline()
	count=0#记录有效数据数
	while line:
		datas = line.split("\t")
		
		if datas[1]!='0' and datas[2]!='0' and datas[3]!='0':#只记录没有标签缺失的用户
			count+=1
			context='\t'.join(datas[0:4])+'\t'+'\t'.join(datas[4:]).decode('GB18030').encode('UTF-8')
			trainFile.write(context)

		line = originFile.readline()

	print "records:",count
	originFile.close()