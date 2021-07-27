# `crypto_payments`

author: redd

`crypto_payments` includes Python utilities to manage crypto payments across multiple blockchains.

## Supported Networks

### Bitcoin

* `bitcoin-mainnet`

I use [mempool.space](https://mempool.space) for the Bitcoin API. No special configuration is necessary. Note that a payment will be considered valid as soon as the transaction hits the mempool. You do not need to wait for the transaction to be confirmed.

### Cardano

* `cardano-mainnet`
* `cardano-testnet`

I use [blockfrost.io](https://blockfrost.io/) for the Cardano API. To properly use the mainnet or testnet, you must obtain an API key and set a `BLOCKFROST_TOKEN` environment variable whose value is your API key.

## Address Management

To monitor a specific addresses, configure `monitor.json` to include the address, network, and previous balance of that address. For a payment to be considered successful, that balance must increase by `self.payment_thresholds` as defined in `AddressMonitor`. This is a feature I plan on improving to allow for variable payments, denomination in fiat, etc.

Note that I do not own any of the addresses used in these commits. I just randomly selected addresses to use for testing.