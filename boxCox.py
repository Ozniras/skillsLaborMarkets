import pandas as pd
import numpy as np
import scipy.stats as stats


def boxcoxTrans(df):
    """
    When passed a DataFrame with only numeric columns and NO zeroes (add 1 to all),
    performs box-cox in each column and pca-Copy1returns transformed matrix
    """
    correction = (df + 1).apply(stats.boxcox)
    for rowtocol in np.arange(correction.shape[0]):
        if rowtocol == 0:
            transformed = pd.DataFrame(correction[rowtocol][0], 
                                       columns = [correction.index[rowtocol]], 
                                       index=df.index) 
        else:
            transformed = pd.merge(transformed, pd.DataFrame(correction[rowtocol][0], 
                                            columns = [correction.index[rowtocol]],
                                           index=df.index), left_index=True, right_index=True)
    
    return transformed