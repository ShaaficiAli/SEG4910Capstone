'''
Creates a binomial regression classification model
Can be found at https://spark.apache.org/docs/latest/ml-classification-regression.html#binomial-logistic-regression
'''
from pyspark.ml.classification import LogisticRegression

import modelutils

import os
train,test,Traindf, Testdf, data = modelutils.getModelData([0.7,0.3])



Binomial = LogisticRegression(labelCol="Label",
                    featuresCol="features",
                    maxIter=5,
                    regParam=0.3,
                    elasticNetParam=0.8)
bi_model = Binomial.fit(Traindf)
bieval = modelutils.getEvaluationMetrics(bi_model, Testdf)

