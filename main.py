#!/usr/bin/env python

import numpy as np

nInst=50
currentPos = np.zeros(nInst)
def getMyPosition (prcSoFar):
    if prcSoFar.shape[1] < 2:
        return currentPos
    # check should buy and sell
    buy = shouldBuyV3(prcSoFar)
    sell = shouldSellV3(prcSoFar)

    # update current position
    currentPos[buy] = 10000
    currentPos[sell] = -10000


    # make all of currentPos 0 except don't change 24th instrument
    # list of all instruments to trade
    TRADE = [2, 11, 12, 24]
    currentPos[0:2] = 0
    currentPos[3:11] = -1000
    currentPos[13:24] = -100000
    currentPos[25:] = -7000

    return currentPos


def shouldBuy(prcSoFar):
    # check if more than one day of info
    if prcSoFar.shape[1] < 2:
        # return all instruments false
        return np.array([False]*nInst)
    # get the last day of prices
    lastDay = prcSoFar[:,-1]
    
    # buy if the price is lower than the day before
    return lastDay < prcSoFar[:,-2]

def shouldSell(prcSoFar):
    # check if more than one day of info
    if prcSoFar.shape[1] < 2:
        # return all instruments false
        return np.array([False]*nInst)
    # get the last day of prices
    lastDay = prcSoFar[:,-1]
    
    # sell if the price is higher than the day before
    return lastDay > prcSoFar[:,-2]

def shouldBuyV2(prcSoFar):
    # check if there is an upwards trend in the past 5 days if 5 days of data
    if prcSoFar.shape[1] < 5:
        # return all instruments false
        return np.array([False]*nInst)
    # get the last day of prices
    lastDay = prcSoFar[:,-1]
    # get the last 5 days of prices
    last5Days = prcSoFar[:,-5:]
    # get the mean of the last 5 days
    last5DaysMean = np.mean(last5Days, axis=1)

    # buy if the price is lower than the mean of the last 5 days
    return lastDay < last5DaysMean

def shouldSellV2(prcSoFar):
    # check if there is an downwards trend in the past 5 days if 5 days of data
    if prcSoFar.shape[1] < 5:
        # return all instruments false
        return np.array([False]*nInst)
    # get the last day of prices
    lastDay = prcSoFar[:,-1]
    # get the last 5 days of prices
    last5Days = prcSoFar[:,-5:]
    # get the mean of the last 5 days
    last5DaysMean = np.mean(last5Days, axis=1)

    # sell if the price is higher than the mean of the last 5 days
    return lastDay > last5DaysMean

def shouldBuyV3(prcSoFar):
    # same as shouldBuyV2 but only if there's an increasing rate of decrease
    if prcSoFar.shape[1] < 5:
        # return all instruments false
        return np.array([False]*nInst)
    # get the last day of prices
    lastDay = prcSoFar[:,-1]
    # get the last 5 days of prices
    last5Days = prcSoFar[:,-5:]
    # get the mean of the last 5 days
    last5DaysMean = np.mean(last5Days, axis=1)
    
    # get the difference between the last day and the mean of the last 5 days
    diff = lastDay - last5DaysMean
    # get the difference between the last 5 days and the mean of the last 5 days
    diff5Days = last5Days - last5DaysMean[:,None]
    # get the mean of the difference between the last 5 days and the mean of the last 5 days
    diff5DaysMean = np.mean(diff5Days, axis=1)

    # buy if the price is lower than the mean of the last 5 days and the difference between the last day and the mean of the last 5 days is increasing
    return np.logical_and(lastDay < last5DaysMean, diff > diff5DaysMean)

def shouldSellV3(prcSoFar):
    # same as shouldSellV2 but only if there's an increasing rate of increase
    if prcSoFar.shape[1] < 5:
        # return all instruments false
        return np.array([False]*nInst)
    # get the last day of prices
    lastDay = prcSoFar[:,-1]
    # get the last 5 days of prices
    last5Days = prcSoFar[:,-5:]
    # get the mean of the last 5 days
    last5DaysMean = np.mean(last5Days, axis=1)
    
    # get the difference between the last day and the mean of the last 5 days
    diff = lastDay - last5DaysMean
    # get the difference between the last 5 days and the mean of the last 5 days
    diff5Days = last5Days - last5DaysMean[:,None]
    # get the mean of the difference between the last 5 days and the mean of the last 5 days
    diff5DaysMean = np.mean(diff5Days, axis=1)

    # sell if the price is higher than the mean of the last 5 days and the difference between the last day and the mean of the last 5 days is increasing
    return np.logical_and(lastDay > last5DaysMean, diff < diff5DaysMean)
