import pandas as pd
import unittest
from temp import find_prices

class TestTemp(unittest.TestCase):
    def test_names(self):
        #test csv files 
        print(find_prices(pd.DataFrame({'name':['iphone 8','iphone 7'],'qty':[4,3]})))
        print(find_prices(pd.DataFrame({'name':['Ematic Low Profile Mount 23-65" - Black (EMW5105 )','heyday  Apple iPhone 8/7/6s/6 Print Case - Blurred Floral'],'qty':[1,3]})))