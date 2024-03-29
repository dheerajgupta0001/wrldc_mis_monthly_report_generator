from src.typeDefs.section_1_4.section_1_4_2 import ISection_1_4_2
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
from src.utils.convertDtToDayNum import convertDtToDayNum
import matplotlib.pyplot as plt
import math


def fetchSection1_4_2Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_4_2:
    monthName = dt.datetime.strftime(startDt, "%b %y")
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR demand hourly values for this month and prev yr month
    wrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', startDt, endDt)
    demVals = [x['data_value'] for x in wrDemVals]
    wr_max_dem = max(demVals)
    wrMaxDemDt = wrDemVals[demVals.index(wr_max_dem)]['time_stamp']
    wr_max_dem_date_str = dt.datetime.strftime(wrMaxDemDt, "%d-%b-%y")
    wr_avg_dem = sum(demVals)/len(demVals)
    wrMaxDemTimestampStr = dt.datetime.strftime(
        wrMaxDemDt, "%d-%b-%y %H:%M")+" hrs"

    lastYrStartDt = addMonths(startDt, -12)
    lastYrEndDt = addMonths(endDt, -12)
    monthNameLastYear = dt.datetime.strftime(lastYrStartDt, "%b %y")
    wrLastYrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', lastYrStartDt, lastYrEndDt)
    demVals = [x['data_value'] for x in wrLastYrDemVals]
    wr_max_dem_last_year = max(demVals)
    wr_max_dem_date_str_last_year = dt.datetime.strftime(
        wrLastYrDemVals[demVals.index(wr_max_dem_last_year)]['time_stamp'], "%d-%b-%y")
    wr_avg_dem_last_year = sum(demVals)/len(demVals)

    wr_avg_dem_perc_change_last_year = round(
        100*(wr_avg_dem-wr_avg_dem_last_year)/wr_avg_dem_last_year, 2)
    wr_max_dem_perc_change_last_year = round(
        100*(wr_max_dem-wr_max_dem_last_year)/wr_max_dem_last_year, 2)

    prevMonthStartDt = addMonths(startDt, -1)
    prevMonthEndDt = addMonths(endDt, -1)
    prev_month_name = dt.datetime.strftime(prevMonthStartDt, "%b %y")
    wrPrevMonthDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', prevMonthStartDt, prevMonthEndDt)
    demVals = [x['data_value'] for x in wrPrevMonthDemVals]
    wr_max_dem_prev_month = max(demVals)
    wr_max_dem_date_str_prev_month = dt.datetime.strftime(
        wrPrevMonthDemVals[demVals.index(wr_max_dem_prev_month)]['time_stamp'], "%d-%b-%y")
    wr_avg_dem_prev_month = sum(demVals)/len(demVals)

    wr_avg_dem_perc_change_prev_month = round(
        100*(wr_avg_dem-wr_avg_dem_prev_month)/wr_avg_dem_prev_month, 2)
    wr_max_dem_perc_change_prev_month = round(
        100*(wr_max_dem-wr_max_dem_prev_month)/wr_max_dem_prev_month, 2)

    # create plot image for demands of prev yr, prev month, this month
    pltDemObjs = [{'Date': convertDtToDayNum(
        x["time_stamp"]), 'colName': monthName, 'val': x["data_value"]} for x in wrDemVals]
    pltDemObjsLastYear = [{'Date': convertDtToDayNum(
        x["time_stamp"]), 'colName': monthNameLastYear, 'val': x["data_value"]} for x in wrLastYrDemVals]
    pltDemObjsPrevMonth = [{'Date': convertDtToDayNum(
        x["time_stamp"]), 'colName': prev_month_name, 'val': x["data_value"]} for x in wrPrevMonthDemVals]
    pltDataObjs = pltDemObjs + pltDemObjsLastYear + pltDemObjsPrevMonth

    pltDataDf = pd.DataFrame(pltDataObjs)
    pltDataDf = pltDataDf.pivot(
        index='Date', columns='colName', values='val')
    pltDataDf.reset_index(inplace=True)
    pltDataDf["Date"] = [math.floor(x) for x in pltDataDf["Date"]]
    pltDataDf = pltDataDf.groupby(by="Date").max()
    # save plot data as excel
    pltDataDf.to_excel("assets/plot_1_4_2.xlsx", index=True)

    # derive plot title
    pltTitle = 'Demand met {0}, {1} & {2} \n Max. {3} MW on dt. {4} \n Average Load Growth {5}{6} against last year'.format(
        monthName, prev_month_name, monthNameLastYear, format(round(wr_max_dem), ","), wrMaxDemTimestampStr, wr_avg_dem_perc_change_last_year, "%")

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # set plot title
    ax.set_title(pltTitle)
    # set x and y labels
    ax.set_xlabel('Date')
    ax.set_ylabel('MW')
    ax.set_facecolor("#c6d9f1")
    fig.patch.set_facecolor('#fac090')
    # plot data and get the line artist object in return
    laThisMonth, = ax.plot(
        pltDataDf.index.values, pltDataDf[monthName].values, color='#ff0000')
    laThisMonth.set_label(monthName)

    laLastYear, = ax.plot(
        pltDataDf.index.values, pltDataDf[monthNameLastYear].values, color='#00ff00')
    laLastYear.set_label(monthNameLastYear)

    laPrevMonth, = ax.plot(
        pltDataDf.index.values, pltDataDf[prev_month_name].values, color='#A52A2A')
    laPrevMonth.set_label(prev_month_name)
    
    ax.set_xlim((1, 31), auto=True)
    # enable y axis grid lines
    ax.yaxis.grid(True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
              ncol=3, mode="expand", borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.savefig('assets/section_1_4_2.png')

    secData: ISection_1_4_2 = {
        'prev_month_name': prev_month_name,
        'wr_max_dem': round(wr_max_dem),
        'wr_max_dem_date_str': wr_max_dem_date_str,
        'wr_avg_dem': round(wr_avg_dem),
        'wr_max_dem_last_year': round(wr_max_dem_last_year),
        'wr_max_dem_date_str_last_year': wr_max_dem_date_str_last_year,
        'wr_avg_dem_last_year': round(wr_avg_dem_last_year),
        'wr_avg_dem_perc_change_last_year': wr_avg_dem_perc_change_last_year,
        'wr_max_dem_perc_change_last_year': wr_max_dem_perc_change_last_year,
        'wr_max_dem_prev_month': round(wr_max_dem_prev_month),
        'wr_max_dem_date_str_prev_month': wr_max_dem_date_str_prev_month,
        'wr_avg_dem_prev_month': round(wr_avg_dem_prev_month),
        'wr_avg_dem_perc_change_prev_month': wr_avg_dem_perc_change_prev_month,
        'wr_max_dem_perc_change_prev_month': wr_max_dem_perc_change_prev_month
    }
    return secData
