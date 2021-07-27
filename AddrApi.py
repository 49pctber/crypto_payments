#
# A base class used to check for a payment.
#
# Must inherit self._checkBalance(). This varies for each blockchain, so look at BitcoinApi or CardanoApi for how to implement functioning classes.
#
# Author: redd
#

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