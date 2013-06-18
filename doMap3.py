from random import shuffle

def loadSol():
	#print("load solution")
	f = open("../track1/KDD_Track1_solution_public.csv")
	lines = f.readlines()
	total = len(lines)
	soldict = dict()

	cnt = 0 
	for line in lines:
		cnt = cnt + 1
		tokens = line.split(",")
		userId = tokens[0]
## to exclude "header"
		if userId.isalpha() :
			continue
## end exclue "header"
		clicks = tokens[1]
		type = tokens[2]
		soldict[userId] = clicks.split()

	#print("load "+str(total)+" line Complete")
#		if cnt == 5:
#			break
#	print soldict
	return soldict

def loadTest():
	#print("load test")
	f = open("submisisonFile.csv")
	lines = f.readlines()
	total = len(lines)
	soldict = dict()

	cnt = 0 
	for line in lines:
		cnt = cnt + 1
		tokens = line.split(",")
		userId = tokens[0]
## to exclude "header"
		if userId.isalpha() :
			continue
## end exclue "header"
		clicks = tokens[1]
		soldict[userId] = clicks.split()

#		if cnt == 5:
#			break
	#print("load "+str(total)+" line Complete")
#	print soldict
	return soldict



def myWrite(fh,s):
	fh.write(s+"\n")
	print(s)



def MAPeval(test, sol):
	pos = 0
	limitPos = 3
	MAP = []
	for userId in test.keys():
		clicked = 0
		itemIdList = test[userId]
		#print userId, itemIdList
#		print sol[int(userId)]
		acc = []
		pos = 0
		list2 = []
		for itemId in itemIdList:
			pos = pos + 1
			if pos > limitPos:
				break
			list2 = sol[userId]
			for clickedItem in list2:
				if clickedItem == itemId :
					clicked = clicked + 1
					acc.append(clicked/float(pos))
		if len(acc) != 0 :
			averageAcc = sum(acc)/float(len(itemIdList))
		else :
			averageAcc = 0.0
		#print acc, averageAcc
		MAP.append(averageAcc)

		#if len(MAP) == 500 : 
			#break

	return MAP
				
def transformTest(resultFilePath):
	fout = open('submisisonFile.csv','w')
	userItemsDic={}
	with open(resultFilePath) as f:
		for line in f:
			arr = line.strip().split(',')
			userId = arr[0]
			itemId = arr[1]
			predict = int(arr[2])
			#actual = int(arr[3])
			h = float(arr[4])
			if predict == 1:
				if not userItemsDic.has_key(userId):
					userItemsDic[userId]=[(itemId,h)]
				else:
					userItemsDic[userId].append((itemId,h))
	for userId in userItemsDic.keys():
		items = userItemsDic[userId]
		shuffle(items)
		sorted(items, key=lambda item: item[1], reverse=True)

		itemIds = ' '.join([x[0] for x in items[:3]])
		fout.write('%s,%s\n'%(userId,itemIds)) 

	fout.close()


if __name__ == '__main__':

	resultFilePath = 'testResult.csv'
	transformTest(resultFilePath)
	
	sol = loadSol()
	test = loadTest()
	fh = open("doRandomMap3.txt",'w+')
	mapList = MAPeval(test,sol)

	#myWrite(fh,''.join(str(e)+' ' for e in mapList))
	average = sum(mapList)/float(len(mapList))
	myWrite(fh, "MAP@3 "+str(average)+" len "+str(len(mapList))+" sum "+str(sum(mapList)))


