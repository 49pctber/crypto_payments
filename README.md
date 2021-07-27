# `crypto_payments`

author: redd

`crypto_payments` includes Python utilities to manage crypto payments across multiple blockchains.

## Supported Networks

### Bitcoin

* `bitcoin-mainnet`

I use [mempool.space](https://mempool.space) for the Bitcoin API. No special configuration is necessary. Note that a payment will be considered valid as soon as the transaction hits the mempool. You do not need to wait for the transaction to be confirmed.

### Ethereum

* `ethereum-mainnet`

I use [etherscan.io](https://etherscan.io) for the Ethereum API. You must obtain an API key after making an account. Once you have an account, go to the [My API Keys](https://etherscan.io/myapikey) page. Set your `ETHERSCAN_TOKEN` environment variable to your API key.

### Cardano

* `cardano-mainnet`
* `cardano-testnet`

I use [blockfrost.io](https://blockfrost.io/) for the Cardano API. To properly use the mainnet or testnet, you must obtain an API key and set a `BLOCKFROST_TOKEN` environment variable whose value is your API key.

## Address Management

To monitor a specific addresses, configure `monitor.json` to include the address, network, and previous balance of each address. For a payment to be considered successful, that balance must increase by the amount specified by your Invoice (if none is specified, any positive change will trigger a successful payment). If there are multiple addresses for the same network, this will only check for the address with the lowest balance. (Ideally you only monitor addresses that haven't been used previously). This reduces the number of API calls, and also reduces address reuse. If you want to see which address will be checked (like to display a QR code to a user), use `AddressMonitor.getNextApis()`.

Note that I do not own any of the addresses used in these commits. I just randomly selected addresses to use for testing.
