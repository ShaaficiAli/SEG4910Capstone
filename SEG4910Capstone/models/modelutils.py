from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.feature import VectorAssembler, VectorIndexer, StringIndexer

from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

from pyspark.mllib.util import MLUtils


import pandas as pd
import numpy as np
'''
A module of functions to ease dataset and ml creation and usage
'''

def createDataset(NumberBenignRecords,NumberMalicousRecords,NameFinalDataset):
    '''
    Create a csv that will contain the training data. Will prioritize
    the top million websites first in the benign records section, with the
    rest being randomly sampled from the rest of the benign dataset

    Keyword Argument:
    NumberBenignRecords: The number of benign records in the dataset
    NumberMalicousRecords:The number of malicious records in the dataset
    NameFinalDataset:The name of the dataset that will be created

    Return:
    : The final pandas dataframe
    '''
    ## get the top million websites
    with open("..\\Data Scripts\\Datasets\\top-1m.csv") as file:
        WebsiteList = [line.strip('\n').split(",")[1] for line in file.readlines()]
    file.close()
    TopWebsiteDict = {}
    for website in WebsiteList:
        TopWebsiteDict[website]=1
    
    BenignDataset = pd.read_csv("..\\Data Scripts\\Datasets\\BenignDataset.csv")
    
    MalicousDataset = pd.read_csv("..\\Data Scripts\\Datasets\\MalicousDataset.csv")
    #check if the arguments contain too many records requested for the final dataset
    if NumberBenignRecords > len(BenignDataset):
            errormsg = "Our Dataset only has {0} benign records and {1} malicous records".format(len(BenignDataset),len(MalicousDataset))
            raise Exception(errormsg)
    #get the set of malicious records for the final dataset
    MalicousSubsection = MalicousDataset.sample(n=NumberMalicousRecords)
    #Get all possible benign records
    BenignSubsection = BenignDataset.drop_duplicates(subset = "Website")
    #Get the set of benign records that are not in the top million website
    BenignSubsectionDifference = BenignDataset[~BenignDataset.apply(tuple,1).isin(BenignSubsection.apply(tuple,1))]
    
    FinalBenignDataset = []
    #if the benign records must be less than the amount
    #of websites in alexa top million, get a sample of the benign
    if NumberBenignRecords < len(BenignDataset):
        FinalBenignDataset = BenignDataset.sample(NumberBenignRecords)
        
    elif NumberBenignRecords > len(BenignSubsection) :
        
        
        NumberBenignDifference = len(BenignDataset) - NumberBenignRecords
        RecordsToAdd = BenignSubsectionDifference.sample(n=NumberBenignDifference)
        FinalBenignDataset = pd.concat(BenignSubsection,RecordsToAdd)
    else:
        FinalBenignDataset = BenignSubsection
    
    FinalDataset = pd.concat([FinalBenignDataset,MalicousSubsection],ignore_index=True)
    FinalDataset.reset_index(drop=True,inplace=True)
    
    FinalDataset.drop(FinalDataset.filter(regex="Unname"),axis=1, inplace=True)
    Path = "..\\Data Scripts\\Datasets\\{0}.csv".format(NameFinalDataset)
    
    FinalDataset.to_csv(Path)
    return FinalDataset

def getModelData(trainingsplit=[0.7,0.3],DataCSV="../Data Scripts/Datasets/FinalDataset.csv"):
    '''
    Create the pyspark dataframes to train ml models
    Keyword arguments:
    trainingsplit: the ratio of training to test samples(default = [0.7,0.3])
    DataCSV: The dataset to get the data from:Default dataset is the one in our
    github
    Returns:
    train: Pyspark dataframe of the train set 
    test: Pyspark dataframe of the test set 
    Traindf: Pyspark dataframe of the Train set that is formatted for pyspark ml models
    Testdf:Pyspark dataframe of the test set that is formatted for pyspark ml models
    data:Pyspark dataframe of the full dataset
    '''
    spark = SparkSession.builder.master("local").appName("SEG CAPSTONE").config(conf=SparkConf()).getOrCreate()
    data = spark.read.options(inferSchema='True',delimiter=',',header='True')\
       .csv(DataCSV)
    data = data.drop('_c0','Website')
    train, test = data.randomSplit(trainingsplit,seed=11)
    print("{0} training examples and {1} test examples.".format(train.count(), test.count()))
    featureColumns = data.columns

    featureColumns.remove('Label')
    assembler = VectorAssembler(inputCols= featureColumns,outputCol="features")
    Traindf = assembler.transform(train)
    Testdf = assembler.transform(test)
    return train,test,Traindf,Testdf,data

def getEvaluationMetrics(model, testData):
    '''

    Keyword arguments:
    model:A pyspark machine learning model to test
    testData:The spark dataframe to test the models on
    
    Returns:
    EvaluationDict: A dictionary containing the f1,accuracy,precision and auc of the model
    '''
    predictions = model.transform(testData).select('Label','prediction')

    evaluatorMulti = MulticlassClassificationEvaluator(labelCol="Label", predictionCol="prediction")
    evaluator = BinaryClassificationEvaluator(labelCol="Label", rawPredictionCol="prediction", metricName='areaUnderROC')

    acc = evaluatorMulti.evaluate(predictions, {evaluatorMulti.metricName: "accuracy"})
    f1 = evaluatorMulti.evaluate(predictions, {evaluatorMulti.metricName: "f1"})
    weightedPrecision = evaluatorMulti.evaluate(predictions, {evaluatorMulti.metricName: "weightedPrecision"})
    weightedRecall = evaluatorMulti.evaluate(predictions, {evaluatorMulti.metricName: "weightedRecall"})
    auc = evaluator.evaluate(predictions)
    EvaluationDict = {}
    EvaluationDict['f1'] = f1
    EvaluationDict['accuracy']=acc
    EvaluationDict['Precision']=weightedPrecision
    EvaluationDict['auc']=auc
    return EvaluationDict


    
