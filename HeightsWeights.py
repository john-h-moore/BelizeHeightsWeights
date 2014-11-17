import csv, os
from fuzzywuzzy import fuzz

inputPath = os.path.dirname(os.path.realpath(__file__)) + '/input'
outputPath = os.path.dirname(os.path.realpath(__file__)) + '/output'

def readInCSV(filepath):
	csvdict = {}
	with open(filepath, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			name = row[0]
			gender = row[1]
			dob = row[2]
			if 'ROSTER' not in name:
				csvdict[name, gender, dob] = row[3:]
	return csvdict

def appendData(allSchoolDict, oneClassDict):
	for classKey in oneClassDict.keys():
		name = classKey[0]
		gender = classKey[1]
		dob = classKey[2]
		# for allSchoolKey in allSchoolDict.keys():
		# 	asName = allSchoolKey[0]
		# 	asGender = allSchoolKey[1]
		# 	asDOB = allSchoolKey[2]
		# 	if gender == asGender:
		# 		if (name == asName) and (dob == asDOB):
		# 			allSchoolDict[allSchoolKey].append(oneClassDict[classKey])
		# 	else:
		# 		oneClassDict[classKey].append('No match')
		for allSchoolKey in allSchoolDict.keys():
			asName = allSchoolKey[0]
			asGender = allSchoolKey[1]
			asDOB = allSchoolKey[2]
			if gender == asGender:
				if (name == asName) and (fuzz.ratio(dob, asDOB) >= 90):
					allSchoolDict[allSchoolKey].append(oneClassDict[classKey])
					oneClassDict[classKey].append('Match found')
				elif (name == asName) and (fuzz.ratio(dob, asDOB) < 90):
					allSchoolDict[allSchoolKey].append(oneClassDict[classKey])
					oneClassDict[classKey].append('DOB match less than 90 (%s, %s)' %(dob, asDOB))
				elif (90 < fuzz.ratio(name, asName) < 100) and (fuzz.ratio(dob, asDOB) >= 90):
					allSchoolDict[allSchoolKey].append(oneClassDict[classKey])
					oneClassDict[classKey].append('Name match between 90 and 100 (%s, %s) ' %(name, asName))
				elif (75 < fuzz.ratio(name, asName) < 90) and (fuzz.ratio(dob, asDOB) >= 90):
					oneClassDict[classKey].append('Name match between 75 and 90 (%s, %s) - no data inserted' %(name, asName))
	return oneClassDict

def prepare(allSchoolFilename):
	allSchoolDict = readInCSV(inputPath + '/' + allSchoolFilename)
	classDicts = {}
	for csvfilepath in os.listdir(inputPath):
		if 'All' not in csvfilepath:
			teacher = csvfilepath.split('- ')[1].split('.csv')[0]
			oneClassDict = readInCSV(inputPath + '/' + csvfilepath)
			classDicts[teacher] = oneClassDict
	return allSchoolDict, classDicts