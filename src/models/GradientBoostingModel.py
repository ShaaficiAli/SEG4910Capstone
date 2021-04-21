'''
Creates a gradient boosted tree classification model
Can be found athttps://spark.apache.org/docs/latest/ml-classification-regression.html#gradient-boosted-tree-classifier
'''

from pyspark.ml.classification import GBTClassifier

import modelutils

import os
train,test,Traindf, Testdf, data = modelutils.getModelData([0.7,0.3])

gbt = GBTClassifier(labelCol="Label",
                    featuresCol="features",
                    maxIter=2)
gbt_model = gbt.fit(Traindf)
gbteval = modelutils.getEvaluationMetrics(gbt_model, Testdf)




