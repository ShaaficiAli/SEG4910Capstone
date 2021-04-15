from pyspark.ml.classification import FMClassifier

import modelutils

train,test,Traindf, Testdf, data = modelutils.getModelData([0.7,0.3])
 
FM = FMClassifier(labelCol="Label",
                 featuresCol="features",
                  maxIter=10)

FMModel = FM.fit(Traindf)
fmeval = modelutils.getEvaluationMetrics(FMModel, Testdf)
