import csv, os

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