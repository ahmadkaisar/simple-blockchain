import _thread
from lib import *
from flask import Flask, request, jsonify

app = Flask(__name__)

blockchain = BlockChain(difficulty=4, pattern='1')
transactions = Transactions()

@app.route('/blocks', methods=['GET'])
def blocks():
	return jsonify(blockchain.convert())

@app.route('/balance/<id>', methods=['GET'])
def balance(id):
	return jsonify(blockchain.getBalance(id))

@app.route('/transactions', methods=['GET'])
def transactionsShow():
	return jsonify(transactions.convert())

@app.route('/reward', methods=['GET'])
def rewardShow():
	return jsonify(blockchain.reward)

@app.route('/transactions/new', methods=['POST'])
def transactionsNew():
	fromAddress = request.form['fromAddress']
	toAddress = request.form['toAddress']
	value = request.form['value']
	transaction = Transaction(value=Value(fromAddress=fromAddress, toAddress=toAddress, value=value.encode()))
	transactions.add(transaction)
	return transactionsShow()

def mineEvery(t=30):
	global blockchain
	global transactions
	pending_block = None
	while True:
		print('[*] checking pending block every', t, 's')
		if pending_block is None and len(transactions.convert()) > 0:
			pending_block = Block(prev_hash=blockchain.last_block.block.hash, transactions=transactions)
			transactions = Transactions()
			Mine('addr1', pending_block, transactions).sequence(difficulty=blockchain.difficulty, pattern=blockchain.pattern, reward=blockchain.mining_reward)
			blockchain.add(pending_block)
			pending_block = None
		else:
			print('[*] no block to mine')
		time.sleep(t)

_thread.start_new_thread(mineEvery, ())
app.run(host='0.0.0.0', port=1234)