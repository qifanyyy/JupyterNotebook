import common as cm
import pandas as pd 

def lowerCaseAndExceptions(S): #lower case, ignore numbers, change nan
	try:
		S = S.lower()
	except:
		S = S 
	if(S==""):
		S = " "
	return S

def createMap(column): #Auxiliar, Create map from column
	scol =  sorted(column)
	#print scol
	coldict = {}
	cont = 0
	for e in scol:
		e = lowerCaseAndExceptions(e)
		#print e
		if e not in coldict:
			coldict[e] = cont
			cont = cont + 1
	return coldict

def mapColumn(column):
	columnMap = createMap(column)
	dataMapped = []
	for e in column:
		e = lowerCaseAndExceptions(e)
		dataMapped.append(columnMap[e])
	return dataMapped


def detectColumnType(feature):
	for r in feature:
		try:
			float(r)
		except ValueError:
			return 1
	return 0

def processDataset(filepath):
	df = pd.read_csv(filepath)
	minValue = df.min(axis=1).min(axis=0)
	df.fillna(minValue-1, inplace=True) #removing empty spaces
	for column in df: #transforming not number columns
		if(detectColumnType(df[column])):
			df[column] = mapColumn(df[column])
	#df.to_csv("z-"+filepath, index=False)
	df.to_csv(filepath, index=False)


processDataset('22c.csv')