import os
import datetime as dt
from src.typeDefs.reportContext import IReportCxt
from typing import List
from docxtpl import DocxTemplate, InlineImage
from src.app.section_1_1.section_1_1_1 import fetchSection1_1_1Context
from src.app.section_1_1.section_1_1_2 import fetchSection1_1_2Context
from src.app.section_1_1.section_1_1_3 import fetchSection1_1_3Context
from src.app.section_1_1.section_1_1_4 import fetchSection1_1_4Context
from src.app.section_1_1.section_1_1_freq import fetchSection1_1_freq_Context
from src.app.section_1_1.section_1_1_volt import fetchSection1_1_voltContext
from src.app.section_1_1.section_1_1_hydro import fetchSection1_1_hydroContext
from src.app.section_1_1.section_1_1_wind_solar import fetchSection1_1_WindSolarContext
from src.app.section_1_3.section_1_3_a import fetchSection1_3_aContext
from src.app.section_1_4.section_1_4_1 import fetchSection1_4_1Context
from src.app.section_1_4.section_1_4_2 import fetchSection1_4_2Context
from src.app.section_1_3.section_1_3_b import fetchSection1_3_bContext
from src.app.section_1_5.section_1_5_1 import fetchSection1_5_1Context
from src.app.section_1_5.section_1_5_2 import fetchSection1_5_2Context
from src.app.section_1_5.section_1_5_3 import fetchSection1_5_3Context
from src.app.section_1_6.section_1_6_1 import fetchSection1_6_1Context
from src.app.section_1_7.section_1_7_1 import fetchSection1_7_1Context
from src.app.section_1_7.section_1_7_2 import fetchSection1_7_2Context
from src.app.section_1_7.section_1_7_3 import fetchSection1_7_3Context
from src.app.section_1_9.section_1_9 import fetchSection1_9Context
from src.app.section_1_10.section_1_10 import fetchSection1_10Context
from src.app.section_1_11.section_1_11_solar import fetchSection1_11_SolarContext
from src.app.section_1_11.section_1_11_wind_c import fetchSection1_11_wind_cContext
from src.app.section_1_11.section_1_11_GenCurve import fetchSection1_11_GenerationCurve
from src.app.section_1_11.section_1_11_solar_c import fetchSection1_11_solar_cContext
from src.app.section_1_11.section_1_11_solarPlf import fetchSection1_11_solarPLF
from src.app.section_1_11.section_1_11_windPlf import fetchSection1_11_windPLF
from src.app.section_1_11.section_1_11_wind import fetchSection1_11_Wind
from src.app.section_1_11.section_1_11_solarGen import fetchSection1_11_SolarGen
from src.app.section_1_11.section_1_11_loadCurve import fetchSection1_11_LoadCurve
from src.app.section_reservoir.section_reservoir import fetchReservoirContext
from src.app.section_reservoir.hydro_gen_reservoir_table import fetchReservoirMonthlyTableContext
from src.app.section_1_12.section_1_12 import fetchSection1_12Context
from src.app.section_1_13.section_1_13 import fetchSection1_13Context
from src.app.section_2_1.section_2_1 import fetchSection2_1
from src.app.section_2_3.section_2_3 import fetchSection2_3_MaxContext,fetchSection2_3_MinContext
from src.utils.addMonths import addMonths
from src.typeDefs.section_1_3.section_1_3_a import ISection_1_3_a
from src.typeDefs.section_1_3.section_1_3_b import ISection_1_3_b
# from docx2pdf import convert


