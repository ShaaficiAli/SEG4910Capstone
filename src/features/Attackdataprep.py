import pandas as pd
import numpy as np
import math
import os
def getpandasfromcsvs(list_of_csv):
    pdList = [pd.read_csv(csv) for csv in list_of_csv]
    return pdList

def extractColumnFromListPandas(list_of_PD,columns):
    ColumnPD = [elem[columns] for elem in list_of_PD]
    finalPD = pd.concat(ColumnPD,ignore_index = True)
    return finalPD
def getQueryFromInfo(infostring):
    infowordList = infostring.split(' ')
    try:
        queryIndex = infowordList.index('TXT') + 1
        if 'init' not in infowordList[queryIndex]:
            return infowordList[queryIndex]
    except:
        return np.nan
def getSubdomainLength(query):
    ''
    labels = query.split('.')
    labels.pop()
    return sum(len(label) for label in labels)
    
def getUppercaseCount(query):
    return sum(1 for letter in query if letter.isupper())
def getLowercaseCount(query):
    return sum(1 for letter in query if letter.islower())
def getNumericCount(query):
    return sum(1 for letter in query if letter.isnumeric())
def getEntropyCount(query):
    'Returns Shannons entropy of a string'
    prob = [float(query.count(char)/len(query)) for char in dict.fromkeys(list(query))]
    entropy = -sum([p*math.log(p,2) for p in prob])
    return entropy

def getSpecialCharCount(query):
    return sum(1 for letter in query if (not letter.isalnum()))
def getLabelsMax(query):
    labels = query.split('.')
    
    return max(len(label) for label in labels)
def getLabelAvg(query):
    labels = query.split('.')
    sumlabel = sum(len(label) for label in labels)
    avglabel = sumlabel/len(labels)
    return avglabel
def getLabelNum(query):
    return len(query.split('.'))
  
def getLengthDomain(query):
    ''
    labels = query.split('.')
    return len(labels.pop())
    
    
if __name__ == "__main__":
    listpd = getpandasfromcsvs(['dnscapturecsv.csv',
                                'dnscapturefirstcsv.csv',
                                'dnscapturesecond.csv',
                                'dnscapturethirdcsv.csv'])
    finalpd = extractColumnFromListPandas(listpd,['Info','Length'])


    finalpd['Website']=finalpd['Info'].apply(lambda x: getQueryFromInfo(x))
    finalpd.dropna(inplace=True)
    finalpd['Subdomain length'] = finalpd['Website'].apply(lambda x: getSubdomainLength(x))
    finalpd['Uppercase count']= finalpd['Website'].apply(lambda x: getUppercaseCount(x))
    finalpd['Lowercase count']=finalpd['Website'].apply(lambda x: getLowercaseCount(x))
    finalpd['Numeric count'] = finalpd['Website'].apply(lambda x: getNumericCount(x))
    finalpd['Entropy'] = finalpd['Website'].apply(lambda x: getEntropyCount(x))
    finalpd['Special Char Count'] = finalpd['Website'].apply(lambda x: getSpecialCharCount(x))
    finalpd['Max label length'] = finalpd['Website'].apply(lambda x: getLabelsMax(x))
    finalpd['Average label length'] = finalpd['Website'].apply(lambda x: getLabelAvg(x))
    finalpd['Number of Labels'] = finalpd['Website'].apply(lambda x: getLabelNum(x))
    finalpd['Length of domain'] = finalpd['Website'].apply(lambda x: getLengthDomain(x))
    finalpd['Label'] = 1
    finalpd.drop(labels="Info",axis=1,inplace=True)
    finalpd.reset_index(drop=True,inplace=True)
    finalpd.to_csv('MalicousDataset.csv')
