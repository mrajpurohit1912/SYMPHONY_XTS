import configparser
import json
import logging
import requests
from six.moves.urllib.parse import urljoin
import Exception as ex
log = logging.getLogger(__name__)

cfg = configparser.ConfigParser()
cfg.read('config.ini')    

class Symphony:

    _routes = {
        # Interactive API endpoints
        "interactive.prefix": "interactive",
        "user.login": "/interactive/user/session",
        "user.logout": "/interactive/user/session",
        "user.profile": "/interactive/user/profile",
        "user.balance": "/interactive/user/balance",

        "orders": "/interactive/orders",
        "trades": "/interactive/orders/trades",
        "dealer.trades": "/interactive/orders/dealertradebook",
        "order.status": "/interactive/orders",
        "delalerorder.status": "/interactive/orders/dealerorderbook",
        "order.place": "/interactive/orders",
        "bracketorder.place": "/interactive/orders/bracket",
        "order.place.cover": "/interactive/orders/cover",
        "order.exit.cover": "/interactive/orders/cover",
        "order.modify": "/interactive/orders",
        "order.bracket.modify":"/interactive/orders/bracket",
        "order.cancel": "/interactive/orders",
        "order.cancelall": "/interactive/orders/cancelall",
        "order.history": "/interactive/orders",

        "portfolio.positions": "/interactive/portfolio/positions",
        "dealerportfolio.positions": "/interactive/portfolio/dealerpositions",
        "portfolio.holdings": "/interactive/portfolio/holdings",
        "portfolio.positions.convert": "/interactive/portfolio/positions/convert",
        "portfolio.squareoff": "/interactive/portfolio/squareoff",

        # Market API endpoints
        "marketdata.prefix": "marketdata",
        "market.login": "/apimarketdata/auth/login",
        "market.logout": "/apimarketdata/auth/logout",

        "market.config": "/apimarketdata/config/clientConfig",

        "market.instruments.master": "/apimarketdata/instruments/master",
        "market.instruments.subscription": "/apimarketdata/instruments/subscription",
        "market.instruments.unsubscription": "/apimarketdata/instruments/subscription",
        "market.instruments.ohlc": "/apimarketdata/instruments/ohlc",
        "market.instruments.indexlist": "/apimarketdata/instruments/indexlist",
        "market.instruments.quotes": "/apimarketdata/instruments/quotes",

        "market.search.instrumentsbyid": '/apimarketdata/search/instrumentsbyid',
        "market.search.instrumentsbystring": '/apimarketdata/search/instruments',

        "market.instruments.instrument.series": "/apimarketdata/instruments/instrument/series",
        "market.instruments.instrument.equitysymbol": "/apimarketdata/instruments/instrument/symbol",
        "market.instruments.instrument.futuresymbol": "/apimarketdata/instruments/instrument/futureSymbol",
        "market.instruments.instrument.optionsymbol": "/apimarketdata/instruments/instrument/optionsymbol",
        "market.instruments.instrument.optiontype": "/apimarketdata/instruments/instrument/optionType",
        "market.instruments.instrument.expirydate": "/apimarketdata/instruments/instrument/expiryDate"
    }
    
    def __init__(self):
        self.source = cfg.get('user', 'source')
        self.market_root_url = cfg.get('market_root_url', 'root')
        self.interactive_root_url = cfg.get('interactive_root_url', 'root')
        #self.hostkookup_url = cfg.get('host_url', 'hostlookup_url')
        self.market_token = None
        self.market_userid = None
        self.inter_token = None
        self.inter_userid = None
        self.isInvestorClient = None


