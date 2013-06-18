import os
import csv
import pickle
import math

dataPath='../track1'
linkPicklePath=os.path.join(dataPath,'links')
profilePicklePath=os.path.join(dataPath,'user_profile')
keywordPicklePath=os.path.join(dataPath,'user_keywords')

trainingFileName='target/rec_log_test_targetUser_public.txt'
trainingOutputFileName='target/test_finalist.csv'
targetUserIdFileName='target/target_users_id.txt'
itemAnditsFollowersName = 'target/itemAnditsFollowers.txt'

maximumAgeDiff = 122.0

def loadAllUserInfo():

	userInformationDict = {}
	linkFileName = "user_sns.txt"
	profileFileName = "user_profile.txt"

	linenum = 0
	with open(os.path.join(dataPath,linkFileName), 'rt') as f:

		for line in f:

			linenum += 1
			line = line.strip()
			links = line.split('\t')
			userId = int(links[0])
			des = int(links[1])

			if not userInformationDict.has_key(userId):
				userInformationDict[userId] = dict()
				userInformationDict[userId]["following"] = []
			userInformationDict[userId]["following"].append(des)

			# if linenum % 1000 == 0:
			# 	print 'loadAllUserInfo() checker in userlinkinfo', linenum

	linenum = 0
	with open(os.path.join(dataPath, profileFileName), 'rt') as f:

		for line in f:

			linenum += 1
			tokens = line.split()
			userId = int(tokens[0])
			birth = tokens[1]
			gender = tokens[2]
			num_tweets = int(tokens[3])
			tags = tokens[4]
			numoftags = len(tags.split(';'))

			if not userInformationDict.has_key(userId):
				userInformationDict[userId] = dict()
				userInformationDict[userId]["following"] = []
			userInformationDict[userId]["birth"] = birth
			userInformationDict[userId]["gender"] = gender
			userInformationDict[userId]["numtweets"] = num_tweets
			userInformationDict[userId]["numtags"] = numoftags

			# if linenum % 1000 == 0:
			# 	print 'loadAllUserInfo() checker in userprofileinfo', linenum

	return userInformationDict


def ageSimilarity(user_profile, item_profile):
	try:
		diff = abs(int(user_profile['birth']) - int(item_profile['birth']))
	except:
		diff = 122
	meanDifference = 20.39026
	sdDifference = 43.53965
	Zscore = (float(diff)- 20.39026)/sdDifference
	return Zscore

def genderSimilarity(user_profile, item_profile):

	if user_profile['gender'] == 0 or item_profile['gender'] == 0:
		similarity = 0
	elif user_profile['gender'] == item_profile['gender']:
		similarity = 1
	else:
		similarity = -1
	return similarity

def networkSimilarity(user_info, item_info):

	user_following_set = set(user_info["following"])
	item_following_set = set(item_info["following"])

	denominator = len(user_following_set | item_following_set)
	if denominator != 0:
		following_sim = len(user_following_set & item_following_set)/denominator
	else:
		following_sim = 0

	return following_sim

def convertTrainingSet(userInfoDict, trainingIdSet):
	itemInfoDic = getNumOfFollowers(itemAnditsFollowersName)
	with open(os.path.join(dataPath, trainingFileName), 'rt') as fIn:
		linenum = 0
		with open(os.path.join(dataPath, trainingOutputFileName), 'wb') as fOut:
			csvwriter = csv.writer(fOut,delimiter=',')
			csvwriter.writerow(['userid','userage','usergender','usernumtweets', 'usernumtags', 'itemid','itemage','itemgender','itemnumtweets','itemnumtags', 'agesim','gendersim','netsim','accepted','nItemFollowers'])
			for line in fIn:

				linenum += 1
				line = line.strip()
				splitted_line = line.split()

				user_id=int(splitted_line[0])
				if user_id not in trainingIdSet:
					continue
				item_id=int(splitted_line[1])
				accepted=int(splitted_line[2])
				timestamp=splitted_line[3]
				agesim = ageSimilarity(userInfoDict[user_id], userInfoDict[item_id])
				gendersim = genderSimilarity(userInfoDict[user_id], userInfoDict[item_id])
				netsim = networkSimilarity(userInfoDict[user_id], userInfoDict[item_id])

				if accepted == -1:
					accepted = 0

				try:
					userage = 2013-int(userInfoDict[user_id]['birth'])
				except:
					userage = 0
				try:
					itemage = 2013-int(userInfoDict[item_id]['birth'])
				except:
					itemage = 0
				csvwriter.writerow([user_id, userage, userInfoDict[user_id]['gender'], userInfoDict[user_id]['numtweets'], userInfoDict[user_id]['numtags'], item_id, itemage, userInfoDict[item_id]['gender'], userInfoDict[item_id]['numtweets'], userInfoDict[item_id]['numtags'], agesim, gendersim, netsim, accepted, itemInfoDic.get(item_id,0)])
				# if linenum % 1000 == 0:
				# 	print 'convertTrainingSet Checker: ', linenum

def getNumOfFollowers(filePath):
	itemInfoDic = {}
	with open(os.path.join(dataPath, filePath),'rt') as f:
		for line in f:
			arr = line.strip().split(',')
			itemId = int(arr[0])
			itemInfo = arr[1]
			arr2 = itemInfo.strip().split(' ')
			nFollowers = arr2[0]
			itemInfoDic[itemId] = int(nFollowers)
	# totalFollowers = sum(itemInfoDic.values())
	# meanFollowers = totalFollowers/(len(itemInfoDic) + 0.0)
	# totalFollowers2 = sum([x**2 for x in itemInfoDic.values()])
	# variance = totalFollowers2/(len(itemInfoDic) + 0.0) - meanFollowers**2
	# std = math.sqrt(variance)

	# for itemId in itemInfoDic.keys():
	# 	nFollowers = itemInfoDic[itemId]
	# 	itemInfoDic[itemId]= (nFollowers-meanFollowers)/std
	#print itemInfoDic
	return itemInfoDic


def loadTargetUsers():

	targetUserSet = set()
	with open(os.path.join(dataPath, targetUserIdFileName), 'rt') as f:

		for line in f:

			user_id = int(line.strip())
			targetUserSet.add(user_id)
	return targetUserSet

print('loadTargetUsers')
targetIdSet = loadTargetUsers()
print('loadAllUserInfo')
userInfoDict = loadAllUserInfo()
print('convertTrainingSet')
convertTrainingSet(userInfoDict, targetIdSet)