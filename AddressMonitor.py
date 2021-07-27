import json
from BitcoinApi import BitcoinApi
from CardanoApi import CardanoApi

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
            elif a['network'] == "cardano-mainnet":
                # self.addr_apis.append(CardanoApi(a))
                pass
            elif a['network'] == "cardano-testnet":
                self.addr_apis.append(CardanoApi(a))
            else:
                raise Exception("Unsupported Network")

        self.payment_thresholds = {
            'bitcoin-mainnet' : 2000,
            'cardano_mainnet' : 10000,
            'cardano_testnet' : 10000
        }


    def _saveAddrInfo(self):
        d = []
        for api in self.addr_apis:
            d.append(api.getAddrInfo())
        j = json.dumps(d)

        with open(self.fname,'w') as f:
            f.write(j)


    def checkForPayment(self):

        success = False

        for api in self.addr_apis:
            complete, chg = api.checkForPayment()
            print(f"{complete} {chg} ({api.network} {api.addr})")
            if complete:
                success = True
                break
        self._saveAddrInfo()

        return success


if __name__ == '__main__':
    fname = 'monitor.json'
    am = AddressMonitor(fname)
    am.checkForPayment()

