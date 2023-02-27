#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import numpy as np

from funcat import *
from funcat.time_series import (
    fit_series,
)

def test_000001():
    from funcat.data.tushare_backend import TushareDataBackend
    set_data_backend(TushareDataBackend())

    T("20161216")
    S("000001.XSHG")

    assert np.equal(round(CLOSE.value, 2), 3122.98)
    assert np.equal(round(OPEN[2].value, 2), 3149.38)
    assert np.equal(round((CLOSE - OPEN).value, 2), 11.47)
    assert np.equal(round((CLOSE - OPEN)[2].value, 2), -8.85)
    assert np.equal(round(((CLOSE / CLOSE[1] - 1) * 100).value, 2), 0.17)
    assert np.equal(round(MA(CLOSE, 60)[2].value, 2), 3131.08)
    assert np.equal(round(MACD().value, 2), -37.18)
    assert np.equal(round(HHV(HIGH, 5).value, 2), 3245.09)
    assert np.equal(round(LLV(LOW, 5).value, 2), 3100.91)
    assert COUNT(CLOSE > OPEN, 5) == 2

def test_000002():
    from funcat.data.rqalpha_data_backend import RQAlphaDataBackend
    set_data_backend(RQAlphaDataBackend())

    # T("20160104")
    # T("20150727")
    # T("20140703")
    T("20230103")
    S("000001.XSHG")

    dkx,madkx = DKX()
    print(dkx,madkx)
    c_dn_dkx = CROSS(madkx, dkx)
    if c_dn_dkx:
        series1, series2, series3 = fit_series(dkx.series, c_dn_dkx.series, madkx.series)
        series_m = (series1[series2] + series3[series2]*2) / 3
        if series_m[-1] < series_m[-2] and series_m[-1] / series_m[-2] > 0.9:
            print('死叉M头信号', series_m[-1], series_m[-2])
    elif REF(dkx,1) - REF(madkx,1) > dkx - madkx > 0:
        series1, series2, series3 = fit_series(dkx.series, c_dn_dkx.series, madkx.series)
        series_m = (series1[series2] + series3[series2]*2) / 3
        if madkx < series_m[-1] and CLOSE < madkx < MAX(HIGH, REF(CLOSE,1)):
            print('穿黄线M头信号', series_m[-1], CLOSE, madkx, MAX(HIGH, REF(CLOSE,1)))
    #
    c_up_dkx = CROSS(dkx, madkx)
    if c_up_dkx:
        series1, series2, series3 = fit_series(dkx.series, c_up_dkx.series, madkx.series)
        series_w = (series1[series2] + series3[series2]*2) / 3
        if series_w[-1] > series_w[-2] and series_w[-1] / series_w[-2] < 1.1:
            print('金叉W底信号', series_w[-1], series_w[-2])
    elif REF(dkx,1) - REF(madkx,1) > dkx - madkx > 0:
        series1, series2, series3 = fit_series(dkx.series, c_up_dkx.series, madkx.series)
        series_w = (series1[series2] + series3[series2]*2) / 3
        if madkx > series_w[-1] and CLOSE > dkx > MIN(LOW, REF(CLOSE,1)):
            print('穿白线W底信号', series_w[-1], CLOSE, madkx, MAX(HIGH, REF(CLOSE,1)))


    top,left,right,bottom = BOX_BOX_UP()
    print(top,left,right,bottom)

    tops, btms = BTB(OPEN, CLOSE, HIGH, LOW)
    print(tops.series, btms.series)

if __name__ == '__main__':
    test_000002()