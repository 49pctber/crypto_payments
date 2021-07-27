#
# A class that handles the API for checking the Bitcoin blockchain.
#
# Author: redd
#

from AddrApi import AddrApi
import requests
import json

class BitcoinApi(AddrApi):
    def __init__(self, d):
        super(BitcoinApi, self).__init__(d)

    def _checkBalance(self):
        self.r = requests.get(f'https://mempool.space/api/address/{self.addr}/utxo')
        if self._isReqStatus200():
            d = self.r.json()
            qty = 0
            for utxo in d:
                qty += int(utxo['value'])
            self.qty = qty
            return self.qty
        else:
            raise Exception(f"Error in BitcoinApi._checkBalance(): Invalid status code.")
