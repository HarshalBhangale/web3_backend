import json 

from script import parse_unstructured_text

examples = {
    # Send
    "send": [
        {"input": "Send 100 USD to John.", "output": {"action": "send", "units": "100", "from": "USD", "to": "USD", "receiver_id": "John"}},
        {"input": "Transfer 50 EUR to Alice.", "output": {"action": "send", "units": "50", "from": "EUR", "to": "EUR", "receiver_id": "Alice"}},
        {"input": "Send 50 EUR to my friend Sarah.", "output": {"action": "send", "units": "50", "from": "EUR", "to": "EUR", "receiver_id": "Sarah"}},
        {"input": "Transfer 2000 INR to mom.", "output": {"action": "send", "units": "2000", "from": "INR", "to": "INR", "receiver_id": "mom"}},
    ],

    # Swap
    "swap": [
        {"input": "Swap 0.1 BTC to ETH.", "output": {"action": "swap", "units": "0.1", "source": "BTC", "dest": "ETH"}},
        {"input": "Exchange 5 LTC for BCH.", "output": {"action": "swap", "units": "5", "source": "LTC", "dest": "BCH"}},
        {"input": "Swap 0.5 ETH for ADA tokens.", "output": {"action": "swap", "units": "0.5", "source": "ETH", "dest": "ADA"}},
        {"input": "Exchange 10 LTC to BTC.", "output": {"action": "swap", "units": "10", "source": "LTC", "dest": "BTC"}},
    ],

    # Stake
    "stake": [
        {"input": "Stake 1000 ADA in Cardano.", "output": {"action": "stake", "units": "1000", "source": "ADA", "chain": "Cardano"}},
        {"input": "Lock 500 DOT in Polkadot.", "output": {"action": "stake", "units": "500", "source": "DOT", "chain": "Polkadot"}},
        {"input": "Stake 500 DOT in Polkadot parachain.", "output": {"action": "stake", "units": "500", "source": "DOT", "chain": "Polkadot"}},
        {"input": "Lock 1000 SOL in Solana staking pool.", "output": {"action": "stake", "units": "1000", "source": "SOL", "chain": "Solana"}},
    ],

    # Borrow
    "borrow": [
        {"input": "Borrow 2000 USDT in Compound.", "output": {"action": "borrow", "units": "2000", "source": "USDT", "source_address": "Compound"}},
        {"input": "Take a loan of 1000 DAI from Aave.", "output": {"action": "borrow", "units": "1000", "source": "DAI", "source_address": "Aave"}},
        # todo: these two cases need revisit
        {"input": "Borrow 5000 USDC from Aave lending platform.", "output": {"action": "borrow", "units": "5000", "source": "USDC", "source_address": "Aave"}},
        {"input": "Take a loan of 10000 BUSD from Compound Finance.", "output": {"action": "borrow", "units": "10000", "source": "BUSD", "source_address": "Compound"}},
    ],

    # Lend
    "lend": [
        {"input": "Lend 3000 USDC to Bob.", "output": {"action": "lend", "units": "3000", "source": "USDC", "dest_address": "Bob", "duration_in_days": None}},
        {"input": "Provide a loan of 500 BTC to Carol.", "output": {"action": "lend", "units": "500", "source": "BTC", "dest_address": "Carol", "duration_in_days": None}},
        {"input": "Lend 2000 DAI to Alice for 30 days.", "output": {"action": "lend", "units": "2000", "source": "DAI", "dest_address": "Alice", "duration_in_days": "30"}},
        {"input": "Provide a loan of 10000 USDT to Bob with interest.", "output": {"action": "lend", "units": "10000", "source": "USDT", "dest_address": "Bob", "duration_in_days": "30"}},
    ],

    # Information on NFT
    "information_on_nft": [
        {"input": "Tell me about the CryptoPunks NFT on Ethereum.", "output": {"action": "information_on_nft", "nft_name": "CryptoPunks", "chain": "Ethereum"}},
        {"input": "Get details on the Art Blocks NFT on Polygon.", "output": {"action": "information_on_nft", "nft_name": "Art Blocks", "chain": "Polygon"}},
        {"input": "Tell me about the Bored Ape Yacht Club NFT on Ethereum.", "output": {"action": "information_on_nft", "nft_name": "Bored Ape Yacht Club", "chain": "Ethereum"}},
        {"input": "Get details on the Decentraland NFT on MANA blockchain.", "output": {"action": "information_on_nft", "nft_name": "Decentraland", "chain": "MANA"}},
    ],

    # Information on Stock Markets
    "information_on_stock_markets": [
        {"input": "What's the stock market data for AMZN on NASDAQ?", "output": {"action": "information_on_stock_markets", "ticker": "AMZN", "market": "NASDAQ"}},
        {"input": "Tell me about GOOGL in NYSE.", "output": {"action": "information_on_stock_markets", "ticker": "GOOGL", "market": "NYSE"}},
        {"input": "Whats the current price of TATA MOTORS on BSE", "output": {"action": "information_on_stock_markets", "ticker": "TATA MOTORS", "market": "BSE"}},
    ],

    # Information on Crypto Markets
    "information_on_crypto_markets": [
        {"input": "Give me details on ETH/BTC on Kraken.", "output": {"action": "information_on_crypto_markets", "crypto_pair": "ETH/BTC", "exchange": "Kraken"}},
        {"input": "What's the data on XRP/USD on Coinbase Pro?", "output": {"action": "information_on_crypto_markets", "crypto_pair": "XRP/USD", "exchange": "Coinbase Pro"}},
    ],

    # Buy NFT
    "buy_nft": [
        {"input": "Buy the unique CryptoPunks NFT on Ethereum.", "output": {"action": "buy_nft", "nft_name": "CryptoPunks", "chain": "Ethereum"}},
        {"input": "Purchase the rare CryptoKitties NFT on Binance Smart Chain.", "output": {"action": "buy_nft", "nft_name": "CryptoKitties", "chain": "Binance Smart Chain"}},
    ],

    # View Portfolio
    "view_portfolio": [
        {"input": "Show me the portfolio for 0x23786423 on polychain.", "output": {'action': 'view_portfolio', 'chain_address': '0x23786423', 'chain': 'polychain'}},
        {"input": "Display the portfolio for 0x23786423 in Coinbase.", "output": {'action': 'view_portfolio', 'chain_address': '0x23786423', 'chain': 'Coinbase'}},
    ]
}

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("keyword", choices=examples.keys(), help="Specify a keyword from the list of keys present in examples")
args = parser.parse_args()

keyword = args.keyword

for ind, interaction in enumerate(examples[keyword]):
    prompt = interaction['input']
    expected_response = interaction['output']
    actual_response = parse_unstructured_text(prompt)['output'].replace('Response:', '').strip()
    actual_response = json.loads(actual_response)

    print(prompt, 'ok' if expected_response == actual_response else ('failed', actual_response))
    # import pdb; pdb.set_trace()