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

def writeOutCSV(dictToWrite, filepath):
	with open(filepath, 'w') as tsvfile:
		for keylist in dictToWrite.keys():
			tmp = list(keylist)
			tmp += dictToWrite[keylist]
			row = '\t'.join(tmp) + '\n'
			tsvfile.write(row)

def appendData(allSchoolDict, oneClassDict, className):
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
					allSchoolDict[allSchoolKey] += (oneClassDict[classKey])
					allSchoolDict[allSchoolKey].append('Matched from %s' %className)
					oneClassDict[classKey].append('Match found')
				elif (name == asName) and (fuzz.ratio(dob, asDOB) < 90):
					allSchoolDict[allSchoolKey] += (oneClassDict[classKey])
					allSchoolDict[allSchoolKey].append('Matched from %s' %className)
					oneClassDict[classKey].append('DOB match less than 90 (%s, %s)' %(dob, asDOB))
				elif (90 < fuzz.ratio(name, asName) < 100) and (fuzz.ratio(dob, asDOB) >= 90):
					allSchoolDict[allSchoolKey] += (oneClassDict[classKey])
					allSchoolDict[allSchoolKey].append('Matched from %s' %className)
					oneClassDict[classKey].append('Name match between 90 and 100 (%s, %s) ' %(name, asName))
				elif (75 < fuzz.ratio(name, asName) < 90) and (fuzz.ratio(dob, asDOB) >= 90):
					allSchoolDict[allSchoolKey].append(('Possible match %s in %s' %(name, className)))
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

def buildNewAllSchool(oldAllSchoolPath, newRosterPath):
	oldAllSchool = readInCSV(oldAllSchoolPath)
	newRoster = readInCSV(newRosterPath)
	for newKey in newRoster.keys():
		name = newKey[0]
		gender = newKey[1]
		dob = newKey[2]
		for oldKey in oldAllSchool.keys():
			oldName = oldKey[0]
			oldGender = oldKey[1]
			oldDOB = oldKey[2]
			if gender == oldGender:
				if (name.strip() == oldName.strip()) and (fuzz.ratio(dob, oldDOB) >= 90):
					newRoster[newKey].append(oldAllSchool[oldKey])
					oldAllSchool[oldKey].append('Match found')
				elif (name.strip() == oldName.strip()) and (fuzz.ratio(dob, oldDOB) < 90):
					newRoster[newKey].append(oldAllSchool[oldKey])
					oldAllSchool[oldKey].append('DOB match less tan 90 (%s, %s)' %(dob, oldDOB))
				elif (90 < fuzz.ratio(name.strip(), oldName.strip()) < 100) and (fuzz.ratio(dob, oldDOB) >= 90):
					newRoster[newKey].append(oldAllSchool[oldKey])
					oldAllSchool[oldKey].append('Name match between 90 and 100 (%s, %s)' %(name, oldName))
				elif (75 < fuzz.ratio(name.strip(), oldName.strip()) < 90) and (fuzz.ratio(dob, oldDOB) >= 90):
					oldAllSchool[oldKey].append('Name match between 75 and 90 (%s, %s) - no data inserted' %(name, oldName))
	return oldAllSchool, newRoster

def execute(allSchoolFilename):
	data = prepare(allSchoolFilename)
	allSchoolDict = data[0]
	classDicts = data[1]
	modifiedClasses = {}
	for key in classDicts:
		modifiedClasses[key] = appendData(allSchoolDict, classDicts[key], key)
	writeOutCSV(allSchoolDict, outputPath + '/all_school.csv')
	for className in modifiedClasses.keys():
		writeOutCSV(modifiedClasses[className], outputPath + '/' + className + '.csv')

def executeNewAllSchool(oldAllSchoolPath, newRosterPath):
	oldAllSchool, newRoster = buildNewAllSchool(oldAllSchoolPath, newRosterPath)
	writeOutCSV(oldAllSchool, outputPath + '/oldAllSchool.csv')
	writeOutCSV(newRoster, outputPath + '/newRoster.csv')