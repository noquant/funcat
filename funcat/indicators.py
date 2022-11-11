# -*- coding: utf-8 -*-

from .api import (
    OPEN, HIGH, LOW, CLOSE, VOLUME, VOL,
    ABS, MIN, MAX, HHV, LLV,
    REF, IF, SUM, STD,
    MA, EMA, SMA,
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

    return MACD


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
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P

    return UPPER, MID, LOWER


def WR(N=10, N1=6):
    """
    W&R 威廉指标
    """
    WR1 = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR2 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100

    return WR1, WR2


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


def VR(M1=26):
    """
    VR 容量比率
    """
    LC = REF(CLOSE, 1)
    VR = SUM(IF(CLOSE > LC, VOL, 0), M1) / SUM(IF(CLOSE <= LC, VOL, 0), M1) * 100

    return VR


def ARBR(M1=26):
    """
    ARBR 人气意愿指标
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


def DKX(M=10):
    """
    DKX 多空线
    """    
    MID = (3*CLOSE+LOW+OPEN+HIGH)/6
    DKX = (20*MID+19*REF(MID,1)+18*REF(MID,2)+17*REF(MID,3)+
        16*REF(MID,4)+15*REF(MID,5)+14*REF(MID,6)+
        13*REF(MID,7)+12*REF(MID,8)+11*REF(MID,9)+
        10*REF(MID,10)+9*REF(MID,11)+8*REF(MID,12)+
        7*REF(MID,13)+6*REF(MID,14)+5*REF(MID,15)+
        4*REF(MID,16)+3*REF(MID,17)+2*REF(MID,18)+REF(MID,20))/210
    MADKX = MA(DKX, M)

    return DKX, MADKX


def BOX(Direction=None, M1=20):
    """
    BOX 箱体计算
    """    
    if Direction is None:
        if REF(CLOSE,1) > REF(OPEN,1):
            Direction = 1
        else:
            Direction = -1
    #
    if Direction == 1:
        for i in range(1, M1):
            if REF(CLOSE,i) > REF(OPEN,i):
                break
        begin_i = i
        for i in range(begin_i, M1):
            if not REF(CLOSE,i) > REF(OPEN,i):
                break
        end_i = i - 1
        # 箱体区间
        return REF(LOW, end_i), REF(OPEN, end_i), REF(CLOSE, begin_i), REF(HIGH, begin_i)
    else:
        for i in range(1, M1):
            if REF(CLOSE,i) < REF(OPEN,i):
                break
        begin_i = i
        for i in range(begin_i, M1):
            if not REF(CLOSE,i) < REF(OPEN,i):
                break
        end_i = i - 1
        # 箱体区间
        return REF(HIGH, end_i), REF(OPEN, end_i), REF(CLOSE, begin_i), REF(LOW, begin_i)


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
    for i in range(start_i, stop_i):
        if REF(CLOSE,i) > REF(OPEN,i):
            begin_i = i
            for j in range(begin_i, stop_i):
                if not REF(CLOSE,j) > REF(OPEN,j):
                    break
            end_i = j - 1
            break
    # 不一定能够找到箱体
    if end_i >= begin_i:
        # 第一个箱体区间
        bottom1, top1 = MIN(REF(LOW, end_i), REF(LOW, begin_i)), MAX(REF(HIGH, end_i), REF(HIGH, begin_i))
        return bottom1, top1

 
def BOX_UP(M2=20):
    """
    BOX_UP 查找前面周期连续阴线，来确定向上突破箱体
    """
    start_i, stop_i = 1, M2
    begin_i, end_i = M2, 0
    for i in range(start_i, stop_i):
        if REF(CLOSE,i) < REF(OPEN,i):
            begin_i = i
            for j in range(begin_i, stop_i):
                if not REF(CLOSE,j) < REF(OPEN,j):
                    break
            end_i = j - 1
            break
    # 不一定能够找到箱体
    if end_i >= begin_i:
        # 第一个箱体区间
        top1, bottom1 = MAX(REF(HIGH, end_i), REF(HIGH, begin_i)), MIN(REF(LOW, end_i), REF(LOW, begin_i))
        return top1, bottom1

                
def BOX_BOX_DOWN(M2=20):
    """
    BOX_DOWN 查找前面周期连续阳线，来确定向下突破箱体
    """
    start_i, stop_i = 1, M2
    begin_i, end_i = M2, 0
    for i in range(start_i, stop_i):
        if REF(CLOSE,i) > REF(OPEN,i):
            begin_i = i
            for j in range(begin_i, stop_i):
                if not REF(CLOSE,j) > REF(OPEN,j):
                    break
            end_i = j - 1
            break
    # 不一定能够找到箱体
    if end_i >= begin_i:
        # 第一个箱体区间
        bottom1, top1 = MIN(REF(LOW, end_i), REF(LOW, begin_i)), MAX(REF(HIGH, end_i), REF(HIGH, begin_i))
        # 之后再找第二个
        start_i, stop_i = 1 + end_i, M2 + end_i
        begin_i, end_i = M2, 0
        for i in range(start_i, stop_i):
            if REF(CLOSE,i) > REF(OPEN,i):
                begin_i = i
                for j in range(begin_i, stop_i):
                    if not REF(CLOSE,j) > REF(OPEN,j):
                        break
                end_i = j - 1
                break
        if end_i >= begin_i:
            bottom2, top2 = MIN(REF(LOW, end_i), REF(LOW, begin_i)), MAX(REF(HIGH, end_i), REF(HIGH, begin_i))
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
    for i in range(start_i, stop_i):
        if REF(CLOSE,i) < REF(OPEN,i):
            begin_i = i
            for j in range(begin_i, stop_i):
                if not REF(CLOSE,j) < REF(OPEN,j):
                    break
            end_i = j - 1
            break
    # 不一定能够找到箱体
    if end_i >= begin_i:
        # 第一个箱体区间
        top1, bottom1 = MAX(REF(HIGH, end_i), REF(HIGH, begin_i)), MIN(REF(LOW, end_i), REF(LOW, begin_i))
        # 之后再找第二个
        start_i, stop_i = 1 + end_i, M2 + end_i
        begin_i, end_i = M2, 0
        for i in range(start_i, stop_i):
            if REF(CLOSE,i) < REF(OPEN,i):
                begin_i = i
                for j in range(begin_i, stop_i):
                    if not REF(CLOSE,j) < REF(OPEN,j):
                        break
                end_i = j - 1
                break
        if end_i >= begin_i:
            top2, bottom2 = MAX(REF(HIGH, end_i), REF(HIGH, begin_i)), MIN(REF(LOW, end_i), REF(LOW, begin_i))
            return top1, bottom1, top2, bottom2
        else:
            return top1, bottom1, None, None
    #
    return None, None, None, None