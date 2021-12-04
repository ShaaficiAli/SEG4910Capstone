import random
from joblib import dump

import numpy as np
import sklearn

dump(clf, './isolation_forest.joblib')

