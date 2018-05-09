import requests as r
import json
import pprint

#TODO: Document that the request exception will be raised as requests.excpetion

class Pynse:
    #util function
    def get_unique_index_list(self):
        pe = r.get(self.all_pe_url, timeout=3)
        s  = set()
        for scrip in pe.json():
            s.add(pe.json()[scrip]["sector"].strip(" "))    
        #print s
        for item in s:
            #print item
            pass
    #end _get_unique_index_list
    
    def __init__(self):
        self.base_url               = "https://www.nseindia.com/live_market/"\
                                      "dynaContent/"
        self.stock_url              = "live_watch/stock_watch/"
        self.activity_analysis_url  = "live_analysis/most_active/"
        self.gainers_analysis_url   = "live_analysis/gainers/"
        self.losers_analysis_url    = "live_analysis/losers/"
        self.index_url_dict         = {}
        self.nifty_url              = self.base_url + self.stock_url + \
                                      "niftyStockWatch.json"
        self.nifty_next_50_url      = self.base_url + self.stock_url + \
                                      "juniorNiftyStockWatch.json"
        self.nse_midcap_url         = self.base_url + self.stock_url + \
                                      "niftyMidcap50StockWatch.json"
        self.nifty_500_url          = self.base_url + self.stock_url + \
                                      "nifty500StockWatch.json"
        self.nse_top_volume_url     = self.base_url + \
                                      self.activity_analysis_url + \
                                      "allTopVolume1.json"
        self.nse_top_turnover_url   = self.base_url + \
                                      self.activity_analysis_url + \
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
        
        self._populate_nifty_index_url_dict()

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
    
        #end __init__

    def _populate_nifty_index_url_dict(self):
        self.index_url_dict["NIFTY PHARMA"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxPharmaStockWatch.json"
        self.index_url_dict["NIFTY 500"]    = self.base_url + \
                                    self.stock_url + \
                                    "nifty500StockWatch.json"
        self.index_url_dict["NIFTY BANK"]    = self.base_url \
                                    + self.stock_url + \
                                    "bankNiftyStockWatch.json"
        self.index_url_dict["NIFTY INDIA CONSUMPTION"]    = self.base_url \
                                    + self.stock_url + \
                                    "cnxConsumptionStockWatch.json"
        self.index_url_dict["NIFTY METAL"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxMetalStockWatch.json"
        self.index_url_dict["NIFTY INFRASTRUCTURE"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxInfraStockWatch.json"
        self.index_url_dict["NIFTY COMMODITIES"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxCommoditiesStockWatch.json"
        self.index_url_dict["NIFTY FMCG"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxFMCGStockWatch.json"
        self.index_url_dict["NIFTY IT"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxitStockWatch.json"
        self.index_url_dict["NIFTY SERVICES SECTOR"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxServiceStockWatch.json"
        self.index_url_dict["NIFTY REALTY"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxRealtyStockWatch.json"
        self.index_url_dict["NIFTY FINANCIAL SERVICES"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxFinanceStockWatch.json"
        self.index_url_dict["NIFTY MEDIA"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxMediaStockWatch.json"
        self.index_url_dict["NIFTY AUTO"]    = self.base_url + \
                                    self.stock_url + \
                                    "cnxAutoStockWatch.json"
    #end _populate_nifty_index_url_dict

    def _get_scrip_index(self, scrip_id):
        pe = r.get(self.all_pe_url, timeout=3)
        if pe.raise_for_status() == None:
            pe_json = pe.json()
            if scrip_id not in pe_json:
                raise KeyError("Not a valid scrip: %s" % scrip_id)
            scrip_index = pe_json[scrip_id]["sector"]
        return scrip_index 
    #end _get_scrip_index

    def _get_index_json(self, index_id):
        #need to strip as sector provided in pe 
        #has trailing whitespaces
        index_id = index_id.strip(" ")

        if index_id not in self.index_url_dict:
            raise StandardError("Could not find index url"\
                                ", ask dev to fix this: %s" % index_id)
        index = r.get(self.index_url_dict[index_id], timeout=3)
        if index.raise_for_status() == None:
            return index.json()
    #end _get_index_json
    
    def _get_scrip_json(self, index_json, scrip_id):
        for item in index_json["data"]:
            if item["symbol"] == scrip_id:
                return item
        raise StandardError("Could not find scrip(%s) in index json, ask dev to fix this" % (scrip_id))
    #end _get_scrip_json
    
    #TODO: Document the format of the json returned in a legend section
    def get_scrip_quote(self, scrip_id):
        index_id   = self._get_scrip_index(scrip_id)
        index_json = self._get_index_json(index_id)
        scrip_json = self._get_scrip_json(index_json, scrip_id)
        pprint.pprint(scrip_json)
        return scrip_json
    #end get_scrip_quote

    #TODO: Document the format of the json returned in a legend section
    def get_scrip_pe(self, scrip_id):
        pe = r.get(self.all_pe_url, timeout=3)
        if pe.raise_for_status() == None:
            pe_json = pe.json()
            if scrip_id not in pe_json:
                raise KeyError("Not a valid scrip: %s" % scrip_id)
            print pe_json[scrip_id]["PE"]
            return pe_json[scrip_id]["PE"]
    
    def get_scrip_and_sector_pe(self, scrip_id):
        pe = r.get(self.all_pe_url, timeout=3)
        if pe.raise_for_status() == None:
            pe_json = pe.json()
            if scrip_id not in pe_json:
                raise KeyError("Not a valid scrip: %s" % scrip_id)
            print (pe_json[scrip_id]["sector"].strip(" "), \
                    pe_json[scrip_id]["PE"], pe_json[scrip_id]["sectorPE"])
            return (pe_json[scrip_id]["sector"].strip(" "), \
                    pe_json[scrip_id]["PE"], pe_json[scrip_id]["sectorPE"])
    #end get_scrip_and_sector_pe
    
    #TODO: Mention that the top gainers and losers are based on percentage
    #and not value
    #TODO: format the json data provided to send a dictionary of gainers 
    #with scrip id and percentage change
    def get_top_10_gainers(self):
        top_10 = r.get(self.all_top_gainers_url, timeout=3)
        pprint.pprint(len(top_10.json()["data"]))
        return top_10.json()["data"]
    #end get_top_10_gainers
    
    def get_top_10_losers(self):
        top_10 = r.get(self.all_top_losers_url, timeout=3)
        pprint.pprint(len(top_10.json()["data"]))
        pprint.pprint(top_10.json()["data"])
        return top_10.json()["data"]
    #end get_top_10_losers
