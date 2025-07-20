from web3 import Web3
import os
import json
from datetime import datetime

w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_URL')))
account = w3.eth.account.from_key(os.getenv('PRIVATE_KEY'))  # کلید خصوصی امن

def log_event(event_data):
    tx = {
        'from': account.address,
        'to': account.address,
        'value': 0,
        'gas': 200000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': w3.eth.getTransactionCount(account.address),
        'data': json.dumps({'timestamp': str(datetime.utcnow()), 'event': event_data})
    }
    signed_tx = w3.eth.account.sign_transaction(tx, os.getenv('PRIVATE_KEY'))
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash.hex()

if __name__ == '__main__':
    while True:
        event = input("Enter event to log: ")
        tx_hash = log_event(event)
        print(f"Logged with hash: {tx_hash}")
