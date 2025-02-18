# -*- coding: utf-8 -*-
#

import copy
import os
import datetime

import numpy as np
from numpy.lib import recfunctions as rfn

from .backend import DataBackend
from ..utils import get_date_from_int, get_int_date

MAX_BAR_COUNT = 10000

class RQAlphaDataBackend(DataBackend):
    """
    目前仅支持日数据
    """
    skip_suspended = True

    def __init__(self, data_proxy=None, rqalpha_path=None):
        #
        self.data_proxy = data_proxy
        self.rqalpha_path = rqalpha_path
        self._datetime = None

    def init(self):
        """"""
        from rqalpha.utils.config import rqalpha_path
        from rqalpha.data.base_data_source import BaseDataSource
        from rqalpha.data.data_proxy import DataProxy

        if self.rqalpha_path is None:
            data_bundle_path = os.path.join(os.path.expanduser(rqalpha_path), "bundle")
        else:
            data_bundle_path = self.rqalpha_path
        self.data_proxy = DataProxy(BaseDataSource(os.path.expanduser(data_bundle_path), {}), None)

    def get_price(self, order_book_id, start, end, freq):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        if self.data_proxy is None:
            self.init()

        assert freq in ("1d", "1w", "1m", "5m", "10m", "15m", "30m", "60m", "D", "W")
        start = get_date_from_int(start)
        end = get_date_from_int(end)
        if freq in ("1d","D"):
            bar_count = min(MAX_BAR_COUNT, (end - start).days)
            bars = self.data_proxy.history_bars(
                order_book_id, bar_count, "1d", field=None,
                dt=datetime.datetime.combine(end, datetime.time(16, 30, 0)))
        elif freq in ("1w","W"):
            bar_count = min(MAX_BAR_COUNT, int((end - start).days / 7)) + 1
            bars = self.data_proxy.history_bars(
                order_book_id, bar_count, "1w", field=None,
                dt=datetime.datetime.combine(end, datetime.time(16, 30, 0)))
        else:
            bars = self.data_proxy.history_bars(
                order_book_id, -1, freq, field=None,
                dt=datetime.datetime.combine(end, datetime.time(16, 30, 0)),
                adjust_orig=datetime.datetime.combine(start - datetime.timedelta(days=1), datetime.time(16, 30, 0)))
            pass
        if bars is None or len(bars) == 0:
            raise KeyError("empty bars {}".format(order_book_id))
        # 只读暂不copy
        # bars = bars.copy()
        self._datetime = bars["datetime"]
        return bars

    def get_order_book_id_list(self, type="CS"):
        """获取所有的
        """
        if self.data_proxy is None:
            self.init()

        import pandas as pd
        insts = self.data_proxy.all_instruments([type])
        if isinstance(insts, pd.DataFrame):
            # for old version of RQAlpha
            return sorted(insts.order_book_id.tolist())
        else:
            # for new version fo RQAlpha
            return sorted([inst.order_book_id for inst in insts])

    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        if self.data_proxy is None:
            self.init()

        return self.data_proxy.instrument(order_book_id).symbol

    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        if self.data_proxy is None:
            self.init()
            
        start = get_date_from_int(start)
        end = get_date_from_int(end)
        trading_dates = self.data_proxy.get_trading_dates(start, end).tolist()
        trading_dates = [get_int_date(dt.date()) for dt in trading_dates]
        return trading_dates

    def get_previous_trading_date(self, start):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        if self.data_proxy is None:
            self.init()
            
        start = get_date_from_int(start)
        trading_date = self.data_proxy.get_previous_trading_date(start)
        trading_date = get_int_date(trading_date.date())
        return trading_date
