
from pyspark.ml.classification import NaiveBayes

import modelutils

import os
train,test,Traindf, Testdf, data = modelutils.getModelData([0.7,0.3])

nb =  NaiveBayes(labelCol="Label",
                    featuresCol="features")
nb_model = nb.fit(Traindf)
nbeval = modelutils.getEvaluationMetrics(nb_model, Testdf)

