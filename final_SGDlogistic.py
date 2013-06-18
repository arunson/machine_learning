import numpy as np
import csv
import os
import math
# import pdb

#***************************** CAUSATION *******************************#
# This file require the pre excution of changeTraningset_jh.py         #
# That file train_finalist_jh.csv, which is used for this code as #
# data(for training model).                                             #
# Please run changeTraningset_jh.py before executing this code.        #
#########################################################################

maximumAgeDiff = 122.0 #2012-1890
nTrainingData = 38332489
alpha0=0.01

def sigmoid(X):
	den = 1.0 + np.e**(-1.0*X)
	d=1.0/den
	return d

def compute_cost(theta,X,y):
	h=sigmoid(X.dot(theta))
	cost = 0.5*((h-y)**2)
	return cost

def update(theta, X, y,eta):
	h = sigmoid(X.dot(theta))
	theta = theta - eta*(h-y)*X
	return theta


# The format of train_finalist_jh.csv is as follows:
# [userid] [usergender] [usernumtweets] [usernumtags] [itemid] [itemage] [itemgender] [itemnumtweets] [itemnumtags] [age similarity] [gender similarity] [network similarity] [result] [nItemFollower]
# age similarity = (absolute difference of age) / (maximum age difference)
# gender similarity = if genders are same == 1, elif either age of two users is unknown == 0, else -1
# network similarity = (number of common following links) / (union of following links)
# result = same as rec_log_train.txt. if recommendation succeeds, 1. else, -1
def getField(trainingDataOneLine):
	# pdb.set_trace()
	try:
		userid = trainingDataOneLine[0]
		userage = zscore(int(trainingDataOneLine[1]), 26.43, 1.777981e+01)
		usergender = int(trainingDataOneLine[2])
		usernumtweets = zscore(int(trainingDataOneLine[3]), 214.5, 6.364181e+02)
		usernumtags = zscore(int(trainingDataOneLine[4]), 4.511, 3.894991e+00)
		itemid = trainingDataOneLine[5]
		itemage = zscore(int(trainingDataOneLine[6]), 30.41, 2.056982e+01)
		itemgender = int(trainingDataOneLine[7])
		itemnumtweets = zscore(int(trainingDataOneLine[8]), 246.8, 4.179840e+02)
		itemnumtags = zscore(int(trainingDataOneLine[9]), 2.226, 2.653076e+00)
		ageSim = float(trainingDataOneLine[10])
		genSim = float(trainingDataOneLine[11])
		netSim = float(trainingDataOneLine[12])
		result = int(trainingDataOneLine[13])
		nItemFollower = zscore(int(trainingDataOneLine[14]), 65339, 8.170466e+04)
		itemPopularity = zscore(float(trainingDataOneLine[15]), -855486, 7993707)
		keywordSimilarity = float(trainingDataOneLine[16])
	except:
		print 'exception:',trainingDataOneLine
		print 'exception:',length(trainingDataOneLine)
		raise Exception
#	return (np.array([0.0001, ageSim, genSim, netSim]), result)
	return (np.array([math.sqrt(usernumtweets),math.sqrt(itemnumtweets),ageSim,math.sqrt(nItemFollower)]), result, userid, itemid)

def zscore(value, mean, sd):

	return (value-mean)/sd

def training(trainingPath, nFeatures, cvStart=0, cvEnd=0, all=False):

	if all:
		cvSize = 0
		nTraining = nTrainingData
	else:
		cvSize = cvEnd - cvStart
		nTraining = nTrainingData - cvSize + 0.0

	theta=np.zeros(nFeatures)
	with open(trainingPath, 'rb') as f:
		reader = csv.reader(f,delimiter=',')
		reader.next()
		lineCount=0
		numOfTrained = 0
		cost = 0.0
		for line in reader:
			if all == False:
				if lineCount>=cvStart and lineCount<cvEnd:
					lineCount+=1
					continue
			try:
				field, result,userid,itemid = getField(line)
			except:
				continue
			cost += compute_cost(theta,field,result)
			if numOfTrained%50000==0:
				print '%f\n'%(cost/50000)
				#print numOfTrained
				cost =0.0
			alpha = alpha0-(alpha0 * numOfTrained/nTraining)
			theta=update(theta, field, result,alpha)
			lineCount+=1
			numOfTrained+=1
	return theta

def Validation(path, theta, cvStart=0, cvEnd=0,all=False):
	tp=fp=fn=0
	fout = open('testResult.csv','w')
	with open(path, 'rb') as f:
		lineCount=0
		reader= csv.reader(f,delimiter=',')
		reader.next()
		for line in reader:
			if all == False:
				if lineCount<cvStart or lineCount>=cvEnd:
					lineCount+=1
					continue
			try:
				field,result,userid,itemid = getField(line)
			except:
				continue
			h = sigmoid(field.dot(theta))
			assert h>=0 and h<=1
			predicted=0
			if h >= 0.5:
				predicted = 1
			if predicted == 1 and result==1:
				tp+=1
			elif predicted == 1 and result==0:
				fp+=1
			elif predicted == 0 and result==1:
				fn+=1
			lineCount+=1
			fout.write('%s,%s,%d,%d,%f\n'%(userid,itemid,predicted,result,h))

		f_measure = (2*tp/(2*tp+fp+fn+0.0))
		print 'tp=%d, fp=%d, fn=%d\n'%(tp,fp,fn)
		print 'f-measures=%f\n' % f_measure
	fout.close()
	return f_measure

if __name__=="__main__":

	# this file refers changed training dataset, which only contains data of target users.
	datapath = '../track1'
	testpath = '../track1'
	filename = 'train_finalist.csv'
	testfilename = 'test_finalist.csv'
	trainingPath = os.path.join(datapath, filename)
	testPath = os.path.join(testpath, testfilename)
	nFeatures = 4

	CROSS_VALIDATION = False

	if CROSS_VALIDATION == True:
		cvStart = 0
		cvEnd = 0
		K = 5
		cvSize = nTrainingData/K
		cvEnd = cvStart+cvSize
		fmeasure_sum = 0
		for i in range(0,5):
			print cvStart, cvEnd
			theta = training(trainingPath, nFeatures, cvStart, cvEnd, nFeatures)
			print 'theta:', theta
			fmeasure_sum += Validation(trainingPath, theta, cvStart, cvEnd)
			cvStart = cvEnd
			cvEnd = cvStart + cvSize
		print 'average f-measure:', (fmeasure_sum/K)
	else:
		print 'training'
		theta = training(trainingPath, nFeatures, all=True)
		print 'theta:', theta
		#theta=np.zeros(nFeatures)
		Validation(testPath, theta, all=True)
