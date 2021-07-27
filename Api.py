#
# Classes to manage the APIs for checking address balances.
#
# AddrApi Must inherit self._checkBalance(). This varies for each blockchain, so look at BitcoinApi or CardanoApi for how to implement functioning classes.
#
# Author: redd
#

import requests
import os

class AddrApi:
    def __init__(self, d):
        self.addr = d['addr'] # target address
        self.r = None # http response
        self.qty = d['prev_qty'] # [lovelace] amount found in self.addr
        self.prev_qty = d['prev_qty'] # [lovelace] amount found from previous API calls
        self.network = d['network']
    
    def _isReqStatus200(self):
        try:
            return self.r.status_code == 200
        except:
            return False

    def getAddrInfo(self):
        return {
            'addr': self.addr,
            'prev_qty': self.prev_qty,
            'network': self.network
        }

    def checkForPayment(self, threshold=1):
        self._checkBalance()
        qty_chg = self.qty - self.prev_qty
        
        if qty_chg >= threshold: # enough for payment has been received
            self.prev_qty = self.qty # reset address balance
            # save address state
            return True, qty_chg
        elif qty_chg < 0: # money withdrawn since last check
            self.prev_qty = self.qty # reset address balance
            return False, qty_chg
        else: # not enough for payment
            return False, qty_chg


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
            raise Exception(f"Error in CardanoApi._checkBalance(): Invalid status code.")


class EthereumApi(AddrApi):

    def __init__(self, d):
        super(EthereumApi,self).__init__(d)
        self.apikey = self._getApiKey()

    def _getApiKey(self):
        return os.environ.get('ETHERSCAN_TOKEN')

    def _checkBalance(self):
        self.r = requests.get(f'https://api.etherscan.io/api?module=account&action=balance&address={self.addr}&tag=latest&apikey={self.apikey}')
        if self._isReqStatus200():
            d = self.r.json()
            self.qty = int(int(d['result']) / 1e9) # gwei
            return self.qty
        else:
            raise Exception(f"Error in Ethereum._checkBalance(): Invalid status code.")