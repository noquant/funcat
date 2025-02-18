# -*- coding: utf-8 -*-
import numpy as np

from .time_series import MarketDataSeries
from .func import (
    SumSeries,
    AbsSeries,
    StdSeries,
    SMASeries,
    CCISeries,
    MovingAverageSeries,
    WeightedMovingAverageSeries,
    ExponentialMovingAverageSeries,
    CrossOver,
    minimum,
    maximum,
    every,
    count,
    hhv,
    llv,
    Ref,
    iif,
    box_top_bottom,
)
from .context import (
    symbol,
    set_current_security,
    get_current_security,
    set_current_date,
    get_current_date,
    set_start_date,
    set_data_backend,
    set_current_freq,
)
from .helper import select


# create open high low close volume datetime
for name in ["open", "high", "low", "close", "volume", "datetime"]:
    dtype = np.float64 if name != "datetime" else np.uint64
    cls = type("{}Series".format(name.capitalize()), (MarketDataSeries, ), {"name": name, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = obj

for field,name in [("total_turnover","amo")]:
    dtype = np.float64
    cls = type("{}Series".format(name.capitalize()), (MarketDataSeries, ), {"name": field, "dtype": dtype})
    obj = cls(dynamic_update=True)
    for var in [name.upper()]:
        globals()[var] = obj

MA = MovingAverageSeries
WMA = WeightedMovingAverageSeries
EMA = ExponentialMovingAverageSeries
SMA = SMASeries
CCI = CCISeries

SUM = SumSeries
ABS = AbsSeries
STD = StdSeries

CROSS = CrossOver
REF = Ref
MIN = minimum
MAX = maximum
EVERY = every
COUNT = count
HHV = hhv
LLV = llv
IF = IIF = iif
BTB = box_top_bottom

S = set_current_security
T = set_current_date


__all__ = [
    "OPEN", "O",
    "HIGH", "H",
    "LOW", "L",
    "CLOSE", "C",
    "VOLUME", "V",
    "DATETIME",

    "AMO",

    "SMA",
    "CCI",
    "MA",
    "EMA",
    "WMA",

    "SUM",
    "ABS",
    "STD",

    "CROSS",
    "REF",
    "MAX",
    "MIN",
    "EVERY",
    "COUNT",
    "HHV",
    "LLV",
    "IF", "IIF",

    "S",
    "T",

    "select",
    "symbol",
    "set_current_security",
    "get_current_security",
    "set_current_date",
    "get_current_date",
    "set_start_date",
    "set_data_backend",
    "set_current_freq",
]