class MonthlyReportGenerator:
    appDbConStr: str = ''
    outageDbConnStr :str = ''
    sectionCtrls = {
        '1_1_1': True,
        '1_1_2': True,
        '1_1_3': True,
        '1_1_4': True,
        '1_1_freq': True,
        '1_1_volt': True,
        '1_1_hydro': True,
        '1_1_wind_solar': True,
        '1_4_1': True,
        '1_4_2': True,
        '1_3_a': True,
        '1_3_b': True,
        '1_5_1': True,
        '1_5_2': True,
        '1_5_3': True,
        '1_6_1': True,
        '1_6_2': True,
        '1_7_1': True,
        '1_7_2': True,
        '1_7_3': True,
        '1_9': True,
        '1_10':True,
        '1_11_solar': True,
        '1_11_wind':True,
        '1_11_gen_curve':True,
        '1_11_wind_c': True,
        '1_11_solar_c': True,
        '1_11_solar_plf':True,
        '1_11_wind_plf':True,
        '1_11_solarGen':True,
        '1_11_loadCurve':True,
        'reservoir': True,
        'reservoir_table':True,
        '1_12': True,
        '1_13':False,
        '2_1':True,
        '2_2':True,
        '2_3_Max':True,
        '2_3_Min':True
    }

    def __init__(self, appDbConStr: str, outageDbConnStr:str ,secCtrls: dict = {}):
        self.appDbConStr = appDbConStr
        self.outageDbConnStr = outageDbConnStr
        self.sectionCtrls.update(secCtrls)

    def getReportContextObj(self, monthDt: dt.datetime) -> IReportCxt:
        """get the report context object for populating the weekly report template
        Args:
            monthDt (dt.datetime): month date object
        Returns:
            IReportCxt: report context object
        """
        # create context for weekly report
        reportContext: IReportCxt = {}

        startDt = dt.datetime(monthDt.year, monthDt.month, 1)
        endDt = addMonths(startDt, 1) - dt.timedelta(days=1)
        if self.sectionCtrls["1_1_1"]:
            # get section 1.1.1 data
            try:
                secData_1_1_1 = fetchSection1_1_1Context(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secData_1_1_1)
                print(
                    "section 1_1_1 context setting complete")
            except Exception as err:
                print(
                    "error while fetching section 1_1_1")
                print(err)

        if self.sectionCtrls["1_1_2"]:
            # get section 1.1.2 data
            try:
                secData_1_1_2 = fetchSection1_1_2Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_2)
                print(
                    "section 1_1_2 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_2"
                )
                print(err)

        if self.sectionCtrls["1_1_3"]:
            # get section 1.1.2 data
            try:
                secData_1_1_3 = fetchSection1_1_3Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_3)
                print(
                    "section 1_1_3 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_3")

        if self.sectionCtrls["1_1_4"]:
            # get section 1.1.2 data
            try:
                secData_1_1_4 = fetchSection1_1_4Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_4)
                print(
                    "section 1_1_4 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_4"
                )
                print(err)

        # get section 1.1 volt data
        if self.sectionCtrls["1_1_volt"]:
            try:
                secData_1_1_volt = fetchSection1_1_voltContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_volt)
                print(
                    "section 1_1_volt context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_volt"
                )
                print(err)

        if self.sectionCtrls["1_1_freq"]:
            # get section 1.1.freq data
            try:
                secData_1_1_freq = fetchSection1_1_freq_Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_freq)
                print(
                    "section 1_1_freq context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_freq"
                )
                print(err)

        if self.sectionCtrls["1_1_hydro"]:
            # get section 1.1.hydro data
            try:
                secData_1_1_hydro = fetchSection1_1_hydroContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_hydro)
                print(
                    "section 1_1_hydro context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_hydro"
                )
                print(err)

        if self.sectionCtrls["1_1_wind_solar"]:
            # get section 1.1.wind_solar data
            try:
                secData_1_1_wind_solar = fetchSection1_1_WindSolarContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_wind_solar)
                print(
                    "section 1_1_wind_solar context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_wind_solar"
                )
                print(err)

        # get section 1.3.a data
        if self.sectionCtrls["1_3_a"]:
            try:
                secData_1_3_a: ISection_1_3_a = fetchSection1_3_aContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_3_a)
                print(
                    "section 1_3_a context setting complete"
                )
            except Exception as err:
                print("error while fetching section 1_3_a")
                print(err)

        # get section 1.3.b data
        if self.sectionCtrls['1_3_b']:
            try:
                secData_1_3_b: List[ISection_1_3_b] = fetchSection1_3_bContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_3_b)
                print('section_1_3_b context setting complete')
            except Exception as err:
                print("error while fetching section 1_3_b")
                print(err)

        if self.sectionCtrls["1_4_1"]:
            # get section 1.4.1 data
            try:
                secData_1_4_1 = fetchSection1_4_1Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_4_1)
                print(
                    "section 1_4_1 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_4_1"
                )
                print(err)

        if self.sectionCtrls["1_4_2"]:
            # get section 1.4.2 data
            try:
                secData_1_4_2 = fetchSection1_4_2Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_4_2)
                print(
                    "section 1_4_2 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_4_2"
                )
                print(err)

        if self.sectionCtrls["1_5_1"]:
            # get section 1.5.1 data
            try:
                secData_1_5_1 = fetchSection1_5_1Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_5_1)
                print(
                    "section 1_5_1 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_5_1"
                )
                print(err)

        if self.sectionCtrls["1_5_2"]:
            # get section 1.5.2 data
            try:
                secData_1_5_2 = fetchSection1_5_2Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_5_2)
                print(
                    "section 1_5_2 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_5_2"
                )
                print(err)

        if self.sectionCtrls["1_5_3"]:
            # get section 1.5.3 data
            try:
                secData_1_5_3 = fetchSection1_5_3Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_5_3)
                print(
                    "section 1_5_3 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_5_3"
                )
                print(err)

        if self.sectionCtrls["1_6_1"]:
            # get section 1.6.1 data
            try:
                secData_1_6_1 = fetchSection1_6_1Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_6_1)
                print(
                    "section 1_6_1 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_6_1"
                )
                print(err)

        if self.sectionCtrls["1_7_1"]:
            # get section 1.7.1 data
            try:
                secData_1_7_1 = fetchSection1_7_1Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_7_1)
                print(
                    "section 1_7_1 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_7_1"
                )
                print(err)

        if self.sectionCtrls["1_7_2"]:
            # get section 1.7.2 data
            try:
                secData_1_7_2 = fetchSection1_7_2Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_7_2)
                print(
                    "section 1_7_2 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_7_2"
                )
                print(err)

        if self.sectionCtrls["1_7_3"]:
            # get section 1.7.3 data
            try:
                secData_1_7_3 = fetchSection1_7_3Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_7_3)
                print(
                    "section 1_7_3 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_7_3"
                )
                print(err)

        if self.sectionCtrls["1_9"]:
            # get section 1.9 data
            try:
                secData_1_9 = fetchSection1_9Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_9)
                print(
                    "section 1_9 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_9"
                )
                print(err)
        if self.sectionCtrls["1_10"]:
            # get section 1.10 data
            

            try:
                secData_1_10 = fetchSection1_10Context(
                    self.outageDbConnStr, startDt, endDt
                )
                reportContext.update(secData_1_10)
                print(
                    "section 1_10 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_10"
                )
                print(err)
        if self.sectionCtrls["1_11_solar_plf"]:
            try:
                secData_1_11_solarplf = fetchSection1_11_solarPLF(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_solarplf)
                print(
                    "section 1_11_solar_plf context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_solar_plf"
                )
                print(err)

        if self.sectionCtrls["1_11_wind_plf"]:
            try:
                secData_1_11_windplf = fetchSection1_11_windPLF(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_windplf)
                print(
                    "section 1_11_wind_plf context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_wind_plf"
                )
                print(err)

        if self.sectionCtrls["1_11_solar"]:
            # get section 1.9 data
            try:
                secData_1_11_solar = fetchSection1_11_SolarContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_solar)
                print(
                    "section 1_11_solar context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_solar"
                )
                print(err)
    
        if self.sectionCtrls["1_11_wind"]:
            # get section 1.11.wind.a data
            try:
                secData_1_11_wind = fetchSection1_11_Wind(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_wind)
                print(
                    "section 1_11_wind context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_wind"
                )
                print(err)
        if self.sectionCtrls["1_11_gen_curve"]:
            
            try:
                secData_1_11_GenCurve = fetchSection1_11_GenerationCurve(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_GenCurve)
                print(
                    "section 1_11_GenCurve context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_GenCurve"
                )
                print(err)
        if self.sectionCtrls["1_11_wind_c"]:
            # get section 1.11.wind.c data
            try:
                secData_1_11_wind_c = fetchSection1_11_wind_cContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_wind_c)
                print(
                    "section 1_11_wind_c context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_wind_c"
                )
                print(err)

        if self.sectionCtrls["1_11_solar_c"]:
            # get section 1.11.wind.c data
            try:
                secData_1_11_solar_c = fetchSection1_11_solar_cContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_solar_c)
                print(
                    "section 1_11_solar_c context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_solar_c"
                )
                print(err)
        
        if self.sectionCtrls["1_11_solarGen"]:
            try:
                secData_1_11_solarGen = fetchSection1_11_SolarGen(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_solarGen)
                print(
                    "section 1_11_solar_gen context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_solar_gen"
                )
                print(err)
                
        if self.sectionCtrls["1_11_loadCurve"]:
            try:
                secData_1_11_loadCurve = fetchSection1_11_LoadCurve(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_11_loadCurve)
                print(
                    "section 1_11_loadCurve context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_11_loadCurve"
                )
                print(err)        
        if self.sectionCtrls["reservoir"]:
            # get section reservoir data
            try:
                secData_reservoir = fetchReservoirContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secData_reservoir)
                print(
                    "section reservoir context setting complete")
            except Exception as err:
                print(
                    "error while fetching section reservoir")
                print(err)
        # get reservoir section table data
        if self.sectionCtrls["reservoir_table"]:
            # get section reservoir data
            try:
                secData_reservoir = fetchReservoirMonthlyTableContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secData_reservoir)
                print(
                    "section hydro reservoir table context setting complete")
            except Exception as err:
                print(
                    "error while fetching section hydro reservoir table")
                print(err)
        # get section 1.12 inter regional data
        if self.sectionCtrls["1_12"]:
            try:
                secData_1_12 = fetchSection1_12Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_12)
                print(
                    "section 1_12 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_12"
                )
                print(err)
        if self.sectionCtrls["1_13"]:
            try:
                from src.config.appConfig import getJsonConfig
                appConfig = getJsonConfig()
                filePath = appConfig['rrasFilePath']
                secData_1_13 = fetchSection1_13Context(self.appDbConStr ,filePath, startDt, endDt
                )
                reportContext.update(secData_1_13)
                print(
                    "section 1_13 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_13"
                )
                print(err)
        if self.sectionCtrls["2_1"]:
            try:
                secData_2_1 = fetchSection2_1(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_2_1)
                print(
                    "section 2_1 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 2_1"
                )
                print(err)

        # get section 2_3_max data
        if self.sectionCtrls["2_3_Max"]:
            try:
                secData_2_3_Max = fetchSection2_3_MaxContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_2_3_Max)
                print(
                    "section 2_3_Max context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 2_3_Max"
                )
                print(err)
    
        # get section 2_3_min data
        if self.sectionCtrls["2_3_Min"]:
            try:
                secData_2_3_Min = fetchSection2_3_MinContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_2_3_Min)
                print(
                    "section 2_3_Min context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 2_3_Min"
                )
                print(err)

        return reportContext

    def generateReportWithContext(self, reportContext: IReportCxt, tmplPath: str, dumpFolder: str) -> bool:
        """generate the report file at the desired dump folder location
        based on the template file and report context object
        Args:
            reportContext (IReportCxt): report context object
            tmplPath (str): full file path of the template
            dumpFolder (str): folder path for dumping the generated report
        Returns:
            bool: True if process is success, else False
        """
        try:
            doc = DocxTemplate(tmplPath)
            # populate section 1.4.2 plot image in word file
            if self.sectionCtrls["1_4_2"]:
                plot_1_4_2_path = 'assets/section_1_4_2.png'
                plot_1_4_2_img = InlineImage(doc, plot_1_4_2_path)
                reportContext['plot_1_4_2'] = plot_1_4_2_img

            # populate section 1.5.1 plot image in word file
            if self.sectionCtrls["1_5_1"]:
                plot_1_5_1_path = 'assets/section_1_5_1.png'
                plot_1_5_1_img = InlineImage(doc, plot_1_5_1_path)
                reportContext['plot_1_5_1'] = plot_1_5_1_img

            # populate section 1.5.2 plot image in word file
            if self.sectionCtrls["1_5_2"]:
                plot_1_5_2_path = 'assets/section_1_5_2.png'
                plot_1_5_2_img = InlineImage(doc, plot_1_5_2_path)
                reportContext['plot_1_5_2'] = plot_1_5_2_img

            # populate section 1.5.3 plot image in word file
            if self.sectionCtrls["1_5_3"]:
                plot_1_5_3_path = 'assets/section_1_5_3.png'
                plot_1_5_3_img = InlineImage(doc, plot_1_5_3_path)
                reportContext['plot_1_5_3'] = plot_1_5_3_img

            # populate section 1.6.2 plot image in word file
            if self.sectionCtrls["1_6_2"]:
                plot_1_6_2_path = 'assets/section_1_6_2.png'
                plot_1_6_2_img = InlineImage(doc, plot_1_6_2_path)
                reportContext['plot_1_6_2'] = plot_1_6_2_img

            # populate section 1.7.3 plot images in word file
            if self.sectionCtrls["1_7_3"]:
                plot_1_7_3_base_path = 'assets/section_1_7_3'
                reportContext['plot_1_7_3'] = []
                for imgItr in range(reportContext['num_plts_sec_1_7_3']):
                    imgPath = '{0}_{1}.png'.format(
                        plot_1_7_3_base_path, imgItr)
                    img = InlineImage(doc, imgPath)
                    imgObj = {"img": img}
                    reportContext['plot_1_7_3'].append(imgObj)

            if self.sectionCtrls["1_10"]:
                plot_1_10_path = 'assets/section_1_10_generation_outage.png'
                plot_1_10_img = InlineImage(doc, plot_1_10_path)
                reportContext['plot_1_10'] = plot_1_10_img

            if self.sectionCtrls["1_11_solar"]:
                plot_1_11_solar_path = 'assets/section_1_11_solar.png'
                plot_1_11_solar_img = InlineImage(doc, plot_1_11_solar_path)
                reportContext['plot_1_11_solar'] = plot_1_11_solar_img
            
            if self.sectionCtrls["1_11_wind"]:
                plot_1_11_wind_base_path = 'assets/section_1_11_wind'
                reportContext['plot_1_11_wind'] = []
                for imgItr in range(1,3):
                    imgPath = '{0}_{1}.png'.format(plot_1_11_wind_base_path,imgItr)
                    img = InlineImage(doc,imgPath)
                    imgObj = {"img":img}
                    reportContext['plot_1_11_wind'].append(imgObj)
            
            if self.sectionCtrls["1_11_solarGen"]:
                plot_1_11_wind_base_path = 'assets/section_1_11_solar'
                reportContext['plot_1_11_solarGen'] = []
                for imgItr in range(1,3):
                    imgPath = '{0}_{1}.png'.format(plot_1_11_wind_base_path,imgItr)
                    img = InlineImage(doc,imgPath)
                    imgObj = {"img":img}
                    reportContext['plot_1_11_solarGen'].append(imgObj)

            if self.sectionCtrls['1_11_gen_curve']:
                plot_1_11_gen_curve_base_path = 'assets/section_1_11'
                reportContext['plot_1_11_gen_curve'] = []
                
                imgPath = '{0}_windGenCurve.png'.format(plot_1_11_gen_curve_base_path)
                img = InlineImage(doc,imgPath)
                imgObj = {"img":img}
                reportContext['plot_1_11_gen_curve'].append(imgObj)

                imgPath1 = '{0}_WindSolarGenCurve.png'.format(plot_1_11_gen_curve_base_path)
                img1 = InlineImage(doc,imgPath1)
                imgObj1 = {"img":img1}
                reportContext['plot_1_11_gen_curve'].append(imgObj1)

            if self.sectionCtrls['1_11_loadCurve']:
                plot_1_11_netloadCurve_path = 'assets/section_1_11_netLoadCurve.png'
                plot_1_11_netLoadCurve = InlineImage(doc, plot_1_11_netloadCurve_path)
                reportContext['plot_1_11_netloadCurve'] = plot_1_11_netLoadCurve

            # populate all reservoir section plot images in word file
            if self.sectionCtrls["reservoir"]:
                plot_reservoir_base_path = 'assets/reservoir_section'
                reportContext['reservoir_section'] = []
                for imgItr in range(reportContext['num_plts_sec_reservoir']):
                    imgPath = '{0}_{1}.png'.format(
                        plot_reservoir_base_path, imgItr)
                    img = InlineImage(doc, imgPath)
                    imgObj = {"img": img}
                    reportContext['reservoir_section'].append(imgObj)

            # populate all inter regioanl section plot images in word file
            if self.sectionCtrls["1_12"]:
                plot_inter_regional_base_path = 'assets/section_1_12'
                reportContext['inter_regioanl_section'] = []
                for imgItr in range(reportContext['num_plts_sec_inter_regional']):
                    imgPath = '{0}_{1}.png'.format(
                        plot_inter_regional_base_path, imgItr)
                    img = InlineImage(doc, imgPath)
                    imgObj = {"img": img}
                    reportContext['inter_regioanl_section'].append(imgObj)

            if self.sectionCtrls['2_1']:
                plot_2_1_basePath = 'assets/section_2_1'
                reportContext['plot_2_1'] = []
                
                imgPath = '{0}_{1}.png'.format(
                        plot_2_1_basePath, 'loadDurationCurve')
                img = InlineImage(doc, imgPath)
                imgObj = {"img": img}
                reportContext['plot_2_1'].append(imgObj)

            if self.sectionCtrls['2_2']:
                plot_2_2_basePath = 'assets/section_2_2'
                reportContext['plot_2_2'] = []

                imgPath = '{0}_{1}.png'.format(
                        plot_2_2_basePath, 'frequencyDurationCurve')
                img = InlineImage(doc, imgPath)
                imgObj = {"img": img}
                reportContext['plot_2_2'].append(imgObj)


            # populate all max hourly section plot images in word file
            if self.sectionCtrls["2_3_Max"]:
                plot_max_hourly_base_path = 'assets/section_2_3_1'
                reportContext['max_hourly_section'] = []
                for imgItr in range(reportContext['num_plts_sec_max_hourly']):
                    imgPath = '{0}_{1}.png'.format(
                        plot_max_hourly_base_path, imgItr)
                    img = InlineImage(doc, imgPath)
                    imgObj = {"img": img}
                    reportContext['max_hourly_section'].append(imgObj)

            # populate all min hourly section plot images in word file
            if self.sectionCtrls["2_3_Min"]:
                plot_min_hourly_base_path = 'assets/section_2_3_2'
                reportContext['min_hourly_section'] = []
                for imgItr in range(reportContext['num_plts_sec_min_hourly']):
                    imgPath = '{0}_{1}.png'.format(
                        plot_min_hourly_base_path, imgItr)
                    img = InlineImage(doc, imgPath)
                    imgObj = {"img": img}
                    reportContext['min_hourly_section'].append(imgObj)


            doc.render(reportContext)

            # derive document path and save
            dumpFileName = 'Monthly_Report_{0}.docx'.format(
                reportContext['full_month_name'])
            dumpFileFullPath = os.path.join(dumpFolder, dumpFileName)
            doc.save(dumpFileFullPath)
        except Exception as err:
            print("error while saving monthly report from context for month ")
            print(err)
            return False
        return True

    def generateMonthlyReport(self, monthDt: dt.datetime, tmplPath: str, dumpFolder: str) -> bool:
        """generates and dumps weekly report for given dates at a desired location based on a template file
        Args:
            monthDt (dt.datetime): month date
            tmplPath (str): full file path of the template file
            dumpFolder (str): folder path where the generated reports are to be dumped
        Returns:
            bool: True if process is success, else False
        """
        reportCtxt = self.getReportContextObj(monthDt)
        isSuccess = self.generateReportWithContext(
            reportCtxt, tmplPath, dumpFolder)
        # convert report to pdf
        # convert(dumpFileFullPath, dumpFileFullPath.replace('.docx', '.pdf'))
        return isSuccess
