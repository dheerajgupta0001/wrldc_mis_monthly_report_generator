from typing import TypedDict
import datetime as dt


class IMetricsDataRecord(TypedDict):
    time_stamp: dt.datetime
    entity_tag: str
    metric_name: str
    data_value: float

class IFreqMetricsDataRecord(TypedDict):
    time_stamp: dt.datetime
    metric_name: str
    data_value: float

class IReservoirDataRecord(TypedDict):
    time_stamp: dt.datetime
    entity_tag: str
    metric_tag: str
    data_value: float

class IGenerationLinesDataRecord(TypedDict):
    time_stamp: dt.datetime
    entity_tag: str
    generator_tag: str
    data_value: float 

class IOutageDataRecord(TypedDict):
    capacity:int
    time_stamp:int