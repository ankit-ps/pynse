import sys
import requests
import traceback
sys.path.append("../pynse")

from pynse import Pynse

p = Pynse()
try:
    #p.get_scrip_quote("HDFCBANK")
    #p.get_scrip_pe("HDFCBANK")
    #p.get_scrip_and_sector_pe("HDFCBANK")
    #p.get_unique_index_list()
    #p.get_top_10_gainers()
    p.get_top_10_losers()
#except requests.ConnectionError as err_c:
    #print "could not connect to internet"
except Exception as e:
    print traceback.print_exc()
