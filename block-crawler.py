import sys
import sqlite3
import logging
import re
from web3 import Web3, HTTPProvider

# Validates input parameters for cases where retrieving transactions will not properly function
# Parameters: endpoint - JSON-RPC endpoint to interact with Ethereum client
#             start_block - starting block number 
#             end_block -  ending block number 
def validate_input(endpoint, start_block, end_block):
    if not isinstance(start_block, int) or not isinstance(end_block, int):
        raise ValueError("start_block and end_block must be integers")
    if start_block < 0 or end_block < 0:
        raise ValueError("start_block and end_block must be positive integers")
    if end_block < start_block:
        raise ValueError("end_block must be greater than or equal to start_block")
    if not re.match(r'^https?://.*$', endpoint):
        raise ValueError("Invalid endpoint URL")


# Retrieves Ethereum Mainnet transactions within a start_block and end_block range and persists them to SQLite database
# Parameters: endpoint - JSON-RPC endpoint to interact with Ethereum client
#             start_block - starting block number 
#             end_block -  ending block number 
def retrieve_transactions(endpoint, start_block, end_block):
    web3 = Web3(HTTPProvider(endpoint))
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    
    # Creates connection to SQLite DB named 'db.sqlite3'
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # Creates 'blocks' table, if it doesn't already exist
    c.execute('''CREATE TABLE IF NOT EXISTS blocks (
        hash TEXT PRIMARY KEY, 
        number TEXT, 
        timestamp INTEGER)
        ''')

    # Creates 'transactions' table, if it doesn't already exist
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        hash TEXT PRIMARY KEY, 
        blockHash TEXT, 
        blockNumber TEXT, 
        sender TEXT, 
        receiver TEXT, 
        value INTEGER)
        ''')

    # Iterates through each block in the specified range
    for block_number in range(start_block, end_block + 1):
        try:
            # Retrieve block data from Ethereum node
            block = web3.eth.get_block(hex(block_number), True)

            # Extract block hash, number, and timestamp, and insert into 'blocks' table in SQLite DB
            block_data = (block.hash.hex(), block.number, block.timestamp)
            c.execute("INSERT INTO blocks (hash, number, timestamp) VALUES (?, ?, ?)", block_data)

            # Iterate through each transaction within a certain block
            for tx in block.transactions:

                # Extract transaction hash, its respective block hash, block number, sender, receiver, and value of Ethereum (Wei converted into Ether), 
                # and insert into 'transactions' table into SQLite DB
                tx_data = (tx.hash.hex(), tx.blockHash.hex(), tx.blockNumber, tx['from'], tx['to'], tx['value']/10**18) 
                c.execute("INSERT INTO transactions (hash, blockHash, blockNumber, sender, receiver, value) VALUES (?, ?, ?, ?, ?, ?)", tx_data)

        # Catch exceptions with processing block data and log errors into external logging file for later reference
        except Exception as e:
            print(f"Error processing block {block_number}: {e}")
            logging.error(f"Error processing block {block_number}: {e}")
            continue

    # Commit and close connection to SQLite database 
    conn.commit()
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python block-crawler <endpoint> <sqlite_file> <block_range>")
        sys.exit(1)

    # Process command line inputs for retrieve_transactions function
    endpoint = sys.argv[1]
    sqlite_file = sys.argv[2]
    block_range = sys.argv[3]

    start_block, end_block = map(int, block_range.split('-'))

    validate_input(endpoint, start_block, end_block)
    retrieve_transactions(endpoint, start_block, end_block)