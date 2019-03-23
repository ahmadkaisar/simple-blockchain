from flask import Flask, request, jsonify
from lib import *
import _thread

app = Flask(__name__)

########### Used Variable ###############
blockchain = BlockChain().recoverBackup()
known = []
pending_block = None
position = 'master'
timeup = str(datetime.datetime.utcnow())
transaction = Transaction()
#########################################

@app.route('/blocks', methods=['GET'])
def blocks():
	return jsonify(blockchain.convert())

@app.route('/blocks/index/<int:index>', methods=['GET'])
def blocksIndex(index):
	return jsonify(blockchain.getIndex(index))

@app.route('/blocks/from/<int:index>', methods=['GET'])
def blocksFrom(index):
	return jsonify(blockchain.getFrom(index))

@app.route('/blocks/last', methods=['GET'])
def blocksLast():
	return jsonify(blockchain.last_block.convert())

@app.route('/blocks/pending', methods=['GET'])
def blocksPending():
	if pending_block is None:
		return jsonify({
			'prev_hash':None,
			'timestamp':None,
			'nonce':None,
			'hash':None,
			'pattern':None
			})
	return jsonify({
		'prev_hash':blockchain.last_block.block.hash,
		'timestamp':pending_block.header.timestamp,
		'nonce':pending_block.header.nonce,
		'hash':pending_block.transaction.hash,
		'pattern':blockchain.pattern
	})

@app.route('/index/last', methods=['GET'])
def indexLast():
	return jsonify({'index':blockchain.last_block.index})

@app.route('/transaction', methods=['GET'])
def transactionShow():
	return jsonify({'transaction':transaction.convert()})

@app.route('/transaction/new', methods=['POST'])
def transactionNew():
	global transaction
	transaction.add(request.form['transaction'].encode())
	return transactionShow()

def createPendingBlock():
	global pending_block
	global transaction
	print('[*] creating pending block to be mined')
	if pending_block is None and len(transaction.transaction) > 0:
		pending_block = Block(transaction)
		transaction = Transaction()
		pending_block.header.prev_hash = blockchain.last_block.block.hash
		print('[*] pending block created')
	elif len(transaction.transaction) < 1:
		print('[*] empty transaction')
	else:
		print('[*] fail to create pending block')

def masterProcess():
	createPendingBlock()

def masterServantProcess(t):
	while True:
		if position == 'master':
			masterProcess()
		else:
			servantProcess()
		time.sleep(t)

def servantProcess():
	_thread.start_new_thread(syncBlockChain, ())
	_thread.start_new_thread(syncPendingBlock, ())

def syncBlockChain():
	pass

def syncPendingBlock():
	pass

_thread.start_new_thread(masterServantProcess, (10,))
app.run(host='0.0.0.0', port=1234)