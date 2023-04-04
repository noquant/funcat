# -*- coding: utf-8 -*-

from .api import (
    OPEN, HIGH, LOW, CLOSE, VOLUME, AMO,
    ABS, MIN, MAX, HHV, LLV, CROSS,
    REF, IF, SUM, STD,
    MA, WMA, EMA, SMA, CCI, BTB,
)
from .time_series import (
    NumericSeries,
)

def KDJ(N=9, M1=3, M2=3):
    """
    KDJ 随机指标
    """
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = K * 3 - D * 2

    return K, D, J


def DMI(M1=14, M2=6):
    """
    DMI 趋向指标
    """
    TR = SUM(MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1))), M1)
    HD = HIGH - REF(HIGH, 1)
    LD = REF(LOW, 1) - LOW

    DMP = SUM(IF((HD > 0) & (HD > LD), HD, 0), M1)
    DMM = SUM(IF((LD > 0) & (LD > HD), LD, 0), M1)
    DI1 = DMP * 100 / TR
    DI2 = DMM * 100 / TR
    ADX = MA(ABS(DI2 - DI1) / (DI1 + DI2) * 100, M2)
    ADXR = (ADX + REF(ADX, M2)) / 2

    return DI1, DI2, ADX, ADXR


def MACD(SHORT=12, LONG=26, M=9):
    """
    MACD 指数平滑移动平均线
    """
    DIFF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
    DEA = EMA(DIFF, M)
    MACD = (DIFF - DEA) * 2

    return DIFF, DEA, MACD


def RSI(N1=6, N2=12, N3=24):
    """
    RSI 相对强弱指标
    """
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1, 1) / SMA(ABS(CLOSE - LC), N1, 1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2, 1) / SMA(ABS(CLOSE - LC), N2, 1) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3, 1) / SMA(ABS(CLOSE - LC), N3, 1) * 100

    return RSI1, RSI2, RSI3


def BOLL(N=20, P=2):
    """
    BOLL 布林带
    """
    MID = MA(CLOSE, N)
    C_STD_P = STD(CLOSE, N) * P
    UPPER = MID + C_STD_P
    LOWER = MID - C_STD_P

    return UPPER, MID, LOWER


def WR(N=10, N1=6):
    """
    W&R 威廉指标
    """
    WR1 = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR2 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100

    return WR1, WR2


def TQA(N1=20, N2=10):
    """
    TQA 唐奇安
    """
    TQA_H = REF(HHV(HIGH, N1), 1)
    TQA_L = REF(LLV(LOW, N2), 1)

    return TQA_H, TQA_L


def BIAS(L1=5, L4=3, L5=10):
    """
    BIAS 乖离率
    """
    BIAS = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L4)) / MA(CLOSE, L4) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L5)) / MA(CLOSE, L5) * 100

    return BIAS, BIAS2, BIAS3


def ASI(M1=26, M2=10):
    """
    ASI 震动升降指标
    """
    LC = REF(CLOSE, 1)
    AA = ABS(HIGH - LC)
    BB = ABS(LOW - LC)
    CC = ABS(HIGH - REF(LOW, 1))
    DD = ABS(LC - REF(OPEN, 1))
    R = IF((AA > BB) & (AA > CC), AA + BB / 2 + DD / 4, IF((BB > CC) & (BB > AA), BB + AA / 2 + DD / 4, CC + DD / 4))
    X = (CLOSE - LC + (CLOSE - OPEN) / 2 + LC - REF(OPEN, 1))
    SI = X * 16 / R * MAX(AA, BB)
    ASI = SUM(SI, M1)
    ASIT = MA(ASI, M2)

    return ASI, ASIT


def ATR(N=14):
    """
    ATR 真实波幅
    """
    MTR = MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW))
    ATR = MA(MTR,N)

    return MTR, ATR


def VR(M1=26):
    """
    VR容量比率
    """
    LC = REF(CLOSE, 1)
    VR = SUM(IF(CLOSE > LC, VOLUME, 0), M1) / SUM(IF(CLOSE <= LC, VOLUME, 0), M1) * 100

    return VR


