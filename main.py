#!/usr/bin/env python

import numpy as np

nInst=50
currentPos = np.zeros(nInst)
def getMyPosition (prcSoFar):
    if prcSoFar.shape[1] < 2:
        return currentPos
    # check should buy and sell
    buy = shouldBuyV4(prcSoFar)
    sell = shouldSellV4(prcSoFar)

    # update current position
    currentPos[buy] += 1000
    currentPos[sell] -= 1000

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

def shouldBuyV4(prcSoFar):
    # same as buyv3 but buy only when the decrease is slowing down and reaching a minimum
    if prcSoFar.shape[1] < 5:
        # return all instruments false
        return np.array([False]*nInst)
    # get the last day of prices
    lastDay = prcSoFar[:,-1]
    # get the last 5 days of prices
    last5Days = prcSoFar[:,-5:]
    # get the mean of the last 5 days
    last5DaysMean = np.mean(last5Days, axis=1)

    # check if it is slowing down decline
    slowingDown = np.logical_and(lastDay < last5DaysMean, lastDay > last5Days[:,-1])
    # check if it is reaching a minimum
    reachingMin = np.logical_and(lastDay < last5DaysMean, lastDay < last5Days[:,-1])
    # check if it is increasing
    increasing = lastDay > last5DaysMean

    # buy if it is slowing down decline or reaching a minimum
    return np.logical_or(slowingDown, reachingMin)

def shouldSellV4(prcSoFar):
    # same as sellv3 but sell only when the increase is slowing down and reaching a maximum
    if prcSoFar.shape[1] < 5:
        # return all instruments false
        return np.array([False]*nInst)
    # get the last day of prices
    lastDay = prcSoFar[:,-1]
    # get the last 5 days of prices
    last5Days = prcSoFar[:,-5:]
    # get the mean of the last 5 days
    last5DaysMean = np.mean(last5Days, axis=1)

    # check if it is slowing down increase
    slowingDown = np.logical_and(lastDay > last5DaysMean, lastDay < last5Days[:,-1])
    # check if it is reaching a maximum
    reachingMax = np.logical_and(lastDay > last5DaysMean, lastDay > last5Days[:,-1])
    # check if it is decreasing
    decreasing = lastDay < last5DaysMean

    # sell if it is slowing down increase or reaching a maximum
    return np.logical_or(slowingDown, reachingMax)