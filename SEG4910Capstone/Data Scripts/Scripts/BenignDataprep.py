import os
from Attackdataprep import *
import numpy as np
import pandas as pd

def pingBenignData():
    with open("top-1m.csv") as file:
        WebsiteList = [line.strip('\n').split(",")[1] for line in file.readlines()]
    WebsiteList = WebsiteList[600000:630000]
    for website in WebsiteList:
        os.system("ping -n 1 "+website)
    file.close()

def checkIfResponse(line):
    entries = line.strip('\n').split(",")
    info = entries[-1]
    if 'response' in info:
        return True
    return False
def checkIfTopMillion(line,TopMillDict):
    possibleSites = line.strip('\n').split(" ")
    for site in possibleSites:
        if site in TopMillDict:
            return True
    return False
def getBenignSite(line,TopMillDict):
    possibleSites = line.strip('\n').split(" ")
    for site in possibleSites:
        if site in TopMillDict:
            return site
    return np.nan

def cleanBenignDataset(finalpd):
    
    with open("top-1m.csv") as file:
        WebsiteList = [line.strip('\n').split(",")[1] for line in file.readlines()]
    file.close()
    TopWebsiteDict = {}
    for website in WebsiteList:
        TopWebsiteDict[website]=1
    
    
    finalpd["IfResponse"] = finalpd['Info'].apply(lambda x: checkIfResponse(x))
    finalpd.drop(finalpd.loc[finalpd['IfResponse']==True].index,inplace=True)
    
    finalpd["IfTopMillion"] = finalpd['Info'].apply(lambda x: checkIfTopMillion(x,TopWebsiteDict))
    finalpd.drop(finalpd.loc[finalpd['IfTopMillion']==False].index,inplace=True)
    finalpd["Website"] = finalpd['Info'].apply(lambda x: getBenignSite(x,TopWebsiteDict))
    
    finalpd.drop(labels=["Info","IfTopMillion","IfResponse"],axis=1,inplace=True)


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
    finalpd['Label'] = 0
    finalpd.reset_index(drop=True,inplace=True)

    finalpd.to_csv('BenignDataset.csv')



if __name__ == "__main__":
    ListOfCsv=["100k_200k.csv",
               "400k_to_500k.csv",
               "500000_to_566043.csv",
               "566043_to_600000.csv",
               "benignData900k.csv",
               "shaafici0-100000.csv",
               "benignData400k.csv",
               "LastCSV.csv"]
    listpd = getpandasfromcsvs(ListOfCsv)
    finalpd = extractColumnFromListPandas(listpd,['Info','Length'])
    cleanBenignDataset(finalpd)


