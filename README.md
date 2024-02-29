# Block-Crawler Mini-Project

This python program retrieves Ethereum Mainnet transactions within a given block range and persists them to a SQLite database.

# Program Structure

Program will take your command line inputs and process them through the main block of code, which will then validate them to ensure that retrieving Ethereum block data is possible with the given information.
It will validate if the start and end blocks are integers that are both greater than 0, the end block value is greater than that of the start block, and that the given HTTP endpoint is a valid endpoint that can be accessed. 
Once the inputs are validated, it will retrieve transactions from the given endpoint and create 'blocks' and 'transactions' tables in SQLite Database to insert data for querying.

# Usage

It takes in three command line inputs: a JSON-RPC endpoint to call an Ethereum client, the path to the SQLite file to write to, and a range of blocks to retrieve data from.
The command line input will be in this format: python3 block-crawler.py https://rpc.quicknode.pro/key db.sqlite3 200-300

# Error Handling and Logging 

With errors in command line input, the program will stop and raise an error immediately to prevent code from continuing with potentially incorrect data.
With errors in processing block data, the block number and error will be recorded in a logging file in directory to go back to for later reference, however, the program will still finish.
