import unittest
import sys

WORK_FOLDER='../'
sys.path.append(WORK_FOLDER)

from utils.helper import loadCovidData, loadCovidDataSpain, getMadridTotalData, plotPlaces

class TotalMadridTest(unittest.TestCase):

    def test_total_Madrid(self):
        df = loadCovidData(prefix=WORK_FOLDER)
        df_spain = loadCovidDataSpain()
        df_all_madrid = getMadridTotalData(df, df_spain)
        plotPlaces(df_all_madrid, df_all_madrid['municipio_distrito'].unique(), plot=False)
        #self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()