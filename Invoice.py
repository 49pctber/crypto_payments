#
# A class used to denominate payments in terms of USD.
#
# Uses Coin Gecko API.
#
# Author: redd
#

import requests


class Invoice:  
    def __init__(self, usdValue=None):
        self.values = self._getDefaultValues()
        if usdValue != None:
            self.setUsdValue(usdValue)

    def _getDefaultValues(self):
        return {
            'bitcoin-mainnet' : 1,
            'bitcoin-testnet' : 1,
            'ethereum-mainnet' : 1,
            'ethereum-testnet' : 1,
            'cardano-mainnet' : 1,
            'cardano-testnet' : 1,
            'dogecoin-mainnet' : 1,
            'dogecoin-testnet' : 1,
            'litecoin-mainnet' : 1,
            'litecoin-testnet' : 1
        }

    def setValue(self, network, threshold):
        """Set the price for a specific network."""
        self.values[network] = threshold

    def setUsdValue(self, value):
        """Use CoinGecko.com to determine the price in terms of USD."""
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Ccardano%2Cdogecoin%2Clitecoin&vs_currencies=usd")
        if r.status_code == 200:
            d = r.json()
            # calculate USD equivalent
            self.values['bitcoin-mainnet'] = int(value / float(d['bitcoin']['usd']) * 1e8) # satoshi
            self.values['ethereum-mainnet'] = int(value / float(d['ethereum']['usd']) * 1e9) # gwei
            self.values['cardano-mainnet'] = int(value / float(d['cardano']['usd']) * 1e6) # lovelace
            self.values['litecoin-mainnet'] = int(value / float(d['litecoin']['usd']) * 1e8) # litoshi
            self.values['dogecoin-mainnet'] = int(value / float(d['dogecoin']['usd']) * 1e8) #
            # set same values for testnets
            self.values['bitcoin-testnet'] = self.values['bitcoin-mainnet']
            self.values['ethereum-testnet'] = self.values['ethereum-mainnet']
            self.values['cardano-testnet'] = self.values['cardano-mainnet']
            self.values['litecoin-testnet'] = self.values['litecoin-mainnet']
            self.values['dogecoin-testnet'] = self.values['dogecoin-mainnet']
        else:
            raise Exception(f"Invoice: invalid status code {r.status_code}.")

    def getInvoice(self):
        """Return a dictionary of prices with the network as the key and the price as the value."""
        return self.values


if __name__ == "__main__":
    i = Invoice(.50)
    print(i.getInvoice())