def VOL(M1=5, M2=10):
    """
    VOL 成交量及平均
    """
    MAVOL1 = MA(VOLUME, M1)
    MAVOL2 = MA(VOLUME, M2)

    return VOLUME, MAVOL1, MAVOL2


def AMOUNT(M1=6, M2=12, M3=24):
    """
    AMO 成交额及平均
    """
    MAAMO1 = MA(AMO, M1)
    MAAMO2 = MA(AMO, M2)
    MAAMO3 = MA(AMO, M3)

    return AMO, MAAMO1, MAAMO2, MAAMO3


def ARBR(M1=26):
    """
    ARBR人气意愿指标
    """
    AR = SUM(HIGH - OPEN, M1) / SUM(OPEN - LOW, M1) * 100
    BR = SUM(MAX(0, HIGH - REF(CLOSE, 1)), M1) / SUM(MAX(0, REF(CLOSE, 1) - LOW), M1) * 100

    return AR, BR


def DPO(M1=20, M2=10, M3=6):
    DPO = CLOSE - REF(MA(CLOSE, M1), M2)
    MADPO = MA(DPO, M3)

    return DPO, MADPO


def TRIX(M1=12, M2=20):
    TR = EMA(EMA(EMA(CLOSE, M1), M1), M1)
    TRIX = (TR - REF(TR, 1)) / REF(TR, 1) * 100
    TRMA = MA(TRIX, M2)

    return TRIX, TRMA


def BBI(M1=3, M2=6, M3=12, M4=24):
    """
    BBI 多空指标
    """    
    BBI = (MA(CLOSE,M1)+MA(CLOSE,M2)+MA(CLOSE,M3)+MA(CLOSE,M4))/4

    return BBI


