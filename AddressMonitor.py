#
# A class that can be used to monitor the balances of several crypto addresses across multiple blockchains.
#
# Author: redd
#

from Api import BitcoinApi, CardanoApi, EthereumApi
from Invoice import Invoice
import json

class AddressMonitor:

    def __init__(self, fname):
        self.fname = fname
        self.addr_apis = [] # all monitored addresses
        self.next_apis = {} # only next addresses

        self._updateNextApis() # the addresses to check for transactions

    def _populateAddrApis(self):
        with open(self.fname,'r') as f:
            s = f.read()
        d = json.loads(s)

        for a in d:
            if a['network'] == "bitcoin-mainnet":
                self.addr_apis.append(BitcoinApi(a))
            elif a['network'] == "ethereum-mainnet":
                self.addr_apis.append(EthereumApi(a))
            # elif a['network'] == "cardano-mainnet":
            #     # self.addr_apis.append(CardanoApi(a))
            #     pass
            elif a['network'] == "cardano-testnet":
                self.addr_apis.append(CardanoApi(a))
            else:
                raise Exception(f"Unsupported Network: {a['network']}")

    def _saveAddrInfo(self):
        d = []
        for api in self.addr_apis:
            d.append(api.getAddrInfo())
        j = json.dumps(d, indent=4)

        with open(self.fname,'w') as f:
            f.write(j)

    def _updateNextApis(self):
        """
        Returns a dictionary.
            Keys are the networks found in monitor.json
            Values of the address in that network with the lowest balance.
        This can be helpful to reduce/prevent address reuse.
        """
        self._populateAddrApis()
        na = {}
        for addrapi in self.addr_apis:
            if addrapi.network in na.keys():
                if addrapi.prev_qty < na[addrapi.network].prev_qty:
                    na[addrapi.network] = addrapi
            else:
                na[addrapi.network] = addrapi
        self.next_apis = na
        return na

    def getNextApis(self):
        """
        Get the address that AddressMonitor will check on each network for payment.
        Returns a dictionary.
            Keys are the networks found in monitor.json
            Values of the address in that network with the lowest balance.
        """
        return self.next_apis

    def checkForPayment(self, invoice=None):
        """
        Checks the addresses in self.next_apis for changes in balance.
        Returns True if a payment was received.
        The threshold for True can be changed by using an Invoice() object
        """
        # get prices denominated in crypto
        if invoice == None:
            invoice = Invoice() # use smallest possible values for threshold
        prices = invoice.getInvoice() # dictionary of the prices

        success = False # indicates if a transaction has been successful        
        for n in self.next_apis: # check each network for payment
            api = self.next_apis[n]
            print(f"Checking {api.network} for payment...")
            complete, chg = api.checkForPayment(prices[api.network])
            print(f"  {'Success!' if complete else 'Failure'} {chg}/{prices[api.network]} ({api.addr})")
            if complete:
                success = True
                break
        
        self._saveAddrInfo() # save the new state
        self._updateNextApis() # update to use new addresses

        return success


if __name__ == '__main__':

    fname = 'monitor.json'
    am = AddressMonitor(fname)
    na = am.getNextApis()
    
    print(f"Active Addresses")
    for n in na:
        print(f"{na[n].network} {na[n].addr}")

    print (f"Checking for Payment")
    fname = 'monitor.json' # contains json object with addresses to monitor
    invoice = Invoice(0.50) # Create an invoice for 50 cents
    am = AddressMonitor(fname)
    rx = am.checkForPayment(invoice) # check for payments
    msg = "Payment received! :)" if rx else "Payment not received. :("
    print(msg)