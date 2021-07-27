import json
import requests
import os 
from AddrApi import AddrApi

class CardanoApi(AddrApi):

    def __init__(self, d):
        super(CardanoApi,self).__init__(d)
        self.header = self._getBlockfrostHeader() # header includes API key for Blockfrost requests

    def _getApiKey(self):
        return os.environ.get('BLOCKFROST_TOKEN') # gets your Blockfrost API key

    def _getBlockfrostHeader(self):
        return {'project_id':self._getApiKey()}
    
    def _checkBalance(self):
        self.r = requests.get(f'https://{self.network}.blockfrost.io/api/v0/addresses/{self.addr}', headers=self.header)
        if self._isReqStatus200():
            d = self.r.json()
            for i in d['amount']:
                if i['unit'] == 'lovelace':
                    self.qty = int(i['quantity'])
                    return self.qty
            return None
        else:
            raise Exception(f"Error in BlockFrostApi._checkBalance(): Invalid status code.")