def BBIBOLL(N=11, M=3):
    """
    BBIBOLL 多空指标
    """    
    BBIBOLL = (MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
    UPR = BBIBOLL+M*STD(BBIBOLL,N)
    DWN = BBIBOLL-M*STD(BBIBOLL,N)

    return BBIBOLL, UPR, DWN


def DKX(M=10):
    """
    DKX 多空线
    """    
    MID = (3*CLOSE+LOW+OPEN+HIGH)/6
    # DKX = (20*MID+19*REF(MID,1)+18*REF(MID,2)+17*REF(MID,3)+
    #     16*REF(MID,4)+15*REF(MID,5)+14*REF(MID,6)+
    #     13*REF(MID,7)+12*REF(MID,8)+11*REF(MID,9)+
    #     10*REF(MID,10)+9*REF(MID,11)+8*REF(MID,12)+
    #     7*REF(MID,13)+6*REF(MID,14)+5*REF(MID,15)+
    #     4*REF(MID,16)+3*REF(MID,17)+2*REF(MID,18)+REF(MID,20))/210
    DKX = WMA(MID, 20)
    MADKX = MA(DKX, M)

    return DKX, MADKX


def ZIG(K=3, N=10):
    """计算之字转向"""
    if isinstance(K, int):
        if K == 0:
            hhv = HHV(OPEN, 12)
            llv = LLV(OPEN, 12)
        elif K == 1:
            hhv = HHV(HIGH, 12)
            llv = LLV(HIGH, 12)
        elif K == 2:
            hhv = HHV(LOW, 12)
            llv = LLV(LOW, 12)
        elif K == 3:
            hhv = HHV(CLOSE, 12)
            llv = LLV(CLOSE, 12)
        elif K == 4:
            hhv = HHV(HIGH, 12)
            llv = LLV(LOW, 12)
        else:
            hhv = HHV(CLOSE, 12)
            llv = LLV(CLOSE, 12)
    else:
        hhv = HHV(K, 12)
        llv = LLV(K, 12)
    #
    count = min(len(hhv), len(llv)) - 1
    # print(hhv.series)
    # print(llv.series)
    cur_stat = None
    last_h = ('high', hhv.value, 0)
    last_l = ('low', llv.value, 0)
    peak_list = []
    for i in range(1, count):
        if cur_stat is None:
            # 状态为空时候初始化，需要同时判断峰谷两个点
            new_h1, new_h2, new_h3 = REF(hhv, i+1).value, REF(hhv, i).value, REF(hhv, i-1).value
            if new_h1 < new_h2 == new_h3 and new_h2 >= last_h[1]:
                last_h = ('high', new_h2, i)
                # 涨幅还是跌幅
                if last_h[2] > last_l[2]:
                    chg_ratio = (last_h[1] - last_l[1]) / last_h[1]
                else:
                    chg_ratio = (last_h[1] - last_l[1]) / last_l[1]
                # 阈值判断
                if chg_ratio > N/100:
                    if last_h[2] > last_l[2]:
                        peak_list.append(last_l)
                        peak_list.append(last_h)
                    else:
                        peak_list.append(last_h)
                        peak_list.append(last_l)
                    cur_stat = -1
            new_l1, new_l2, new_l3 = REF(llv, i+1).value, REF(llv, i).value, REF(llv, i-1).value
            if new_l1 > new_l2 == new_l3 and new_l2 <= last_l[1]:
                last_l = ('low', new_l2, i)
                # 涨幅还是跌幅
                if last_h[2] > last_l[2]:
                    chg_ratio = (last_h[1] - last_l[1]) / last_h[1]
                else:
                    chg_ratio = (last_h[1] - last_l[1]) / last_l[1]
                # 阈值判断
                if chg_ratio > N/100:
                    if last_h[2] > last_l[2]:
                        peak_list.append(last_l)
                        peak_list.append(last_h)
                    else:
                        peak_list.append(last_h)
                        peak_list.append(last_l)
                    cur_stat = 1
            pass
        else:
            # 检测波峰并判断是否复合条件
            new_h1, new_h2, new_h3 = REF(hhv, i+1).value, REF(hhv, i).value, REF(hhv, i-1).value
            if new_h1 < new_h2 == new_h3:
                # print(new_h1, new_h2, new_h3)
                flag, last_c, idx = peak_list[-1]
                if flag == 'high':
                    if new_h2 > last_c:
                        peak_list[-1] = ('high', new_h2, i)
                    else:
                        pass
                elif (new_h2 - last_c) / new_h2 > N/100:  # 跌幅
                    peak_list.append(('high', new_h2, i))
            # 检测波峰并判断是否复合条件
            new_l1, new_l2, new_l3 = REF(llv, i+1).value, REF(llv, i).value, REF(llv, i-1).value
            if new_l1 > new_l2 == new_l3:
                # print(new_l1, new_l2, new_l3)
                flag, last_c, idx = peak_list[-1]
                if flag == 'low':
                    if new_l2 < last_c:
                        peak_list[-1] = ('low', new_l2, i)
                    else:
                        pass
                elif (last_c - new_l2) / new_l2 > N/100:  # 涨幅
                    peak_list.append(('low', new_l2, i))
    #
    bool_list, h_bool_list, l_bool_list = [], [], []
    i = 0
    for p in peak_list:
        while i != p[2]:
            bool_list.append(False)
            h_bool_list.append(False)
            l_bool_list.append(False)
            i += 1
        if p[0] == 'low':
            h_bool_list.append(False)
            l_bool_list.append(True)
        else:
            h_bool_list.append(True)
            l_bool_list.append(False)
        bool_list.append(True)
        i += 1
    bool_list.reverse()
    h_bool_list.reverse()
    l_bool_list.reverse()
    #
    if isinstance(K, int):
        # o,h,l,c 对应返回
        if K in (0, 1, 2, 3):
            if K == 0:
                series = CLOSE.series[-len(bool_list):]
            elif K == 1:
                series = HIGH.series[-len(bool_list):]
            elif K == 2:
                series = LOW.series[-len(bool_list):]
            elif K == 3:
                series = CLOSE.series[-len(bool_list):]
            a_series = series[bool_list]
            h_series = series[h_bool_list]
            l_series = series[l_bool_list]
        else:
            close_series = CLOSE.series[-len(bool_list):]
            high_series = HIGH.series[-len(bool_list):]
            low_series = LOW.series[-len(bool_list):]

            a_series = close_series[bool_list]
            h_series = high_series[h_bool_list]
            l_series = low_series[l_bool_list]
    else:
        series = K.series[-len(bool_list):]
        #
        a_series = series[bool_list]
        h_series = series[h_bool_list]
        l_series = series[l_bool_list]
    # print(peak_list)
    # print(series)
    return NumericSeries(a_series), NumericSeries(h_series), NumericSeries(l_series), bool_list


def BOX_FIND(Direction=None, M1=20):
    """
    BOX_FIND 箱体查找
    """    
    if Direction is None:
        if REF(CLOSE,1) > REF(OPEN,1):
            Direction = 1
        else:
            Direction = -1
    # 不一定能够找到箱体
    if Direction == 1:
        begin_i, end_i = M1, 0
        for i in range(1, M1):
            if REF(CLOSE,i) > REF(OPEN,i):
                begin_i = i
                for j in range(begin_i, M1):
                    if not REF(CLOSE,j) > REF(OPEN,j):
                        break
                end_i = j - 1
                break
        # print(begin_i, end_i)
        if end_i >= begin_i:
            # 箱体区间
            return REF(LOW, end_i), REF(OPEN, end_i), REF(CLOSE, begin_i), REF(HIGH, begin_i)
    else:
        begin_i, end_i = M1, 0
        for i in range(1, M1):
            if REF(CLOSE,i) < REF(OPEN,i):
                begin_i = i
                for j in range(begin_i, M1):
                    if not REF(CLOSE,j) < REF(OPEN,j):
                        break
                end_i = j - 1
                break
        # print(begin_i, end_i)
        if end_i >= begin_i:
            # 箱体区间
            return REF(HIGH, end_i), REF(OPEN, end_i), REF(CLOSE, begin_i), REF(LOW, begin_i)
        
        
def BOX_DOWN(M2=20):
    """
    BOX_DOWN 查找前面周期连续阳线，来确定向下突破箱体
    """
    start_i, stop_i = 1, M2
    begin_i, end_i = M2, 0
    # for i in range(start_i, stop_i):
    #     if REF(CLOSE,i) > REF(OPEN,i) or (REF(CLOSE,i) == REF(OPEN,i) and REF(CLOSE,i) > REF(CLOSE,i+1)):
    #         begin_i = i
    #         for j in range(begin_i, stop_i):
    #             if not REF(CLOSE,j) > REF(OPEN,j):
    #                 break
    #         end_i = j - 1
    #         break
    c_index, c_series, o_index, o_series = len(CLOSE) - 1, CLOSE.series, len(OPEN) - 1, OPEN.series
    for i in range(start_i, stop_i):
        if c_series[c_index-i] > o_series[o_index-i] or (c_series[c_index-i] == o_series[o_index-i] and c_series[c_index-i] > c_series[c_index-(i+1)]):
            begin_i = i
            for j in range(begin_i, stop_i):
                if not (c_series[c_index-j] > o_series[o_index-j] or (c_series[c_index-j] == o_series[o_index-j] and c_series[c_index-j] > c_series[c_index-(j+1)])):
                    break
            end_i = j - 1
            break
    # 不一定能够找到箱体
    if end_i >= begin_i:
        # 第一个箱体区间
        n1 = end_i - begin_i
        if n1 <= 1:
            bottom1, top1 = MIN(REF(LOW, end_i), REF(LOW, begin_i)), MAX(REF(HIGH, end_i), REF(HIGH, begin_i))
        else:
            bottom1, top1 = LLV(REF(LOW, begin_i), n1+1), HHV(REF(HIGH, begin_i), n1+1)
        return bottom1, top1
    #
    return None, None

 
def BOX_UP(M2=20):
    """
    BOX_UP 查找前面周期连续阴线，来确定向上突破箱体
    """
    start_i, stop_i = 1, M2
    begin_i, end_i = M2, 0
    # for i in range(start_i, stop_i):
    #     if REF(CLOSE,i) < REF(OPEN,i) or (REF(CLOSE,i) == REF(OPEN,i) and REF(CLOSE,i) < REF(CLOSE,i+1)):
    #         begin_i = i
    #         for j in range(begin_i, stop_i):
    #             if not REF(CLOSE,j) < REF(OPEN,j):
    #                 break
    #         end_i = j - 1
    #         break
    c_index, c_series, o_index, o_series = len(CLOSE) - 1, CLOSE.series, len(OPEN) - 1, OPEN.series
    for i in range(start_i, stop_i):
        if c_series[c_index-i] < o_series[o_index-i] or (c_series[c_index-i] == o_series[o_index-i] and c_series[c_index-i] <= c_series[c_index-(i+1)]):
            begin_i = i
            for j in range(begin_i, stop_i):
                if not (c_series[c_index-j] < o_series[o_index-j] or (c_series[c_index-j] == o_series[o_index-j] and c_series[c_index-j] <= c_series[c_index-(j+1)])):
                    break
            end_i = j - 1
            break
    # 不一定能够找到箱体
    if end_i >= begin_i:
        # 第一个箱体区间
        n1 = end_i - begin_i
        if n1 <= 1:
            top1, bottom1 = MAX(REF(HIGH, end_i), REF(HIGH, begin_i)), MIN(REF(LOW, end_i), REF(LOW, begin_i))
        else:
            top1, bottom1 = HHV(REF(HIGH, begin_i), n1+1), LLV(REF(LOW, begin_i), n1+1)
        return top1, bottom1
    #
    return None, None

                
def BOX_BOX_DOWN(M2=20):
    """
    BOX_DOWN 查找前面周期连续阳线，来确定向下突破箱体
    """
    start_i, stop_i = 1, M2
    begin_i, end_i = M2, 0
    # for i in range(start_i, stop_i):
    #     if REF(CLOSE,i) > REF(OPEN,i) or (REF(CLOSE,i) == REF(OPEN,i) and REF(CLOSE,i) > REF(CLOSE,i+1)):
    #         begin_i = i
    #         for j in range(begin_i, stop_i):
    #             if not (REF(CLOSE,j) > REF(OPEN,j) or (REF(CLOSE,j) == REF(OPEN,j) and REF(CLOSE,j) > REF(CLOSE,j+1))):
    #                 break
    #         end_i = j - 1
    #         break
    c_index, c_series, o_index, o_series = len(CLOSE) - 1, CLOSE.series, len(OPEN) - 1, OPEN.series
    for i in range(start_i, stop_i):
        if c_series[c_index-i] > o_series[o_index-i] or (c_series[c_index-i] == o_series[o_index-i] and c_series[c_index-i] > c_series[c_index-(i+1)]):
            begin_i = i
            for j in range(begin_i, stop_i):
                if not (c_series[c_index-j] > o_series[o_index-j] or (c_series[c_index-j] == o_series[o_index-j] and c_series[c_index-j] > c_series[c_index-(j+1)])):
                    break
            end_i = j - 1
            break
    # 不一定能够找到箱体
    if end_i >= begin_i:
        # 第一个箱体区间
        n1 = end_i - begin_i
        if n1 <= 1:
            bottom1, top1 = MIN(REF(LOW, end_i), REF(LOW, begin_i)), MAX(REF(HIGH, end_i), REF(HIGH, begin_i))
        else:
            bottom1, top1 = LLV(REF(LOW, begin_i), n1+1), HHV(REF(HIGH, begin_i), n1+1)
        # 之后再找第二个
        start_i, stop_i = 1 + end_i, M2 + end_i
        begin_i, end_i = M2, 0
        # for i in range(start_i, stop_i):
        #     if REF(CLOSE,i) > REF(OPEN,i) or (REF(CLOSE,i) == REF(OPEN,i) and REF(CLOSE,i) > REF(CLOSE,i+1)):
        #         begin_i = i
        #         for j in range(begin_i, stop_i):
        #             if not (REF(CLOSE,j) > REF(OPEN,j) or (REF(CLOSE,j) == REF(OPEN,j) and REF(CLOSE,j) > REF(CLOSE,j+1))):
        #                 break
        #         end_i = j - 1
        #         break
        for i in range(start_i, stop_i):
            if c_series[c_index-i] > o_series[o_index-i] or (c_series[c_index-i] == o_series[o_index-i] and c_series[c_index-i] > c_series[c_index-(i+1)]):
                begin_i = i
                for j in range(begin_i, stop_i):
                    if not (c_series[c_index-j] > o_series[o_index-j] or (c_series[c_index-j] == o_series[o_index-j] and c_series[c_index-j] > c_series[c_index-(j+1)])):
                        break
                end_i = j - 1
                break
        if end_i >= begin_i:
            n2 = end_i - begin_i
            if n2 <= 1:
                bottom2, top2 = MIN(REF(LOW, end_i), REF(LOW, begin_i)), MAX(REF(HIGH, end_i), REF(HIGH, begin_i))
            else:
                bottom2, top2 = LLV(REF(LOW, begin_i), n2+1), HHV(REF(HIGH, begin_i), n2+1)
            return bottom1, top1, bottom2, top2
        else:
            return bottom1, top1, None, None
    #
    return None, None, None, None

   
def BOX_BOX_UP(M2=20):
    """
    BOX_UP 查找前面周期连续阴线，来确定向上突破箱体
    """
    start_i, stop_i = 1, M2
    begin_i, end_i = M2, 0
    # for i in range(start_i, stop_i):
    #     if REF(CLOSE,i) < REF(OPEN,i) or (REF(CLOSE,i) == REF(OPEN,i) and REF(CLOSE,i) <= REF(CLOSE,i+1)):
    #         begin_i = i
    #         for j in range(begin_i, stop_i):
    #             if not (REF(CLOSE,j) < REF(OPEN,j) or (REF(CLOSE,j) == REF(OPEN,j) and REF(CLOSE,j) <= REF(CLOSE,j+1))):
    #                 break
    #         end_i = j - 1
    #         break
    c_index, c_series, o_index, o_series = len(CLOSE) - 1, CLOSE.series, len(OPEN) - 1, OPEN.series
    for i in range(start_i, stop_i):
        if c_series[c_index-i] < o_series[o_index-i] or (c_series[c_index-i] == o_series[o_index-i] and c_series[c_index-i] <= c_series[c_index-(i+1)]):
            begin_i = i
            for j in range(begin_i, stop_i):
                if not (c_series[c_index-j] < o_series[o_index-j] or (c_series[c_index-j] == o_series[o_index-j] and c_series[c_index-j] <= c_series[c_index-(j+1)])):
                    break
            end_i = j - 1
            break
    # 不一定能够找到箱体
    if end_i >= begin_i:
        # 第一个箱体区间
        n1 = end_i - begin_i
        if n1 <= 1:
            top1, bottom1 = MAX(REF(HIGH, end_i), REF(HIGH, begin_i)), MIN(REF(LOW, end_i), REF(LOW, begin_i))
        else:
            top1, bottom1 = HHV(REF(HIGH, begin_i), n1+1), LLV(REF(LOW, begin_i), n1+1)
        # 之后再找第二个
        start_i, stop_i = 1 + end_i, M2 + end_i
        begin_i, end_i = M2, 0
        # for i in range(start_i, stop_i):
        #     if REF(CLOSE,i) < REF(OPEN,i) or (REF(CLOSE,i) == REF(OPEN,i) and REF(CLOSE,i) <= REF(CLOSE,i+1)):
        #         begin_i = i
        #         for j in range(begin_i, stop_i):
        #             if not (REF(CLOSE,j) < REF(OPEN,j) or (REF(CLOSE,j) == REF(OPEN,j) and REF(CLOSE,j) <= REF(CLOSE,j+1))):
        #                 break
        #         end_i = j - 1
        #         break
        for i in range(start_i, stop_i):
            if c_series[c_index-i] < o_series[o_index-i] or (c_series[c_index-i] == o_series[o_index-i] and c_series[c_index-i] <= c_series[c_index-(i+1)]):
                begin_i = i
                for j in range(begin_i, stop_i):
                    if not (c_series[c_index-j] < o_series[o_index-j] or (c_series[c_index-j] == o_series[o_index-j] and c_series[c_index-j] <= c_series[c_index-(j+1)])):
                        break
                end_i = j - 1
                break
        if end_i >= begin_i:
            n2 = end_i - begin_i
            if n2 <= 1:
                top2, bottom2 = MAX(REF(HIGH, end_i), REF(HIGH, begin_i)), MIN(REF(LOW, end_i), REF(LOW, begin_i))
            else:
                top2, bottom2 = HHV(REF(HIGH, begin_i), n2+1), LLV(REF(LOW, begin_i), n2+1)
            return top1, bottom1, top2, bottom2
        else:
            return top1, bottom1, None, None
    #
    return None, None, None, None