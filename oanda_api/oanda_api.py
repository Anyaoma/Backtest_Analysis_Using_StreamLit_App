import json
import pandas as pd
import requests
from datetime import datetime as dt
from dateutil import parser
import constants.constants as comps
from instruments.api_price import ApiPrice
from instruments.instrument_data import instrumentCollection as ic


class OandaApi:
    def __init__(self):
        self.name = 'OandaApi'

   
    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=comps.SECURE_HEADER):
        full_url = f"{comps.OANDA_URL}/{url}"

        if data is not None:
            data = json.dumps(data)

        try:
            response = None
            if verb == 'get':
                response = requests.get(full_url, params=params, data=data, headers=headers)

            if verb == 'post':
                response = requests.post(full_url, params=params, data=data, headers=headers)

            if verb == 'put':
                response = requests.put(full_url, params=params, data=data, headers=headers)

            if response == None:
                return False, {'Error encountered':'data not found'}
            
            if response.status_code == code:
                return True, response.json()
            else:
                return False, response.json()
        except Exception as error:
            return False, {'Exception': error}
        

    def get_account_ep(self, ep, data_key):
        url = f"accounts/{comps.ACCOUNT_ID}/{ep}"
        ok, data = self.make_request(url)

        if ok == True and data_key in data:
            #print(data[data_key])
            return data[data_key]
        else:
            print("Error get_account_ep()", data)
            return None

    def get_account_summary(self):
        return self.get_account_ep('summary', 'account')

    def get_instruments(self):
        return self.get_account_ep('instruments', 'instruments')
        
    
    def fetch_candles(self, pair_name, count=10, granularity='M15',price='MBA', date_f=None, date_t=None):
        url = f'instruments/{pair_name}/candles'
        params = dict(granularity= granularity,price=price)
        if date_f is not None and date_t is not None:
            date_format = '%Y-%m-%dT%H:%M:%SZ'
            params['from'] = dt.strftime(date_f, date_format)
            params['to'] = dt.strftime(date_t, date_format)
        else:
            params['count'] = count

        ok, data = self.make_request(url, params=params)
        if ok == True and 'candles' in data:
            return data['candles']
        else:
            print("ERROR fetch_candles()", params, data)
            return None
            
    
    def get_candles_df(self, pair_name, **kwargs):
        data = self.fetch_candles(pair_name, **kwargs)

        if data == None:
            return None
        if len(data) == 0:
            return pd.DataFrame()
        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']
        
        final_data = []
        for candle in data:
            if candle['complete'] == False:
                continue
            new_dict = {}
            new_dict['time'] = parser.parse(candle['time'])
            new_dict['volume'] = candle['volume']
            for p in prices:
                if p in candle:
                    for o in ohlc:
                        new_dict[f"{p}_{o}"] = float(candle[p][o])
            final_data.append(new_dict)
        df = pd.DataFrame.from_dict(final_data)
        return df


    def place_trade(self, pair_name, units, direction:int, stop_loss:float=None, take_profit:float=None):
        url = f"accounts/{comps.ACCOUNT_ID}/orders"

        #Since ic has been instantiated, api_test.py must ensure that ic.instruments_dict is populated before calling place_trade.
        #this is done by api_test.py importing the instanciated ic same as above and also the place trade function, populate the ic,
        #then call the place trade function.
        instrument = ic.instruments_dict[pair_name]
        units = round(units, instrument.tradeUnitsPrecision)

        if direction == comps.SELL:
            units = units * -1

        data = dict(
            order=dict(
                units=str(units),
                instrument = pair_name,
                type="MARKET"
            )
        )
        if stop_loss is not None:
            sld = dict(price = str(round(stop_loss, instrument.displayPrecision)))
            data['order']['stopLossOnFill'] = sld
        
        if take_profit is not None:
            tpd = dict(price = str(round(take_profit, instrument.displayPrecision)))
            data['order']['takeProfitOnFill'] = tpd

        #print(data)

        ok, response = self.make_request(url, verb='post', data=data, code=201)
        #print(ok, response)

        if ok == True and 'orderFillTransaction' in response:
            return response['orderFillTransaction']['id']
        else:
            return None

    def close_trade(self, trade_id):
        url = f"accounts/{comps.ACCOUNT_ID}/trades/{trade_id}/close"

        ok, _ = self.make_request(url, verb='put', code=200)

        if ok == True:
            print('trade_id:',trade_id, 'has been closed successfully')
        else:
            print(f'failed to close {trade_id}')

        return ok
    
    def get_prices(self, instrument_list):
        url = f"accounts/{comps.ACCOUNT_ID}/pricing"
        params = dict(
            instruments= ','.join(instrument_list),
            includeHomeConversions = True
    
        )
        ok, response = self.make_request(url, params=params)
        if ok == True and 'prices' in response and 'homeConversions' in response:
            return [ApiPrice(x, response['homeConversions']) for x in (response['prices'])]
        return None
        

oandaApi = OandaApi()