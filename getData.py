import yfinance as yf
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import sys

def getTrandLine(target, x, y, degree):
    fit = np.polyfit(target.loc[:, x].values, target.loc[:, y].values, degree)
    trendline = []
    for i in target[x]:
        k = degree
        temp = 0
        for j in fit:
            temp = temp + j*math.pow(i, k)
            k = k - 1
        trendline.append(temp)
    return trendline

def get_data(name):
    company = yf.Ticker(name)
    hist = company.history(period="max")

    # res라는 DataFrame 생성 (Close열, Dividends열 인덱스 기준으로 merge)
    res = pd.concat([hist['Close'], hist['Dividends']], axis=1)

    # 현재 인덱스(날짜)를 열로 바꾸면서 date로 열이름 변경
    res = res.rename_axis('Date').reset_index()

    # Id열 추가 (index+1)
    res.insert(0, 'Id', np.arange(len(res)) + 1)

    # DivAdd(누적 배당금) 열 추가
    divadd = []
    divadd.append(res.loc[0]['Dividends'])
    for i in range(1, len(res)):
        divadd.append(divadd[i-1] + res.loc[i]['Dividends'])
    res['DivAdd'] = divadd

    return res

def drawChart(res, date, x, y=""):
    timelimit = res['Date'] > '2000-01-01'
    plt.plot(res.loc[timelimit, date].values, res.loc[timelimit, x].values)
    if y!="":
        plt.plot(res.loc[timelimit, date].values, res.loc[timelimit, y].values)
    plt.show()

if __name__ == '__main__':
    res = get_data("AAPL")
    res['TrendLineWithClose'] = getTrandLine(res, 'Id', 'Close', 4)
    drawChart(res, 'Date', 'Close', 'TrendLineWithClose')
    #res['trendLineWidDivAdd'] = getTrandLine(res, 'Id', 'DivAdd', 4)
    #res['expectWithDivAddGrowth'] = getTrandLine(res, 'trendLineWidDivAdd', 'Close', 1)
    
    #res['Bubble'] = res.loc[:, 'Close'].values - res.loc[:, 'expectWithDivAddGrowth'].values
    #res['BubblePercent'] = res.loc[:, 'Close'].values / res.loc[:, 'expectWithDivAddGrowth'].values * 100 - 100
    