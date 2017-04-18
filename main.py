#encoding=utf-8
import PrepareWork as p0
import DelWord as p1
import CountInfo as p2
import Classify as p3
#p0.InitOriginFile("user_tag_query.10W.TRAIN","train.csv")
#p1.DeleteStopWord("train.csv","newTrain.csv")
#p2.CountUserRate("newTrain.csv","info.csv")

def testAnn():
	k,c,score=clf.Annealing(1,80,100,2)
	print "Best is:","k=",k,"c=",c,"correct=",score

def testClassify():
	global yes,no
	for i in range(1,2000):
		yes,no=clf.test(i*10)
		print "k:",i*10,"yes:",yes,"no:",no,"correct:",yes*1.0/(yes+no)



yes,no=0,0
allNum,testNum=2000,400
k,c,score=1,1.0,0
allNum,testNum=2000,400
clf=p3.Clf(allNum,testNum)
clf.LoadData(allNum)

testAnn()

