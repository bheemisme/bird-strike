from functools import reduce
from typing import Callable

import numpy as np
import pandas as pd
import math
Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


class DataSchema:
    pass


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=False)

def iqr_cleaning(df: pd.DataFrame, attr: str, thresh = 0) -> pd.DataFrame:
    if df[attr].dtype == np.float64 or df[attr].dtype == np.float32 or df[attr].dtype == np.int64 or df[attr].dtype == np.int32:
        q1, q2, q3 = df[attr].quantile([.25,.5,.75])
        iqr = q3 - q1
        return df[(df[attr] >= q1 - thresh * iqr) & (df[attr] <= q3 + thresh * iqr)]
    raise ValueError("attr should be of float or int dtype")



def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)

def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()

def load_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path
    )
    preprocessor = compose(
        drop_na,
        remove_duplicates,
    )
    return preprocessor(data)