'''
Creates a linear support vector machine classification model
Can be found at https://spark.apache.org/docs/latest/ml-classification-regression.html#linear-support-vector-machine
'''
from pyspark.ml.classification import LinearSVC
import modelutils
import pickle
train,test,Traindf, Testdf, data = modelutils.getModelData([0.7,0.3])
 
SVM  = LinearSVC(maxIter=10,
                 regParam=0.1,
                 labelCol="Label",
                 featuresCol="features")

lscvModel = SVM.fit(Traindf)
svmeval = modelutils.getEvaluationMetrics(lscvModel, Testdf)

with open('SVMModel_pickle', 'wb') as f:
	picke.dump(lscvModel, f)
