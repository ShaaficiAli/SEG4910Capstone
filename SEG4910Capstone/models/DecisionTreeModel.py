
from pyspark.ml.classification import DecisionTreeClassifier


import modelutils

import os
train,test,Traindf, Testdf, data = modelutils.getModelData([0.7,0.3])

DecisionTree = DecisionTreeClassifier(labelCol="Label",
                    featuresCol="features")
DecisionTree_model = DecisionTree.fit(Traindf)
Decisioneval = modelutils.getEvaluationMetrics(DecisionTree_model, Testdf)

