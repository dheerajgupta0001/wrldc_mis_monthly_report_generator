import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
from src.utils.convertDtToDayNum import convertDtToDayNum
from src.utils.getPrevFinYrDt import getPrevFinYrDt,getFinYrDt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def fetchSection1_11_SolarContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:
    # get WR Solar Generation from recent Fin year start till this month
    # and WR Solar Generation from 2 years back fin year to last fin year
    # example: For Jan 21, we require data from 1-Apr-2019 to 31-Mar-2020 and 1-Apr-2020 to 31 Jan 21

    finYrStart = getFinYrDt(startDt)
    prevFinYrStart = getPrevFinYrDt(finYrStart)

    finYrName = '{0}-{1}'.format(finYrStart.year, (finYrStart.year+1) % 100)
    prevFinYrName = '{0}-{1}'.format(finYrStart.year-1, finYrStart.year % 100)
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR Solar Generation values for this financial year
    wrSolVals = mRepo.getEntityMetricDailyData(
        'wr', 'Solar(MU)', finYrStart, endDt)
    wrPrevFinYrSolVals = mRepo.getEntityMetricDailyData(
        'wr', 'Solar(MU)', prevFinYrStart, finYrStart-dt.timedelta(days=1))

    # create plot image for generation of prev fin year and this fin year
    pltGenerationObjs = [{'MONTH': x["time_stamp"], 'colName': finYrName,
                   'val': x["data_value"]} for x in wrSolVals]
    pltGenerationObjsLastYear = [{'MONTH': x["time_stamp"],
                           'colName': prevFinYrName, 'val': x["data_value"]} for x in wrPrevFinYrSolVals]

    pltDataObjs = pltGenerationObjs + pltGenerationObjsLastYear

    pltDataDf = pd.DataFrame(pltDataObjs)
    pltDataDf = pltDataDf.pivot(
        index='MONTH', columns='colName', values='val')
    maxTs = pltDataDf.index.max()
    for rIter in range(pltDataDf.shape[0]):
        # check if Prev fin Yr data column is not Nan, if yes set this year data column
        lastYrDt = pltDataDf.index[rIter].to_pydatetime()
        if not pd.isna(pltDataDf[prevFinYrName].iloc[rIter]):
            thisYrTs = pd.Timestamp(addMonths(lastYrDt, 12))
            if thisYrTs <= maxTs:
                thisYrVal = pltDataDf[finYrName].loc[thisYrTs]
                pltDataDf.at[pd.Timestamp(lastYrDt), finYrName] = thisYrVal
    pltDataDf = pltDataDf[~pltDataDf[prevFinYrName].isna()]

    # save plot data as excel
    pltDataDf.to_excel("assets/plot_1_11_solar.xlsx", index=True)

    # derive plot title
    pltTitle = 'Western Region Solar Generation {0} to {1}'.format(
        prevFinYrName, finYrName)

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # set plot title
    ax.set_title(pltTitle)
    # set x and y labels
    ax.set_xlabel('MONTH')
    ax.set_ylabel('MUs')

    plt.xticks(rotation=90)
    # set x axis formatter as month name and 10 days interval
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b') )
    
    ax.set_xlim(xmin=prevFinYrStart , xmax= finYrStart-dt.timedelta(days=1))
    
    # plot data and get the line artist object in return
    laThisYr, = ax.plot(pltDataDf.index.values,
                        pltDataDf[finYrName].values, color='#ff0000' )
    laThisYr.set_label(finYrName)

    laLastYear, = ax.plot(pltDataDf.index.values,
                          pltDataDf[prevFinYrName].values, color='#0000ff')
    laLastYear.set_label(prevFinYrName)

    # enable axis grid lines
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 0.4, 0.0), loc='lower center',
              ncol=2, borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.savefig('assets/section_1_11_solar.png')

    secData: dict = {}
    return secData
