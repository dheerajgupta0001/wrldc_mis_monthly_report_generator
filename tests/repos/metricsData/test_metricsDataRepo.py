import unittest
from src.config.appConfig import loadJsonConfig
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import datetime as dt


class TestMetricsDataRepo(unittest.TestCase):
    def setUp(self):
        self.jsonConf = loadJsonConfig()

    def test_getEntityMetricHourlyData(self) -> None:
        """tests the function that gets hourly data of entity metric
        """
        appDbConnStr = self.jsonConf['appDbConnStr']
        mRepo = MetricsDataRepo(appDbConnStr)
        startDt = dt.datetime(2020, 1, 1)
        endDt = dt.datetime(2020, 1, 10)
        samples = mRepo.getEntityMetricHourlyData(
            "wr", "Demand(MW)", startDt, endDt)
        self.assertFalse(len(samples) == 0)