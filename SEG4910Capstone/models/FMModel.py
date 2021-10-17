'''
Creates a factorization machines classification model
Can be found at https://spark.apache.org/docs/latest/ml-classification-regression.html#factorization-machines-classifier
'''
from pyspark.ml.classification import FMClassifier

import modelutils

import pickle

train,test,Traindf, Testdf, data = modelutils.getModelData([0.7,0.3])
 
FM = FMClassifier(labelCol="Label",
                 featuresCol="features",
                  maxIter=10)

FMModel = FM.fit(Traindf)
fmeval = modelutils.getEvaluationMetrics(FMModel, Testdf)

with open('FMModel_pickle', 'wb') as f:
	picke.dump(FMModel, f)
