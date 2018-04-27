import numpy as np
import pandas as pd
import matplotlib as plt

from skills import readLimitMergeSkills

def gini(array):
    """
    Calculate the Gini coefficient of a numpy array
    """
    # All values are treated equally, arrays must be 1d:
    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)
    # Values cannot be 0:
    array += np.finfo(float).eps
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

def giniMacro(baseFile=None, 
              skillName=None,
              level1='country_sk',
              skillLevel='industry_sk',
              threshold=None):
    """
    Gini sequence
    """
    skillPen = readLimitMergeSkills(baseFile=baseFile, 
                                    skillName=skillName,
                                    level1=level1,
                                    skillLevel=skillLevel,
                                    threshold=threshold)
    
    giniCoeff = pd.Series(index=skillPen.columns)
    for i in np.arange(0, skillPen.shape[1]):
        giniCoeff.iloc[i] = gini(skillPen[skillPen.columns[i]].values)
    
    print('\nDistribution of Gini coeff for each skill across all countries:')
    print(giniCoeff.describe())
    
    giniCoeff.hist(bins=int(giniCoeff.shape[0] / 25))
    
    return giniCoeff.sort_values()