#####################################################################################################################################################################
############################################################     MARKET DATA API    ###################################################################################################
#####################################################################################################################################################################

    def market_login(self,api_key,secret_key):
        ''' This is login function it takes 2 parameter marketdata api_key and secret_key'''
        try:
            params={"secretKey":secret_key,
            "appKey":api_key,
            "source":self.source}
            response = requests.post(self.market_root_url + Symphony._routes['market.login'] ,params)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            if response['type'] == 'success':
                self.market_token = response['result']['token']
                self.market_userid = response['result']['userID']
            return response
        except Exception as e:
            return e
    def market_logout(self):
        ''' This is logout function '''
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.market_token}
            #params={}
            response = requests.delete(self.market_root_url + Symphony._routes['market.logout'] ,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def get_config(self):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.market_token}
            #params={}
            response = requests.get(self.market_root_url + Symphony._routes['market.config'] ,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def get_quote(self,Instruments,xtsMessageCode):
        ''' This is quote function it takes 2 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
    {'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
    {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]
    2)xtsMessageCode = 1501/1502/1505/1510/1512
    '''
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.market_token}
            params={
              "instruments":Instruments,"xtsMessageCode": xtsMessageCode,"publishFormat":"JSON"
            }
            response = requests.post(self.market_root_url + Symphony._routes['market.instruments.quotes'] ,json.dumps(params),headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

    def send_subscription(self,Instruments,xtsMessageCode):
        ''' This is send_subscription function it takes 2 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
    {'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
    {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]
    2)xtsMessageCode = 1501/1502/1505/1510/1512
    '''
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.market_token}
            params={
              "instruments":Instruments,"xtsMessageCode": xtsMessageCode
            }
            response = requests.post(self.market_root_url + Symphony._routes['market.instruments.subscription'] ,json.dumps(params),headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def send_unsubscription(self,Instruments,xtsMessageCode):
        ''' This is send_unsubscription function it takes 2 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
    {'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
    {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]
    2)xtsMessageCode = 1501/1502/1505/1510/1512
    '''
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.market_token}
            params={
              "instruments":Instruments,"xtsMessageCode": xtsMessageCode
            }
            response = requests.put(self.market_root_url + Symphony._routes['market.instruments.unsubscription'] ,json.dumps(params),headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def get_master(self,exchange_list):
        ''' This is get_master function it takes 1 parameters - 1) exchangeSegmentList = its should be a list containing exchangeSegment
        like ['NSECM','NSECD','NSEFO','BSECM','BSEFO']

        '''
        try:
            headers = {"Content-Type":"application/json",
                        "authorization":self.market_token}
            params={"exchangeSegmentList": exchange_list}
            response = requests.post(self.market_root_url + Symphony._routes['market.instruments.master'] ,json.dumps(params),headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def get_series(self,exchangeSegment):
        ''' This is get_series function it takes 1 parameters - exchangeSegment it should be numeric
        eg: {"NSECM": 1, "NSEFO": 2, "NSECD": 3,"BSECM": 11, "BSEFO": 12, "MCXFO": 51}
        exchangeSegment = 1/2/3/11/15/51
        '''
        try:
            headers = {"Content-Type":"application/json",
                        "authorization":self.market_token}
            params={"exchangeSegment": exchangeSegment}
            response = requests.get(self.market_root_url + Symphony._routes['market.instruments.instrument.series'] ,params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def get_equity_symbol(self,exchangeSegment,series,symbol):
        ''' This is get_equity_symbol function it takes 3 parameters - 1)exchangeSegment it should be numeric
        eg: {"NSECM": 1, "NSEFO": 2, "NSECD": 3,"BSECM": 11, "BSEFO": 12, "MCXFO": 51} ,exchangeSegment = 1/2/3/11/15/51
        2) series = "EQ"/"FO",
        3) symbol = Symbol should be string "Acc"/"Reliance"
        '''
        try:
            headers = {"Content-Type":"application/json",
                        "authorization":self.market_token}
            params={"exchangeSegment": exchangeSegment,
                   "series":series,
                   "symbol":symbol}
            response = requests.get(self.market_root_url + Symphony._routes['market.instruments.instrument.equitysymbol'] ,params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def get_expirydate(self,exchangeSegment,series,symbol):
        ''' This is get_expirydate function it takes 3 parameters - 1)exchangeSegment it should be numeric
        eg: {"NSECM": 1, "NSEFO": 2, "NSECD": 3,"BSECM": 11, "BSEFO": 12, "MCXFO": 51} ,exchangeSegment = 1/2/3/11/15/51
        2) series = "FUTIDX"/"OPTIDX",
        3) symbol = Symbol should be string "NIFTY"/"BANKNIFTY"
        '''
        try:
            headers = {"Content-Type":"application/json",
                        "authorization":self.market_token}
            params={"exchangeSegment": exchangeSegment,"series":series,"symbol":symbol}
            response = requests.get(self.market_root_url + Symphony._routes['market.instruments.instrument.expirydate'] ,params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def get_future_symbol(self,exchangeSegment,series,symbol,expiryDate):
        ''' This is get_future_symbol function it takes 4 parameters - 1)exchangeSegment it should be numeric
        eg: {"NSECM": 1, "NSEFO": 2, "NSECD": 3,"BSECM": 11, "BSEFO": 12, "MCXFO": 51} ,exchangeSegment = 1/2/3/11/15/51
        2) series = "FUTIDX"/"OPTIDX",
        3) symbol = Symbol should be string "NIFTY"/"BANKNIFTY"
        4) expiryDate = 20Sep2019/28Sep2023
        '''
        try:
            headers = {"Content-Type":"application/json",
                        "authorization":self.market_token}
            params={"exchangeSegment": exchangeSegment,"series":series,"symbol":symbol,"expiryDate":expiryDate}
            response = requests.get(self.market_root_url + Symphony._routes['market.instruments.instrument.futuresymbol'] ,params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

    def get_option_symbol(self,exchangeSegment,series,symbol,expiryDate,optionType,strikePrice):
        ''' This is get_option_symbol function it takes 6 parameters - 1)exchangeSegment it should be numeric
        eg: {"NSECM": 1, "NSEFO": 2, "NSECD": 3,"BSECM": 11, "BSEFO": 12, "MCXFO": 51} ,exchangeSegment = 1/2/3/11/15/51
        2) series = "FUTIDX"/"OPTIDX",
        3) symbol = Symbol should be string "NIFTY"/"BANKNIFTY"
        4) expiryDate = 20Sep2019/28Sep2023
        5) optionType = CE/PE
        6) strikePrice = 2000,19000,19100.......
        '''
        try:
            headers = {"Content-Type":"application/json",
                        "authorization":self.market_token}
            params={"exchangeSegment": exchangeSegment,"series":series,"symbol":symbol,"expiryDate":expiryDate,"optionType":optionType,"strikePrice":strikePrice}
            response = requests.get(self.market_root_url + Symphony._routes['market.instruments.instrument.optionsymbol'] ,params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    
    def get_option_type(self,exchangeSegment,series,symbol,expiryDate):
            ''' This is get_option_symbol function it takes 6 parameters - 1)exchangeSegment it should be numeric
            eg: {"NSECM": 1, "NSEFO": 2, "NSECD": 3,"BSECM": 11, "BSEFO": 12, "MCXFO": 51} ,exchangeSegment = 1/2/3/11/15/51
            2) series = "FUTIDX"/"OPTIDX",
            3) symbol = Symbol should be string "NIFTY"/"BANKNIFTY"
            4) expiryDate = 20Sep2019/28Sep2023
            '''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.market_token}
                params={"exchangeSegment": exchangeSegment,"series":series,"symbol":symbol,"expiryDate":expiryDate}
                response = requests.get(self.market_root_url + Symphony._routes['market.instruments.instrument.optiontype'] ,params,headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
    def get_indexlist(self,exchangeSegment):
            ''' This is get_indexlist function it takes 6 parameters - 1)exchangeSegment it should be numeric
            eg: {"NSECM": 1, "NSEFO": 2, "NSECD": 3,"BSECM": 11, "BSEFO": 12, "MCXFO": 51} ,exchangeSegment = 1/2/3/11/15/51
            '''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.market_token}
                params={"exchangeSegment": exchangeSegment}
                response = requests.get(self.market_root_url + Symphony._routes['market.instruments.indexlist'] ,params,headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
    def search_by_instrumentid(self,Instruments):
            ''' This is search_by_instrumentid function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
    [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
    {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]
            '''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.market_token}
                params={"source":self.source,"UserID":self.userid,"instruments": Instruments}
                response = requests.post(self.market_root_url + Symphony._routes['market.search.instrumentsbyid'] ,json.dumps(params),headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
    def search_by_scriptname(self,searchString):
            ''' This is search_by_scriptname function it takes 1 parameters - 1) searchString = its should be a string containing name of the instrumet
            eg: "RELIANCE"/"ACC"
            '''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.market_token}
                params={"source":self.source,"searchString":searchString}
                response = requests.get(self.market_root_url + Symphony._routes['market.search.instrumentsbystring'] ,params,headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
    def get_ohlc(self,exchangesegment,exchangeinstrumentid,starttime,endtime,compressionvalue):
        ''' This is get_ohlc function it takes 5 parameters - 1)exchangeSegment it should be string
        eg: ["NSECM", "NSEFO", "NSECD","BSECM","BSEFO","MCXFO"]
        2) exchangeInstrumentID = It should be integer eg: 22/2885/25
        3) StartTime = Default: "Jul 01 2020 091500",Format: MMM DD YYYY HHMMSS
        4) EndTime = Default: "Jul 01 2020 153000",Format: MMM DD YYYY HHMMSS
        5) compressionValue = "In1Second:1" "In1Minute: 60" "In2Minute : 120" "In3Minute : 180" "In5Minute : 300" "In10Minute : 600" "In15Minute : 900" "In30Minute : 1800" "In60Minute : 3600"        '''
        try:
            headers = {"Content-Type":"application/json",
                        "authorization":self.market_token}
            params={"exchangeSegment": exchangesegment,"exchangeInstrumentID":exchangeinstrumentid,"StartTime":starttime,"EndTime":endtime,"compressionValue":compressionvalue}
            response = requests.get(self.market_root_url + Symphony._routes['market.instruments.ohlc'],params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

#####################################################################################################################################################################
############################################################     Interactive DATA API    ###################################################################################################
#####################################################################################################################################################################


    def interactive_login(self,api_key,secret_key):
        ''' This is Interactive login function it takes 2 parameter marketdata api_key and secret_key'''
        try:
            params={"secretKey":secret_key,
            "appKey":api_key,
            "source":self.source}
            response = requests.post(self.interactive_root_url + Symphony._routes['user.login'] ,params)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            if response['type'] == 'success':
                self.inter_token = response['result']['token']
                self.inter_userid = response['result']['userID']
                self.isInvestorClient = response['result']['isInvestorClient']
            return response
        except Exception as e:
            return e

    def interactive_logout(self):
        ''' This is logout function '''
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            #params={}
            response = requests.delete(self.interactive_root_url + Symphony._routes['user.logout'] ,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

    def profile(self):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            #params={}
            response = requests.get(self.interactive_root_url + Symphony._routes['user.profile'] ,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

    def balance(self):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            #params={}
            response = requests.get(self.interactive_root_url + Symphony._routes['user.balance'] ,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
            
    def place_order(self,exchangeSegment,exchangeInstrumentID,productType,orderType,orderSide,timeInForce,disclosedQuantity,orderQuantity,limitPrice,stopPrice,orderUniqueIdentifier,clientid=None):            
        ''' This is place_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
            [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
            {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
        try:
            headers = {"Content-Type":"application/json",
                        "authorization":self.inter_token}
            params={"exchangeSegment": exchangeSegment,"exchangeInstrumentID": exchangeInstrumentID,"productType": productType,"orderType": orderType,"orderSide": orderSide,
                    "timeInForce": timeInForce,"disclosedQuantity": disclosedQuantity,"orderQuantity": orderQuantity,"limitPrice": limitPrice,"stopPrice": stopPrice,"orderUniqueIdentifier": orderUniqueIdentifier,"clientID":clientid}
            response = requests.post(self.interactive_root_url + Symphony._routes['order.place'] ,json.dumps(params),headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

    def modify_order(self,appOrderID,modifiedProductType,modifiedOrderType,modifiedOrderQuantity,modifiedDisclosedQuantity,modifiedLimitPrice,modifiedStopPrice,modifiedTimeInForce,orderUniqueIdentifier,clientid=None):            
            ''' This is modify_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
                [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.inter_token}
                params={"appOrderID": appOrderID,"modifiedProductType": modifiedProductType,"modifiedOrderType": modifiedOrderType,"modifiedOrderQuantity": modifiedOrderQuantity,
                        "modifiedDisclosedQuantity": modifiedDisclosedQuantity,"modifiedLimitPrice": modifiedLimitPrice,"modifiedStopPrice": modifiedStopPrice,"modifiedTimeInForce": modifiedTimeInForce,"orderUniqueIdentifier": orderUniqueIdentifier,"clientID":clientid}
                response = requests.put(self.interactive_root_url + Symphony._routes['order.place'] ,json.dumps(params),headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
    def cancel_order(self,appOrderID,clientid=None):            
            ''' This is place_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
                [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.inter_token}
                params={"appOrderID":appOrderID,
                        "clientID":clientid}
                response = requests.delete(self.interactive_root_url + Symphony._routes['order.cancel'] ,params=params,headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e

    def cancell_all(self,exchangeSegment,exchangeInstrumentID,clientid=None): 
            ''' This is cancell_all function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
                [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.inter_token}
                params={"exchangeSegment":exchangeSegment,"exchangeInstrumentID": exchangeInstrumentID,"clientID":clientid}
                response = requests.post(self.interactive_root_url + Symphony._routes['order.cancelall'] ,json.dumps(params),headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e

    def bracket_order(self,exchangeSegment,exchangeInstrumentID,orderSide,disclosedQuantity,limitPrice,orderType,orderQuantity,squarOff,stopLossPrice,trailingStoploss,isProOrder,orderUniqueIdentifier,clientid=None):            
            ''' This is place_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
                [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.inter_token}
                params={"exchangeSegment":exchangeSegment,"exchangeInstrumentID": exchangeInstrumentID,"orderSide":orderSide,"disclosedQuantity":disclosedQuantity,"limitPrice" : limitPrice,
                        "orderType":orderType,"orderQuantity":orderQuantity,"squarOff" :squarOff,"stopLossPrice":stopLossPrice,"trailingStoploss":trailingStoploss,"isProOrder":isProOrder,
                        "orderUniqueIdentifier":orderUniqueIdentifier,"clientID":clientid}
                response = requests.post(self.interactive_root_url + Symphony._routes['bracketorder.place'] ,json.dumps(params),headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
                
    def bracket_modify_order(self,appOrderID,limitPrice,stopLossPrice,orderQuantity):            
            ''' This is modify_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
                [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.inter_token}
                params={"appOrderID" :appOrderID,"limitPrice":limitPrice,"stopLossPrice":stopLossPrice,"orderQuantity":orderQuantity}
                response = requests.put(self.interactive_root_url + Symphony._routes['order.bracket.modify'] ,json.dumps(params),headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
    # def bracket_cancel_order(self,appOrderID):            
    #         ''' This is place_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
    #             [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
    #             {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
    #         try:
    #             headers = {"Content-Type":"application/json",
    #                         "authorization":self.inter_token}
    #             params={"appOrderID":appOrderID}
    #             response = requests.delete(self.interactive_root_url + Symphony._routes['order.cancel'] ,params=params,headers=headers)
    #             response = response.content.decode('utf-8')
    #             response = json.loads(response)
    #             return response
    #         except Exception as e:
    #             return e
    def cover_order(self,exchangeSegment,exchangeInstrumentID,orderSide,orderQuantity,disclosedQuantity,limitPrice,stopPrice,orderType,orderUniqueIdentifier,clientid=None):            
            ''' This is place_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
                [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.inter_token}
                params={"exchangeSegment": exchangeSegment,"exchangeInstrumentID": exchangeInstrumentID,"orderSide": orderSide,"orderQuantity": orderQuantity,"disclosedQuantity": disclosedQuantity,
                      "limitPrice": limitPrice,"stopPrice": stopPrice,"orderType": orderType,"orderUniqueIdentifier": orderUniqueIdentifier,"clientID":clientid}
                response = requests.post(self.interactive_root_url + Symphony._routes['order.place.cover'] ,json.dumps(params),headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
    def exit_cover_order(self,appOrderID,clientid=None):            
            ''' This is modify_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
                [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.inter_token}
                params={"appOrderID" :appOrderID,"clientID":clientid}
                response = requests.put(self.interactive_root_url + Symphony._routes['order.exit.cover'] ,json.dumps(params),headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e
    def order_book(self):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            params={}
            response = requests.get(self.interactive_root_url + Symphony._routes['order.status'] ,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def trade_book(self):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            params={}
            response = requests.get(self.interactive_root_url + Symphony._routes['trades'] ,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
        
    def dealer_order_book(self,clientid=None):
        try:
            if clientid != None:
                params={"clientID":clientid}
            else:
                params={}
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            response = requests.get(self.interactive_root_url + Symphony._routes['delalerorder.status'] ,headers=headers,params=params)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def dealer_trade_book(self,clientid=None):
        try:
            if clientid != None:
                params={"clientID":clientid}
            else:
                params={}
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}

            #params={"clientID":clientid}
            response = requests.get(self.interactive_root_url + Symphony._routes['dealer.trades'] ,headers=headers,params=params)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

    def order_history(self,appOrderID):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            params={"appOrderID":appOrderID}
            response = requests.get(self.interactive_root_url + Symphony._routes['order.history'],params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def holdings(self):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            #params={}
            response = requests.get(self.interactive_root_url + Symphony._routes['portfolio.holdings'] ,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e
    def positions(self,dayOrNet):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            params={"dayOrNet":dayOrNet}
            response = requests.get(self.interactive_root_url + Symphony._routes['portfolio.positions'],params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

    def dealer_positions(self,dayOrNet,clientid=None):
        try:
            headers = {"Content-Type":"application/json",
            "authorization":self.inter_token}
            params={"dayOrNet":dayOrNet,"clientID":clientid}
            response = requests.get(self.interactive_root_url + Symphony._routes['dealerportfolio.positions'],params,headers=headers)
            response = response.content.decode('utf-8')
            response = json.loads(response)
            return response
        except Exception as e:
            return e

    def position_convert(self,exchangeSegment,exchangeInstrumentID,oldProductType,newProductType,isDayWise,targetQty,statisticsLevel,isInterOpPosition):            
            ''' This is modify_order function it takes 1 parameters - 1) Instruments = its should be a list containing exchangeSegment & exchangeInstrumentID [
                [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
                {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]'''
            try:
                headers = {"Content-Type":"application/json",
                            "authorization":self.inter_token}
                params={"exchangeSegment": exchangeSegment,"exchangeInstrumentID": exchangeInstrumentID,"oldProductType": oldProductType,"newProductType": newProductType,
                        "isDayWise": isDayWise,"targetQty": targetQty,"statisticsLevel": statisticsLevel,"isInterOpPosition": isInterOpPosition}
                response = requests.put(self.interactive_root_url + Symphony._routes['portfolio.positions.convert'] ,json.dumps(params),headers=headers)
                response = response.content.decode('utf-8')
                response = json.loads(response)
                return response
            except Exception as e:
                return e