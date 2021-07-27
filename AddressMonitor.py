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
        with open(self.fname,'r') as f:
            s = f.read()
        d = json.loads(s)

        self.addr_apis = []

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
                raise Exception("Unsupported Network")


    def _saveAddrInfo(self):
        d = []
        for api in self.addr_apis:
            d.append(api.getAddrInfo())
        j = json.dumps(d)

        with open(self.fname,'w') as f:
            f.write(j)


    def checkForPayment(self, invoice=None):

        success = False

        # get prices denominated in crypto
        if invoice == None:
            invoice = Invoice() # use smallest possible values for threshold
        price = invoice.getInvoice() # dictionary of the prices

        for api in self.addr_apis: # check each network for payment
            print(f"Checking {api.network} for payment...")
            complete, chg = api.checkForPayment(price[api.network])
            print(f"  {'Success!' if complete else 'Failure'} {chg}/{price[api.network]} ({api.addr})")
            if complete:
                success = True
                break
        self._saveAddrInfo()

        return success


if __name__ == '__main__':

    fname = 'monitor.json' # contains json object with addresses to monitor
    invoice = Invoice(0.50) # Create an invoice for 50 cents
    am = AddressMonitor(fname)
    rx = am.checkForPayment(invoice) # check for payments
    msg = "Payment received! :)" if rx else "Payment not received. :("
    print(msg)