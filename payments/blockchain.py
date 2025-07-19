from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_KEY'))

def mint_nft(user_wallet, video_hash, contract_address, contract_abi):
    """ایجاد NFT برای ویدئو"""
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    txn = contract.functions.mintNFT(user_wallet, video_hash).buildTransaction({
        'from': user_wallet,
        'nonce': w3.eth.get_transaction_count(user_wallet)
    })
    return txn
