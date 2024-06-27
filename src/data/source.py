from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from .loader import DataSchema


@dataclass
class DataSource:
    _data: pd.DataFrame

    @property
    def df(self) -> pd.DataFrame:
        return self._data