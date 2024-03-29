import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
from src.config.appConfig import getREConstituentsMappings
import numpy as np
from src.typeDefs.section_1_11.section_1_11_PLFCUF import ISection_1_11_PLFCUF, IPLFCUFDataRow
import math

def fetchSection1_11_windPLF(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_11_PLFCUF:
    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)

    numOfDays = ( endDt - startDt ).days + 1

    soFarHighestAllEntityGenVals = mRepo.getSoFarHighestAllEntityData(
        'soFarHighestWindGen', addMonths(startDt, -1))
    soFarHighestGenLookUp = {}
    for v in soFarHighestAllEntityGenVals:
        soFarHighestGenLookUp[v['constituent']] = {
            'value': v['data_value'], 'ts': v['data_time']}

    dispRows: List[IPLFCUFDataRow] = []
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(math.isnan(constInfo['windCapacity'])):
            continue

        maxGenData = mRepo.getEntityMetricHourlyData(
            constInfo["entity_tag"], "Wind(MW)", startDt, endDt)
        
        if constInfo['entity_tag'] == 'central':
            windEnerConsumption = mRepo.getEntityMetricDailyData(
            'wr', 'CGS Wind(Mus)' ,startDt, endDt)
        elif constInfo['entity_tag'] == 'wr':
            windEnerConsumption = mRepo.getEntityMetricDailyData(
            'wr', "Wind(MU)" ,startDt, endDt)
            cgsWindEnerConsumption = mRepo.getEntityMetricDailyData(
            'wr', 'CGS Wind(Mus)' ,startDt, endDt)
            for w,c in zip(windEnerConsumption,cgsWindEnerConsumption):
                w["data_value"] += c["data_value"]
        else:
            windEnerConsumption = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'], 'Wind(MU)' ,startDt, endDt)
        
        energyConsumption = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'],'Consumption(MU)',startDt , endDt
        )

        maxGenDf = pd.DataFrame(maxGenData)
        maxGenDf = maxGenDf.pivot(
            index='time_stamp',columns='metric_name',values='data_value'
        )
        windEnerConsumptionSum = pd.DataFrame(windEnerConsumption).groupby('entity_tag').sum().iloc[0]['data_value']

        if(len(energyConsumption) == 0):
            # This is for central sector as we dont have consumption data
            # calculate mu from mw
            # df = pd.DataFrame(maxGenData)
            # average = df.groupby('entity_tag').mean()
            # windEnerConsumptionSumDf = average * 0.024 * numOfDays #To Calculate Avg MU from MW
            # windEnerConsumptionSum = windEnerConsumptionSumDf.iloc[0]['data_value']
            EnerConsumptionSum = 0
            penetrationLevel = 0
        else:
            EnerConsumptionSum = pd.DataFrame(energyConsumption).groupby('entity_tag').sum().iloc[0]['data_value']
            penetrationLevel = round((windEnerConsumptionSum/EnerConsumptionSum) * 100 ,2)


        maxWind = maxGenDf["Wind(MW)"].max()
        maxWindDt = maxGenDf["Wind(MW)"].idxmax()


        plf = ( windEnerConsumptionSum * 1000 ) / (int(constInfo['windCapacity'])*24*numOfDays )
        cuf = maxWind * 100 / (int(constInfo['windCapacity']))

        prevHighestWindObj = soFarHighestGenLookUp[constInfo["entity_tag"]]
        newHighestWind = maxWind
        newHighestWindTime = maxWindDt.to_pydatetime()

        if newHighestWind < prevHighestWindObj["value"]:
            newHighestWind = prevHighestWindObj["value"]
            newHighestWindTime = prevHighestWindObj["ts"]

               
        mRepo.insertSoFarHighest(
            constInfo['entity_tag'], "soFarHighestWindGen", startDt, newHighestWind, newHighestWindTime)
        # soFarHighestAllEntityGenVals = mRepo.getSoFarHighestAllEntityData(
        # 'soFarHighestWindGen', startDt)
        # soFarHighestGenLookUp = {}
        # for v in soFarHighestAllEntityGenVals:
        #     soFarHighestGenLookUp[v['constituent']] = {
        #     'value': v['data_value'], 'ts': v['data_time']}
        so_far_high_gen_str = str(round(newHighestWind)) + ' on ' + dt.datetime.strftime(newHighestWindTime,'%d-%b-%Y') + ' at ' + dt.datetime.strftime(newHighestWindTime,'%H:%S')
                              
        const_display_row: IPLFCUFDataRow = {
            'entity': constInfo['display_name'],
            'capacityMW': round(constInfo['windCapacity']),
            'maxgenerationMW': round(maxWind),
            'soFarHighestGenMW': so_far_high_gen_str,
            'energyGeneration': round(windEnerConsumptionSum),
            'energyConsumption': round(EnerConsumptionSum),
            'penetration': penetrationLevel,
            'plf': round(plf*100),
            'cuf': round(cuf)                                                           
        }
        dispRows.append(const_display_row)

    secData: ISection_1_11_PLFCUF = {"so_far_hig_win_gen_plf": dispRows}
    return secData
