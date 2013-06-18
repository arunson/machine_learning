import math

def filterUserKeyWord(userKeywordPath):
	userKeywordDic={}
	i=0
	with open(userKeywordPath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			keywords = arr[1].strip().split(';')
			for keyword in keywords:
				if(i==1):
					i=0
					break
				keywordNum = keyword.strip().split(':')[0]
				if not userKeywordDic.has_key(keywordNum):
					userKeywordDic[keywordNum]=1
				else:
					userKeywordDic[keywordNum]+=1
				i+=1
	print 'number of userKeyword:',len(userKeywordDic)
	return userKeywordDic

def filterUserKeyWord2(userKeywordPath):
	userKeywordDic={}
	with open(userKeywordPath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			userId = arr[0].strip()
			keywords = arr[1].strip().split(';')
			userKeywordDic[userId]=keywords
	return userKeywordDic

def filterUserKeyWord3(userKeywordPath,itempath):
	itemDic = filterItem3(itempath)
	userKeywordDic = filterUserKeyWord2(userKeywordPath)
	print ('before:',len(userKeywordDic))
	for key in userKeywordDic.keys():
		if not itemDic.has_key(key):
			userKeywordDic.pop(key,None)
	print ('after:',len(userKeywordDic))
	return userKeywordDic



def filterItem(itempath):
	i=0
	itemDic={}
	with open(itempath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			itemId = arr[0].strip()
			itemCategory = arr[1].strip()
			itemDic[itemId]=itemCategory
			if i< 10:
				print itemId,itemCategory
				i=i+1
	print ''
	print 'total number of items:',len(itemDic)

	return itemDic

def filterItem2(itempath):
	j=0
	itemKeywordDic={}
	with open(itempath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			itemKeywords = arr[2].strip()
			keywords = itemKeywords.strip().split(';')
			for i in range(0,len(keywords)):
				if(j==2):
					j=0
					break
				keyword = keywords[i].strip()
				if not itemKeywordDic.has_key(keyword):
					itemKeywordDic[keyword]=1
				else:
					itemKeywordDic[keyword]+=1
				j+=1
	print 'number of itemKeywords:',len(itemKeywordDic)
	return itemKeywordDic

def filterItem3(itempath):
	itemKeywordDic={}
	with open(itempath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			itemId = arr[0].strip()
			itemKeywords = arr[2].strip().split(';')
			itemKeywordDic[itemId]=itemKeywords
	return itemKeywordDic

def filterUser(userPath):
	i=0
	userDic={}
	with open(userPath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			userId = arr[0].strip()
			yearOfBirth = arr[1].strip()
			gender = arr[2].strip()
			userDic[userId]=[yearOfBirth,gender]
			if i<10:
				print userId, yearOfBirth, gender
				i=i+1
	print ''
	print 'total number of users:',len(userDic)
	return userDic

def filterUser2(userpath):
	i=0
	tagIdDic={}
	with open(userpath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			tagIds = arr[4]
			arr2 = tagIds.strip().split(';')
			for num in arr2:
				if not tagIdDic.has_key(num):
					tagIdDic[num]=1
				else:
					tagIdDic[num]+=1
	print''
	print 'total number of tags:',len(tagIdDic)
	return tagIdDic

#numOfTweet
def filterUser3(userpath):
	i=0
	userDic={}
	with open(userpath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			userId = arr[0].strip()
			yearOfBirth = arr[1].strip()
			gender = arr[2].strip()
			nTweet = arr[3].strip()
			userDic[userId]=[yearOfBirth,gender,nTweet]
			if i<10:
				print userId, yearOfBirth, gender,nTweet
				i=i+1
	print ''
	print 'total number of users:',len(userDic)
	return userDic


def analyzeItems(itempath):
	itemDic = filterItem(itempath)

	values = itemDic.values()

	itemCategoryDic = {}
	for value in values:
		value = value.strip()
		if itemCategoryDic.has_key(value):
			itemCategoryDic[value]=itemCategoryDic[value]+1
		else:
			itemCategoryDic[value]=1

	itemCategoryList =  itemCategoryDic.items()
	itemCategoryList = sorted(itemCategoryList, key=lambda entry: entry[1], reverse=True)
	print 'most popluar category: ',itemCategoryList[0]

	cnt=0
	category_max=[0,0,0,0]
	category_min=[9999,9999,9999,9999]
	category_range=[0,0,0,0]

	categoryDist = {'c0':{},'c1':{},'c2':{},'c3':{}}

	for value in values:
		category = value.strip().split('.')
		#assert len(category) == 4, len(category)
		if len(category) < 4:
			continue
		for i in range(0,4):
			try:
				categoryInt = int(category[i])
			except:
				print 'cause:', category[i]
			assert categoryInt>=0
			if categoryInt>category_max[i]:
				category_max[i]=categoryInt
			if categoryInt<category_min[i]:
				category_min[i]=categoryInt
			categoryName = 'c'+str(i)
			categoryDic = categoryDist[categoryName]
			if categoryDic.has_key(categoryInt):
				categoryDic[categoryInt] = categoryDic[categoryInt] + 1
			else:
				categoryDic[categoryInt] = 1


		cnt=cnt+1
	print 'category_max: ',category_max
	print 'category_min: ',category_min
	print 'total number of items that have four category:', cnt
	print 'category distribution'
	print 'c0:',categoryDist['c0']
	print 'c1:',categoryDist['c1']
	print 'c2:',categoryDist['c2']
	print 'c3:',categoryDist['c3']

def analyzeUsers(userpath):
	userDic = filterUser(userpath)
	values = userDic.values()
	genders = [0,0,0]
	age = [0,0,0,0]
	temp = 0
	for value in values:
		try:
			yearOfBirth=int(value[0])
		except:
			temp+=1
			if temp < 100:
				print value[0],value[1]
			continue
		gender=int(value[1])
		if yearOfBirth >= 1900 and yearOfBirth < 1970:
			age[0]=age[0]+1
		elif yearOfBirth >= 1970 and yearOfBirth < 1980:
			age[1]=age[1]+1
		elif yearOfBirth >= 1980 and yearOfBirth < 1990:
			age[2]=age[2]+1
		elif yearOfBirth >= 1990 and yearOfBirth < 2005:
			age[3]=age[3]+1


		if gender == 0:
			genders[0]=genders[0]+1
		elif gender == 1:
			genders[1]=genders[1]+1
		elif gender == 2:
			genders[2]=genders[2]+1

	print 'gender: ',genders
	print 'age: ',age
	print 'temp: ',temp

def analyzeUsers2(userpath):
	userDic = filterUser2(userpath)

#user and item age distribution
def analyzeUsers3(userpath,itempath,targetUserPath):
	userDic = filterUser(userpath)
	ageDist = {}
	for userId in userDic.keys():
		try:
			userAge = int(userDic[userId][0])
		except:
			continue
		if ageDist.has_key(userAge):
			ageDist[userAge]+=1
		else:
			ageDist[userAge]=1
	print ageDist

	itemDic = filterItem3(itempath)
	itemAgeDist={}
	for itemId in itemDic.keys():
		try:
			itemAge = int(userDic[itemId][0])
		except:
			continue
		itemAgeDist[itemAge] = ageDist[itemAge]
	print 'item age dist'
	print itemAgeDist

	itemSum = 0.0
	count = 0
	for key,val in itemAgeDist.items():
		itemSum += key * val
		count += val
	itemMean = itemSum/count

	itemVSum = 0.0
	for key,val in itemAgeDist.items():
		itemVSum += key**2 * val
	itemVMean = itemVSum/count
	itemVariance = itemVMean - itemMean**2
	itemStd = math.sqrt(itemVariance)
	print 'item age mean and std:',itemMean, itemStd

	# for key,val in ageDist.items():
	# 	if val<10:
	# 		ageDist.pop(key)
	# print ageDist

	targetUserDic={}
	i=0
	with open(targetUserPath,'r') as f:
		for line in f:
			userId = line.strip()
			targetUserDic[userId]=1
			if i<10:
				print userId
				i+=1

	targetUserAgeDist = {}
	for userId in targetUserDic.keys():
		try:
			userAge = int(userDic[userId][0])
		except:
			continue
		if targetUserAgeDist.has_key(userAge):
			targetUserAgeDist[userAge]+=1
		else:
			targetUserAgeDist[userAge]=1
	print targetUserAgeDist

	userSum = 0.0
	count = 0
	for key,val in targetUserAgeDist.items():
		userSum += key * val
		count += val
	userMean = userSum/count

	userVSum = 0.0
	for key,val in targetUserAgeDist.items():
		userVSum += key**2 * val
	userVMean = userVSum/count
	userVariance = userVMean - userMean**2
	userStd = math.sqrt(userVariance)
	print 'target user age mean and std:',userMean, userStd



def saveFilteredItems(itempath):
	itemDic = filterItem(itempath)
	
	cnt=1
	categoryDic = {}
	for itemId,category in itemDic.items():
		# categoryList = category.strip().split('.')
		# categoryDicValue=''
		# if len(category) < 3:
		# 	categoryDicValue = str.format('%s.%s\n' % (itemId,category[0],category[1]))
		# else:
		# 	categoryDicValue = str.format('%s.%s.%s\n' % (itemId,category[0],category[1],category[2]))
		category = category.strip()
		if not categoryDic.has_key(category):
			categoryDic[category]=cnt
			cnt=cnt+1

	for key,value in categoryDic.items():
		categoryDic[key]=categoryDic[key]/(0.0+cnt)
	
	with open('filteredItem.txt','w') as fout:
		for itemId,category in itemDic.items():
			category = category.strip()
			fout.write('%s,%.5f\n'%(itemId,categoryDic[category]))


	# with open('filteredItem.txt','w') as fout:
	# 	for item in items:
	# 		category = item[1].strip().split('.')
	# 		if len(category) < 3:
	# 			fout.write('%s,%s.%s\n' % (item[0],category[0],category[1]))
	# 		else:
	# 			fout.write('%s,%s.%s.%s\n' % (item[0],category[0],category[1],category[2]))


def saveFilteredUsers(userpath):
	userDic = filterUser(userpath)
	users = userDic.items()
	with open('filteredUser.txt','w') as fout:
		for user in users:
			try:
				yearOfBirth=int(user[1][0])
			except:
				continue
			if yearOfBirth >= 1900 and yearOfBirth < 1970:
				user[1][0]='-1'
			elif yearOfBirth >= 1970 and yearOfBirth < 1980:
				user[1][0]='0'
			elif yearOfBirth >= 1980 and yearOfBirth < 1990:
				user[1][0]='1'
			elif yearOfBirth >= 1990 and yearOfBirth < 2005:
				user[1][0]='2'
			else:
				user[1][0]='-2'
			fout.write('%s,%s,%s\n'%(user[0],user[1][0],user[1][1]))

def analyzeUserAndItem(userpath,itempath):
	userDic = filterUser(userpath)
	itemDic = filterItem(itempath)
	itemKeys = itemDic.keys()
	cnt=0
	for itemKey in itemKeys:
		if userDic.has_key(itemKey):
			if(cnt<20):
				print userDic[itemKey]
				print itemDic[itemKey]
				print ''
			cnt+=1

	print 'cnt: ',cnt

def analyzeUserKeywordAndItemKeyword(userKeywordPath,itemPath):
	userKeywordDic = filterUserKeyWord2(userKeywordPath)
	itemDic = filterItem3(itemPath)
	i=0
	for itemId in itemDic.keys():
		if i<20:
			print itemDic[itemId]
			print userKeywordDic[itemId]
			print '%d,%d\n'%(len(itemDic[itemId]),len(userKeywordDic[itemId]))
			i+=1
		else:
			if not userKeywordDic.has_key(itemId):
				print 'error'
				break

def analyzeUserKeywordAndItemKeyword2(userKeywordPath,itemPath):
	userKeywordDic = filterUserKeyWord2(userKeywordPath)
	itemDic = filterItem3(itemPath)
	keywordDic={}
	i=0
	cnt=1
	for itemId in itemDic.keys():
		assert userKeywordDic.has_key(itemId)
		keywords = userKeywordDic[itemId]
		if i<20:
				print keywords
				i+=1
		for j in range(0,len(keywords)):
			keyword = keywords[j]
			keyword = keyword.strip().split(':')[0]
			
			if not keywordDic.has_key(keyword):
				keywordDic[keyword]=cnt
				cnt+=1
			if j >= 1:
				break

	print 'nKeywordDic:',len(keywordDic)

	with open('keywordDic.txt','w') as fout:
		fout.write('%d\n'%(len(keywordDic)))
		for keyword, num in keywordDic.items():
			fout.write('%s,%d\n'%(keyword,num))

def analyzeUserKeywordAndItemKeyword3(userKeywordPath,itemPath):
	userKeywordDic = filterUserKeyWord2(userKeywordPath)
	itemDic = filterItem3(itemPath)
	keywordDic={}
	i=0
	for itemId in itemDic.keys():
		assert userKeywordDic.has_key(itemId)
		keywords = userKeywordDic[itemId]
		if i<20:
				print keywords
				i+=1
		for j in range(0,len(keywords)):
			keyword = keywords[j]
			keyword = keyword.strip().split(':')[0]
			
			if not keywordDic.has_key(keyword):
				keywordDic[keyword]=1
			else:
				keywordDic[keyword]+=1

	print 'nKeywordDic:',len(keywordDic)	

	def keywordReduction(keywordDic,num):
		for key in keywordDic.keys():
			if keywordDic[key] <=num:
				keywordDic.pop(key,None)
		print "length after: ",len(keywordDic)

	keywordReduction(keywordDic,1)

	cnt=1
	for key in keywordDic.keys():
		keywordDic[key] = cnt
		cnt+=1

	with open('keywordDicAfterReduction1.txt','w') as fout:
		fout.write('%d\n'%(len(keywordDic)))
		for keyword, num in keywordDic.items():
			fout.write('%s,%d\n'%(keyword,num))


	return keywordDic


def countUsersInTestdata(testdataPath):
	testUserDicLeader = {}
	testUserDicFinal = {}
	flag = False
	with open(testdataPath, 'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			userId = arr[0]
			timestamp = arr[3]
			if timestamp == '1321891200':
				flag = True
			if flag == False:
				testUserDicLeader[userId] = 1
			else:
				testUserDicFinal[userId]= 1
	print len(testUserDicLeader) + len(testUserDicFinal)

def createSubmissionFile(testdataPath):
	testUserDicPublic = {}
	testUserDicFinal = {}
	with open(testdataPath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			userId = int(arr[0])
			itemId = arr[1]
			result = int(arr[2])
			timestamp = int(arr[3])
			if result == 1 and timestamp < 1321891200:
				if not testUserDicPublic.has_key(userId):
					testUserDicPublic[userId] = [itemId]
				else:
					testUserDicPublic[userId].append(itemId)
			elif result == 1:
				if not testUserDicFinal.has_key(userId):
					testUserDicFinal[userId] = [itemId]
				else:
					testUserDicFinal[userId].append(itemId)
	
	publicKeys = testUserDicPublic.keys()
	publicKeys.sort()

	finalKeys = testUserDicFinal.keys()
	finalKeys.sort()

	#write submission file with header
	with open('submisisonFile.csv','w') as fout:
		fout.write('id,clicks\n')
		for key in publicKeys:
			itemIds = ' '.join(testUserDicPublic[key])
			record = '%d,%s\n'%(key,itemIds)
			fout.write(record)
		for key in finalKeys:
			itemIds = ' '.join(testUserDicFinal[key])
			record = '%d,%s\n'%(key,itemIds)
			fout.write(record)

def itemAndTargetUsers(itempath,targetUserpath):
	targetUserDic={}
	i=0
	with open(targetUserpath,'r') as f:
		for line in f:
			userId = line.strip()
			targetUserDic[userId]=1
			if i<10:
				print userId
				i+=1
	print len(targetUserDic)


	itemDic = filterItem3(itempath)
	print len(itemDic)
	cnt = 0
	i=0
	for itemId in itemDic.keys():
		if not targetUserDic.has_key(itemId):
			cnt+=1
			if i<10:
				print itemId
				i+=1


	print '# of itemId not in targetUser: ',cnt

def testDataAndTargetUser(targetUserIdPath,testDataPath):
	targetUserDic={}
	i=0
	with open(targetUserIdPath,'r') as f:
		for line in f:
			userId = line.strip()
			targetUserDic[userId]=1
			if i<10:
				print userId
				i+=1
	print len(targetUserDic)

	cnt=0
	noTargetUserDic={}
	with open(testDataPath,'r') as f:
		for line in f:
			arr = line.strip().split('\t')
			userId = arr[0]
			if not targetUserDic.has_key(userId):
				cnt+=1
				noTargetUserDic[userId]=1
	print '# of no target users:',len(noTargetUserDic)





def extractTargetUserSimilarity(targetSimilarityPath):
	fout = open('../track1/target/train_similarity1191_reduction.txt','w')
	i=0
	with open(targetSimilarityPath,'r') as f:
		for line in f:
			arr = line.strip().split()
			sim = float(arr[2])
			fout.write('%f\n'%(sim))
	fout.close()

def analyzeUserNTweet(userpath,itempath,targetUserPath):
	userDic = filterUser3(userpath)
	nTweetDist = {}
	for userId in userDic.keys():
		try:
			nTweet = int(userDic[userId][2])
		except:
			continue
		if nTweetDist.has_key(nTweet):
			nTweetDist[nTweet]+=1
		else:
			nTweetDist[nTweet]=1
	# print ageDist

	itemDic = filterItem3(itempath)
	itemNTweetDist={}
	for itemId in itemDic.keys():
		try:
			itemNTweet = int(userDic[itemId][2])
		except:
			continue
		itemNTweetDist[itemNTweet] = nTweetDist[itemNTweet]
	print 'item age dist'
	print itemNTweetDist

	itemSum = 0.0
	count = 0
	for key,val in itemNTweetDist.items():
		itemSum += key * val
		count += val
	itemMean = itemSum/count

	itemVSum = 0.0
	for key,val in itemNTweetDist.items():
		itemVSum += key**2 * val
	itemVMean = itemVSum/count
	itemVariance = itemVMean - itemMean**2
	itemStd = math.sqrt(itemVariance)
	#item nTweet mean and std: 96.5402289794 131.803242083
	print 'item nTweet mean and std:',itemMean, itemStd

	# for key,val in ageDist.items():
	# 	if val<10:
	# 		ageDist.pop(key)
	# print ageDist

	targetUserDic={}
	i=0
	with open(targetUserPath,'r') as f:
		for line in f:
			userId = line.strip()
			targetUserDic[userId]=1
			if i<10:
				print userId
				i+=1

	targetUserAgeDist = {}
	for userId in targetUserDic.keys():
		try:
			userNTweet = int(userDic[userId][2])
		except:
			continue
		if targetUserAgeDist.has_key(userNTweet):
			targetUserAgeDist[userNTweet]+=1
		else:
			targetUserAgeDist[userNTweet]=1
	print targetUserAgeDist

	userSum = 0.0
	count = 0
	for key,val in targetUserAgeDist.items():
		userSum += key * val
		count += val
	userMean = userSum/count

	userVSum = 0.0
	for key,val in targetUserAgeDist.items():
		userVSum += key**2 * val
	userVMean = userVSum/count
	userVariance = userVMean - userMean**2
	userStd = math.sqrt(userVariance)
	#target user nTweet mean and std: 161.277149127 406.4640056
	print 'target user nTweet mean and std:',userMean, userStd

def AnalyzeUserSNSAndItem(userSNSPath,itemPath,userPath):
	itemDic = filterItem(itemPath)
	itemFollowersDic = {}
	with open(userSNSPath) as f:
		for line in f:
			arr = line.strip().split('\t')
			followerUserId = arr[0].strip()
			followee = arr[1].strip()
			if itemDic.has_key(followee):
				if not itemFollowersDic.has_key(followee):
					itemFollowersDic[followee] = [followerUserId]
				else:
					itemFollowersDic[followee].append(followerUserId)
	
	userDic = filterUser(userPath)

	for key in itemFollowersDic.keys():
		followers = itemFollowersDic[key]
		followerInfo=[]
		followerInfo.append(len(followers))
		genderList=[0,0,0]
		ageList = [0]*13 #2010/10 - 1890/10
		for follower in followers:
			userInfo = userDic[follower]
			age = userInfo[0]
			gender = userInfo[1]
			if age.isdigit():
				age = int(age)
				if age>=1890 and age<=2012:
					ageList[age/10-189]+=1
			if gender.isdigit():
				gender = int(gender)
				if gender >= 0 and gender <= 2:
					genderList[gender]+=1
		followerInfo.extend(genderList)
		followerInfo.extend(ageList)
		itemFollowersDic[key] = followerInfo

	fout = open('../track1/target/itemAnditsFollowers.txt','w')
	for key in itemFollowersDic.keys():
		users = ' '.join(str(x) for x in itemFollowersDic[key])
		fout.write('%s,%s\n'%(key,users))
	fout.close()

def AnalyzeUserSNSAndItem(userSNSPath,itemPath,userPath,targetUserPath):
	itemDic = filterItem(itemPath)
	
	targetUserDic={}
	with open(targetUserPath,'r') as f:
		for line in f:
			userId = line.strip()
			targetUserDic[userId]=1
	
	userFollowingItemCategoryDic = {}
	with open(userSNSPath) as f:
		for line in f:
			arr = line.strip().split('\t')
			followerUserId = arr[0].strip()
			followee = arr[1].strip()
			if targetUserDic.has_key(followerUserId):
				if itemDic.has_key(followee):
					category=itemDic[followee]
					if not userFollowingItemCategoryDic.has_key(followerUserId):
						userFollowingItemCategoryDic[followerUserId]={category:1}
					else:
						userCategoryDic = userFollowingItemCategoryDic[followerUserId]
						if not userCategoryDic.has_key(category):
							userCategoryDic[category]=1
						else:
							userCategoryDic[category]+=1

	with open('../track1/target/userAndhisFollowings.txt','w') as fout:
		for userId in userFollowingItemCategoryDic.keys():
			userCategoryDic = userFollowingItemCategoryDic[userId]
			userFollowingInfo = ';'.join(category+':'+str(count) for category,count in userCategoryDic.items())
			fout.write('%s,%s\n'%(userId,userFollowingInfo))

def nAcceptTestData(testdataPath):
	nAccept=0
	nReject=0
	with open(testdataPath) as f:
		for line in f:
			arr = line.strip().split('\t')
			result = int(arr[2])
			if result == 1:
				nAccept+=1
			else:
				nReject+=1
	print 'nAccept: %d,nReject: %d\n'%(nAccept,nReject)


if __name__=="__main__":
	#analyzeItems('../track1/item.txt')
	#analyzeUsers('../track1/user_profile.txt')
	#saveFilteredItems('../track1/item.txt')
	#saveFilteredUsers('../track1/user_profile.txt')
	#filterItem2('../track1/item.txt')
	#analyzeUserAndItem('../track1/user_profile.txt','../track1/item.txt')
	#analyzeUsers2('../track1/user_profile.txt')
	#filterUserKeyWord('../track1/user_key_word.txt')
	#analyzeUserKeywordAndItemKeyword('../track1/user_key_word.txt', '../track1/item.txt')
	#analyzeUserKeywordAndItemKeyword2('../track1/user_key_word.txt', '../track1/item.txt')
	#analyzeUserKeywordAndItemKeyword3('../track1/user_key_word.txt', '../track1/item.txt')
	#filterUserKeyWord3('../track1/user_key_word.txt','../track1/item.txt')
	#countUsersInTestdata('../rec_log_test.txt')
	#createSubmissionFile('../track1/testsampleForEvaluation.txt')
	#itemAndTargetUsers('../track1/item.txt','../track1/target_users_id.txt')
	#testDataAndTargetUser('../track1/target_users_id.txt','../track1/rec_log_test.txt')
	#analyzeUsers3('../track1/user_profile.txt','../track1/item.txt','../track1/target/target_users_id.txt')
	#extractTargetUserSimilarity('../track1/target/train_similarity1191.txt')
	#analyzeUserNTweet('../track1/user_profile.txt','../track1/item.txt','../track1/target/target_users_id.txt')
	#AnalyzeUserSNSAndItem('../track1/user_sns.txt','../track1/item.txt','../track1/user_profile.txt','../track1/target/target_users_id.txt')
	nAcceptTestData('../track1/target/rec_log_test_targetUser_public.txt')
