import json
import pandas as pd
from typing import List, Any
from src.typeDefs.config.appConfig import IConstituentConfig

constituentsMappings: List[IConstituentConfig] = []
constituentsMappingsRE: List[Any] = []
jsonConfig: dict = {}


def initConfigs():
    loadJsonConfig()
    loadConstituentsMappings()
    loadREConstituentsMappings()
    loadReservoirsMappings()


def loadJsonConfig(fName="config.json") -> dict:
    global jsonConfig
    with open(fName) as f:
        data = json.load(f)
        jsonConfig = data
        return jsonConfig


def loadConstituentsMappings(filePath='config.xlsx', sheetname='constituents'):
    global constituentsMappings
    constituentsMappingsDf = pd.read_excel(filePath, sheet_name=sheetname)
    # Convert Nan to None
    # fileMappings = fileMappingsDf.where(pd.notnull(fileMappings),None)
    constituentsMappings = constituentsMappingsDf.to_dict('records')
    return constituentsMappings

def loadREConstituentsMappings(filePath='config.xlsx', sheetname='REconstituents'):
    global constituentsMappingsRE
    constituentsMappingsREDf = pd.read_excel(filePath, sheet_name=sheetname)
    constituentsMappingsRE = constituentsMappingsREDf.to_dict('records')
    return constituentsMappingsRE

def loadMetricsInfo(filePath='config.xlsx', sheetname='volt_metrics'):
    global voltMetrics
    voltMetrics = pd.read_excel(filePath, sheet_name=sheetname)
    voltMetrics = voltMetrics.to_dict('records')
    return voltMetrics

def loadREConstituentsMappings(filePath='config.xlsx', sheetname='REconstituents'):
    global constituentsMappingsRE
    constituentsMappingsREDf = pd.read_excel(filePath, sheet_name=sheetname)
    constituentsMappingsRE = constituentsMappingsREDf.to_dict('records')
    return constituentsMappingsRE


def loadReservoirsMappings(filePath='config.xlsx', sheetname='reservoir'):
    global reservoirsMappings
    reservoirsMappingsDf = pd.read_excel(filePath, sheet_name=sheetname)
    # Convert Nan to None
    reservoirsMappings = reservoirsMappingsDf.to_dict('records')
    return reservoirsMappings


def getJsonConfig() -> dict:
    global jsonConfig
    return jsonConfig


def getConstituentsMappings():
    global constituentsMappings
    return constituentsMappings


def getREConstituentsMappings():
    global constituentsMappingsRE
    return constituentsMappingsRE


def getReservoirsMappings():
    global reservoirsMappings
    return reservoirsMappings 
