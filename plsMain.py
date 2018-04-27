import pandas as pd
import numpy as np

from sklearn import cross_decomposition
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import scale

from boxCox import boxcoxTrans

def pls(X=None, y=None, maxComp=40):
    """
    Defines and finds the min MSE PLS regression model using gridsearch and CV
    """
    
    linear = cross_decomposition.PLSRegression()
    pipe = Pipeline(steps=[('linear', linear)])
    
    X_digits = scale(boxcoxTrans(X))
    y_digits = scale(y)

    # Prediction
    n_components = np.arange(1, min(X_digits.shape[0], maxComp) + 1)

    estimator = GridSearchCV(pipe, dict(linear__n_components=n_components))
    estimator.fit(X_digits, y_digits)
    
    return estimator