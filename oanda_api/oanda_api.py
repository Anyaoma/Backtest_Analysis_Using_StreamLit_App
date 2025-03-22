import json
import pandas as pd
import requests
from datetime import datetime as dt
from dateutil import parser
import constants.constants as comps
from instruments.api_price import ApiPrice


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
