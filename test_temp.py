import unittest
import os
from temp import manifest_csv_to_df

class TestTemp(unittest.TestCase):
    def test_names(self):
        #test csv files 
        print(manifest_csv_to_df('cam.csv'))
        print(manifest_csv_to_df('b3.csv'))
        
        
