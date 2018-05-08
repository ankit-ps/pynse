import requests
import json

class Pynse:
    def __init__():
        self.base_url               = "https://www.nseindia.com/live_market/"\
                                      "dynaContent/"
        self.stock_url              = "live_watch/stock_watch/"
        self.activity_analysis_url  = "live_analysis/most_active/"
        self.gainers_analysis_url   = "live_analysis/gainers/"
        self.losers_analysis_url   = "live_analysis/losers/"
        self.nifty_url              = self.base_url + self.stock_url + \
                                      "niftyStockWatch.json"
        self.nifty_next_50_url      = self.base_url + self.stock_url + \
                                      "juniorNiftyStockWatch.json"
        self.nse_commodities_url    = self.base_url + self.stock_url + \
                                      "cnxCommoditiesStockWatch.json"
        self.nse_midcap_url         = self.base_url + self.stock_url + \
                                      "niftyMidcap50StockWatch.json"
        self.nifty_500_url          = self.base_url + self.stock_url + \
                                      "nifty500StockWatch.json"
        self.nse_top_volume_url     = self.base_url + self.analysis_url + \
                                      "allTopVolume1.json"
        self.nse_top_turnover_url   = self.base_url + self.analysis_url + \
                                      "allTopValue1.json"
        self.nifty_top_gainers_url  = self.base_url + \
                                      self.gainers_analysis_url + \
                                      "niftyGainers1.json"
        self.all_top_gainers_url    = self.base_url + \
                                      self.gainers_analysis_url + \
                                      "allTopGainers1.json"
        self.nifty_top_losers_url   = self.base_url + \
                                      self.losers_analysis_url + \
                                      "niftyLosers1.json"
        self.all_top_losers_url     = self.base_url + \
                                      self.losers_analysis_url + \
                                      "allTopLosers1.json"
        self.all_pe_url             = "https://nseindia.com/homepage" \
                                      "/peDetails.json"
                                      
        #OKAY: Found a way to use nse jsons to get a quote,
        #Find which sector does a stock belong to and then
        #download that sectors json and find data for the stock 
        #in question. Can be done by downloading first the P/E json and 
        #then load it in memory. Then whenever a stock is requested, 
        #use the P/E json to figure out the index. Download index json and 
        #we are done

        #We will yahoo finance url in a different class to provide much finer
        #data
        self.yahoo_finance_base_url = "https://query1.finance.yahoo.com"\
                                      "/v8/finance/chart/"
        self.yahoo_finance_dict = {
                                    "region": "IN",
                                    "lang": "en-IN",
                                    "range": "1d",
                                    "includePrePost": "false",
                                    "interval": "2m",
                                    "corsDomain": "in.finance.yahoo.com",
                                    ".tsrc" : "finance"
                                    }
