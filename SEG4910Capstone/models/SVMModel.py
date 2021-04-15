from pyspark.ml.classification import LinearSVC
import modelutils

train,test,Traindf, Testdf, data = modelutils.getModelData([0.7,0.3])
 
SVM  = LinearSVC(maxIter=10,
                 regParam=0.1,
                 labelCol="Label",
                 featuresCol="features")

lscvModel = SVM.fit(Traindf)
svmeval = modelutils.getEvaluationMetrics(lscvModel, Testdf)

