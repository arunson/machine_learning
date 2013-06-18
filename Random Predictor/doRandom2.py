def rs(itemIds):
	import random
	limit = 3
	list = []
	#print itemIds
	if len(itemIds) <= 3 :
		return itemIds
	else :
		for i in range(limit):
			list.append(itemIds[int(random.random()*len(itemIds))])	

	#print list	
	return list


def createSubmissionFile(testdataPath):
	testUserDicFinal = {}
	pos = 0 
	#read test result file
	with open(testdataPath,'r') as f:
		for line in f:
			pos = pos + 1
			arr = line.strip().split('\t')
			userId = int(arr[0])
			itemId = arr[1]
			result = int(arr[2])
			timestamp = int(arr[3])
			if not testUserDicFinal.has_key(userId):
				testUserDicFinal[userId] = [itemId]
			else:
				testUserDicFinal[userId].append(itemId)
			#if pos == 50 :
				#break

	#sort by userId
	finalKeys = testUserDicFinal.keys()
	finalKeys.sort()
	#print testUserDicFinal

	#write submission file with header
	with open('submisisonFile.csv','w+') as fout:
		fout.write('id,clicks\n')
		for key in finalKeys:
			itemIds = rs(testUserDicFinal[key])
			itemIds = ' '.join(itemIds)
			record = '%d,%s\n'%(key,itemIds)
			fout.write(record)

if __name__=="__main__":
	createSubmissionFile("rec_log_test_targetUser.txt")
