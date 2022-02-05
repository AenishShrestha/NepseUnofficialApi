import requests
from collections import defaultdict
from json import JSONDecodeError
import json
import time
from datetime import date

class TokenParser():
    def __init__(self):
        ###############################################MAGIC ARRAY###############################################
        #FOR details check http://newweb.nepalstock.com/assets/prod/css.wasm
        #decompiling the wasm gives access to the following magic array and (rdx, cdx) function
        self.data_segment_data_0 = [
                                      0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 
                                      0x07, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 
                                      0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                      0x09, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x06, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 
                                      0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 
                                      0x03, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x04, 
                                    ]
        
    def rdx(self, w2c_p0, w2c_p1, w2c_p2, w2c_p3, w2c_p4):

        w2c_i0 = w2c_p1
        w2c_i1 = 100
        w2c_i0 = w2c_i0 // w2c_i1
        w2c_i1 = 10
        w2c_i0 = w2c_i0 % w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = 10
        w2c_i1 = w2c_i1 // w2c_i2
        w2c_p0 = w2c_i1
        w2c_i2 = 10
        w2c_i1 = w2c_i1 % w2c_i2
        w2c_i0 += w2c_i1
        w2c_p2 = w2c_i0
        w2c_i1 = w2c_p2
        w2c_i2 = w2c_p1
        w2c_i3 = w2c_p0
        w2c_i4 = 10
        w2c_i3 *= w2c_i4
        w2c_i2 -= w2c_i3
        w2c_i1 += w2c_i2
        w2c_i2 = 2
        w2c_i1 <<= (w2c_i2 & 31)

        w2c_i1 = self.data_segment_data_0[w2c_i1]
        w2c_i0 += w2c_i1
        w2c_i1 = 22
        w2c_i0 += w2c_i1
        return w2c_i0


    def cdx(self, w2c_p0, w2c_p1, w2c_p2, w2c_p3, w2c_p4):
        w2c_i0 = w2c_p1
        w2c_i1 = 10
        w2c_i0 = w2c_i0 // w2c_i1
        w2c_p0 = w2c_i0
        w2c_i1 = 10
        w2c_i0 = w2c_i0 % w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = w2c_p0
        w2c_i3 = 10
        w2c_i2 *= w2c_i3
        w2c_i1 -= w2c_i2
        w2c_i0 += w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = 100
        w2c_i1 = w2c_i1 // w2c_i2
        w2c_i2 = 10
        w2c_i1 = w2c_i1 % w2c_i2
        w2c_i0 += w2c_i1
        w2c_i1 = 2
        w2c_i0 <<= (w2c_i1 & 31)

        w2c_i0 = self.data_segment_data_0[w2c_i0]
        w2c_i1 = 22
        w2c_i0 += w2c_i1

        return w2c_i0

    def parse_token_response(self, token_response):
        n = self.cdx(token_response['salt1'], token_response['salt2'], token_response['salt3'], token_response['salt4'], token_response['salt5']);
        l = self.rdx(token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5']);
        
        i = self.cdx(token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt5'], token_response['salt4']);
        r = self.rdx(token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt4'], token_response['salt5']);

        access_token  = token_response['accessToken']
        refresh_token = token_response['refreshToken']
        
        parsed_access_token  = access_token[0:n] + access_token[n + 1: l] + access_token[l + 1:]
        parsed_refresh_token = refresh_token[0:i] + refresh_token[i + 1: r] + refresh_token[r + 1:]
    
        #returns both access_token and refresh_token, i don't know what's the purpose of refresh token.
        #Right now new access_token can be used for every new api request
        return (parsed_access_token, parsed_refresh_token)

class Nepse:
    def __init__(self):
        self.token_request_count = 0 
        self.total_request_count = 0
        
        self.token_parser     = TokenParser()

        self.base_url             = "https://www.nepalstock.com.np"
        
        self.token_url            = f"{self.base_url}/api/authenticate/prove"
        self.refresh_url          = f"{self.base_url}/api/authenticate/refresh-token"

        self.post_payload_id      = None

        self.company_symbol_id_keymap = None
        
        self.floor_sheet_size = 500
        
        self.api_end_points = {
                                "price_volume_url"     : f"{self.base_url}/api/nots/securityDailyTradeStat/58",
                                "summary_url"          : f"{self.base_url}/api/nots/market-summary/",
                                "top_ten_scrips_url"   : f"{self.base_url}/api/nots/top-ten/trade-qty",
                                "supply_demand_url"    : f"{self.base_url}/api/nots/nepse-data/supplydemand",
                                "turnover_url"         : f"{self.base_url}/api/nots/top-ten/turnover",
                                "top_gainers_url"      : f"{self.base_url}/api/nots/top-ten/top-gainer",
                                "top_losers_url"       : f"{self.base_url}/api/nots/top-ten/top-loser",
                                "nepse_open_url"       : f"{self.base_url}/api/nots/nepse-data/market-open",
                                "nepse_index_url"      : f"{self.base_url}/api/nots/nepse-index",
                                "nepse_subindices_url" : f"{self.base_url}/api/nots",
                                "nepse_isopen"         : f"{self.base_url}/api/nots/nepse-data/market-open",

                                "company_list_url"     : f"{self.base_url}/api/nots/company/list",

                                ###graph data api (these requires post request) ####
                                "nepse_index_daily_graph"          : f"{self.base_url}/api/nots/graph/index/58",
                                "sensitive_index_daily_graph"      : f"{self.base_url}/api/nots/graph/index/57",
                                "float_index_daily_graph"          : f"{self.base_url}/api/nots/graph/index/62",
                                "sensitive_float_index_daily_graph": f"{self.base_url}/api/nots/graph/index/63",
                                
                                ##sub index graph##
                                "banking_sub_index_graph"          : f"{self.base_url}/api/nots/graph/index/51",
                                "development_bank_sub_index_graph" : f"{self.base_url}/api/nots/graph/index/55",
                                "finance_sub_index_graph"          : f"{self.base_url}/api/nots/graph/index/60",
                                "hotel_tourism_sub_index_graph"    : f"{self.base_url}/api/nots/graph/index/52",
                                "hydro_sub_index_graph"            : f"{self.base_url}/api/nots/graph/index/54",
                                "investment_sub_index_graph"       : f"{self.base_url}/api/nots/graph/index/67",
                                "life_insurance_sub_index_graph"   : f"{self.base_url}/api/nots/graph/index/65",
                                "manufacturing_sub_index_graph"    : f"{self.base_url}/api/nots/graph/index/56",
                                "microfinance_sub_index_graph"     : f"{self.base_url}/api/nots/graph/index/64",
                                "mutual_fund_sub_index_graph"      : f"{self.base_url}/api/nots/graph/index/66",
                                "non_life_insurance_sub_index_graph": f"{self.base_url}/api/nots/graph/index/59",
                                "others_sub_index_graph"            : f"{self.base_url}/api/nots/graph/index/53",
                                "trading_sub_index_graph"           : f"{self.base_url}/api/nots/graph/index/61",

                                ##company_graph_data (add company id after the frontslash)##
                                "company_daily_graph"               : f"{self.base_url}/api/nots/market/graphdata/daily/",
                                "company_details"                   : f"{self.base_url}/api/nots/security/",
                                "company_price_volume_history"      : f"{self.base_url}/api/nots/market/security/price/",
                                "company_floorsheet"                : f"{self.base_url}/api/nots/security/floorsheet/",

                                "floor_sheet"                       : f"{self.base_url}/api/nots/nepse-data/floorsheet",

                                "todays_price"         : f"{self.base_url}/api/nots/nepse-data/today-price?&size=20&securityId=2742&businessDate=2022-01-06",
                              }
        
        self.api_end_point_access_token = defaultdict(lambda : False)
        
        self.headers= {
                            'Host': 'www.nepalstock.com.np',
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                            'Accept': 'application/json, text/plain, */*',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Referer': 'https://www.nepalstock.com.np/',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'TE': 'Trailers',
                        }
    ###############################################PRIVATE METHODS###############################################
    
    def requestAPI(self, url):
        self.incrementTotalRequestCount()
        
        headers = self.headers
        if url in self.api_end_points.values():
            access_token, request_token = self.getTokenForURL(url)
            headers = {'Authorization': f'Salter {access_token}', **self.headers}
        
        
        response = requests.get(url, headers=headers)
        if (response.status_code != 200):
            self.refreshTokenForURL(url)
            return self.requestAPI(url) 
        
        return response.json()
    
    def requestPOSTAPI(self, url):
        self.incrementTotalRequestCount()
        
        
        access_token, request_token = self.getTokenForURL(url)
        
        headers = {'Content-Type':'application/json', 'Authorization': f'Salter {access_token}', **self.headers, }
        response = requests.post(url, headers=headers, data=json.dumps({"id": self.getPOSTPayloadID()}))
        
        if (response.status_code != 200):
            self.refreshTokenForURL(url)
            return self.requestAPI(url)
        
        return response.json()
            
    
    #token is unique for each url, when token is requested, the access token received when first used for accessing a url can be 
    #used to send multiple request for the same url without requesting new access token.
    def getTokenForURL(self, url):
        if self.api_end_point_access_token[url] is False:
            token_response = self.getValidToken()
            self.api_end_point_access_token[url] = token_response
        
        return self.api_end_point_access_token[url]
    
    def refreshTokenForURL(self, url):
        print(f'token refresh: {url}')
        
        access_token, refresh_token = self.api_end_point_access_token[url]

        data=json.dumps({'refreshToken':refresh_token})

        headers= {**self.headers, 
                    "Content-Type": "application/json",
                    "Content-Length": str(len(data)),
                    "Authorization": f"Salter {access_token}"
                 }
        
        refresh_key = requests.post(self.refresh_url, 
                                    headers=headers, 
                                    data=data)
        
        if refresh_key.status_code != 200:
            self.resetTokenForURL(url)
        else:
            self.api_end_point_access_token[url] = self.getValidTokenFromJSON( refresh_key.json() )
        
    def resetTokenForURL(self, url):
        self.api_end_point_access_token[url] = False
        
#         self.api_end_point_access_token[url] = False
    def getValidTokenFromJSON(self, token_response):
        for salt_index in range(1, 6):
            token_response[f'salt{salt_index}'] = int(token_response[f'salt{salt_index}'])
        
        #returns access_token only, refresh token is not used right now
        return self.token_parser.parse_token_response(token_response)
        
    def getValidToken(self):
        self.incrementTokenRequestCount()
        
        token_response = self.requestAPI(url=self.token_url)        
        return self.getValidTokenFromJSON(token_response)
    
    def incrementTokenRequestCount(self):
        self.token_request_count += 1
        
    def incrementTotalRequestCount(self):
        self.total_request_count += 1

    ##################method to get post payload id#################################33
    def getDummyID(self):
        return self.getMarketStatus()['id']
    
    def getDummyData(self):
        return [147, 117, 239, 143, 157, 312, 161, 612, 512, 804, 411, 527, 170,
            511, 421, 667, 764, 621, 301, 106, 133, 793, 411, 511, 312, 423,
            344, 346, 653, 758, 342, 222, 236, 811, 711, 611, 122, 447, 128,
            199, 183, 135, 489, 703, 800, 745, 152, 863, 134, 211, 142, 564,
            375, 793, 212, 153, 138, 153, 648, 611, 151, 649, 318, 143, 117,
            756, 119, 141, 717, 113, 112, 146, 162, 660, 693, 261, 362, 354,
            251, 641, 157, 178, 631, 192, 734, 445, 192, 883, 187, 122, 591,
            731, 852, 384, 565, 596, 451, 772, 624, 691,
          ]
    
    def _getPOSTPayloadID(self):
        if self.post_payload_id is None:
            dummy_id = self.getDummyID()
            self.post_payload_id = self.getDummyData()[dummy_id] + dummy_id + 2*(date.today().day)
        
        return self.post_payload_id
    
    def getPOSTPayloadID(self):
        return self._getPOSTPayloadID()
    
    ###############################################PUBLIC METHODS###############################################
    def getMarketStatus(self):
        return self.requestAPI(url=self.api_end_points['nepse_isopen'])

    def getTotalRequestCount(self):
        return self.total_request_count
    
    def getTokenRequestCount(self):
        return self.token_request_count
        
    def getPriceVolume(self):
        return self.requestAPI(url=self.api_end_points['price_volume_url'])
    
    def getSummary(self):
        return self.requestAPI(url=self.api_end_points['summary_url'])
    
    def getTopTenScrips(self):
        return self.requestAPI(url=self.api_end_points['top_ten_scrips_url'])
    
    def getSupplyDemand(self):
        return self.requestAPI(url=self.api_end_points['supply_demand_url'])
    
    def getTopGainers(self):
        return self.requestAPI(url=self.api_end_points['top_gainers_url'])
    
    def getTopLosers(self):
        return self.requestAPI(url=self.api_end_points['top_losers_url'])
    
    def isNepseOpen(self):
        return self.requestAPI(url=self.api_end_points['nepse_open_url'])
    
    def getNepseIndex(self):
        return self.requestAPI(url=self.api_end_points['nepse_index_url'])
    
    def getNepseSubIndices(self):
        return self.requestAPI(url=self.api_end_points['nepse_subindices_url'])
    
    def getCompanyList(self):
        return self.requestAPI(url=self.api_end_points['company_list_url'])
    
    def getCompanyIDKeyMap(self):
        if self.company_symbol_id_keymap is None:
            company_list = self.getCompanyList()
            self.company_symbol_id_keymap = {company['symbol']:company['id'] for company in company_list}
        return self.company_symbol_id_keymap
    
    #####api requiring post method 
    def getDailyNepseIndexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['nepse_index_daily_graph'])

    def getDailySensitiveIndexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['sensitive_index_daily_graph'])

    def getDailyFloatIndexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['float_index_daily_graph'])
    
    def getDailySensitiveFloatIndexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['sensitive_float_index_daily_graph'])

    def getDailyBankSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['banking_sub_index_graph'])
    def getDailyDevelopmentBankSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['development_bank_sub_index_graph'])
    def getDailyFinanceSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['finance_sub_index_graph'])
    def getDailyHotelTourismSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['hotel_tourism_sub_index_graph'])
    def getDailyHydroSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['hydro_sub_index_graph'])
    def getDailyInvestmentSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['investment_sub_index_graph'])
    def getDailyLifeInsuranceSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['life_insurance_sub_index_graph'])
    def getDailyManufacturingSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['manufacturing_sub_index_graph'])
    def getDailyMicrofinanceSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['microfinance_sub_index_graph'])
    def getDailyMutualfundSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['mutual_fund_sub_index_graph'])
    def getDailyNonLifeInsuranceSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['non_life_insurance_sub_index_graph'])
    def getDailyOthersSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['others_sub_index_graph'])
    def getDailyTradingSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points['trading_sub_index_graph'])
    
    def getCompanyDailyPriceGraph(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(url=f"{self.api_end_points['company_daily_graph']}{company_id}")
    
    def getCompanyDetails(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(url=f"{self.api_end_points['company_details']}{company_id}")

    ##unfinished 
    def getCompanyPriceVolumeHistory(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(url=f"{self.api_end_points['company_price_volume_history']}{company_id}")
    
    def getFloorSheet(self):
        url = f"{self.api_end_points['floor_sheet']}?=&size={self.floor_sheet_size}&sort=contractId,asc"
        sheet = self.requestPOSTAPI(url=url)
        floor_sheets = sheet['floorsheets']['content']
        for page in range(1, sheet['floorsheets']['totalPages']+1):
            next_sheet = self.requestPOSTAPI(url=f"{url}&page={page}")
            next_floor_sheet = next_sheet['floorsheets']['content']
            floor_sheets.extend(next_floor_sheet)
        return floor_sheets
    
    def getFloorSheetOf(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        url = f"{self.api_end_points['company_floorsheet']}{company_id}?=&size={self.floor_sheet_size}&sort=contractId,asc&businessDate={date.isoformat(date.today())}"
        sheet = self.requestPOSTAPI(url=url)
        floor_sheets = sheet['floorsheets']['content']
        for page in range(1, sheet['floorsheets']['totalPages']+1):
            next_sheet = self.requestPOSTAPI(url=f"{url}&page={page}")
            next_floor_sheet = next_sheet['floorsheets']['content']
            floor_sheets.extend(next_floor_sheet)
        return floor_sheets


def test():
    a = Nepse()
    print(a.getFloorSheetOf("MLBBL"))
if __name__ == '__main__':
    test()
