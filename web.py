from flask import Flask, request, jsonify
from lib import *
from function import *
import _thread

app = Flask(__name__)

########### Used Variable ###############
blockchain = None
known = []
maximum = 4
mining = None
pending_block = None
point = 0
position = 'master'
reward = 2
timeout = 10
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
		'prev_hash':pending_block.header.prev_hash,
		'timestamp':pending_block.header.timestamp,
		'nonce':None,
		'hash':pending_block.transaction.hash(),
		'pattern':blockchain.pattern
	})

@app.route('/blocks/pending/approve', methods=['GET'])
def blocksPendingApprove():
	global blockchain
	global pending_block
	global reward
	try:
		if position == 'master' and pending_block is not None:
			pending_block.header.nonce = request.form['nonce']
			blockchain.add(pending_block)
			pending_block = None
			reward = reward / 2
			return jsonify({'reward':reward})
	except:
		return jsonify({'reward':0})

@app.route('/index/last', methods=['GET'])
def indexLast():
	return jsonify({'index':blockchain.last_block.index})

@app.route('/point', methods=['GET'])
def point():
	if position == 'master':
		return jsonify({'point':point})
	return jsonify({'point':0})

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

def getReward():
	global point
	while True:
		if pending_block is not None:
			if pending_block.header.nonce is not None:
				for addr in known:
					resp = requestPost(addr + '/blocks/pending/approve', {'nonce':pending_block.header.nonce})
					if resp is None:
						continue
					resp = json.loads(resp)
					if resp['reward'] > 0:
						print('[*] block accepted')
						print('[*] get reward', resp['reward'])
						point += resp['reward']
						break

def masterProcess():
	createPendingBlock()

def masterServantProcess(t):
	while True:
		if position == 'master':
			masterProcess()
		else:
			servantProcess()
		time.sleep(t)

def readArgs(args):
	global known
	global maximum
	global port
	global timeout
	index = 1
	maximum = 4
	port = 1102
	timeout = 10
	while index < len(args):
		if '--port' == args[index]:
			try:
				port = int(args[index + 1])
				index += 1
			except:
				print('[*] port must be integer / number')
				exit()
		elif '--full-node-server-list' == args[index]:
			try:
				with open(args[index + 1], 'r') as f:
					known = f.read()
					known = known.split('\n')
					known = [x for x in known if len(x) > 0]
				index += 1
			except:
				print('[*] fail to open file')
				print('[*] example file:')
				print('http://123.234.45.6:1234')
				print('http://234.345.56.7:2345')
				print('http://345.456.65.8:3456')
				exit()
		elif '--maximum-node' == args[index]:
			try:
				maximum = int(args[index + 1])
				index += 1
			except:
				print('[*] maximum node must be integer / number')
				exit()
		elif '--sequence-method' == args[index]:
			try:
				start = int(args[index + 1])
				step = int(args[index + 2])
				index += 2
			except:
				print('[*] start / stop must be integer / number without (\'<\') and (\'>\')')
				exit()
		elif '--timeout' == args[index]:
			try:
				timeout = int(args[index + 1])
				index += 1
			except:
				print('[*] timeout must be integer / number')
		elif '--help':
			print('Usage:')
			print('--help', '\t\t\t\t\tshow this help')
			print('--full-node-server-list', '\t\tread all known full node server')
			print('--maximum-node', '\t\t\t\tmaximum node that can connect to this server (default=4)')
			print('--sequence-method <start> <step>', '\tuse sequence number to mine pending transaction from start with auto increment step (default=None)')
			print('--port', '\t\t\t\t\tset port for server (default=1102)')
			print('--timeout', '\t\t\t\tset timeout for each request (default=10)')
			print('Example:')
			print('-', args[0])
			print('-', args[0], '--port', '1234')
			print('-', args[0], '--full-node-server-list', 'list.txt')
			print('-', args[0], '--port', '1234', '--full-node-server-list', 'list.txt')
			exit()
		index += 1

def requestGet(url, params={}):
	try:
		query_string = urllib.parse.urlencode(params)
		if len(query_string) > 0:
			url = url + '?' + query_string
		with urllib.request.urlopen(url) as response:    
		    response_text = response.read().decode()
	except:
		return None
	return response_text

def requestPost(url, params):
	global timeout
	query_string = urllib.parse.urlencode(params)
	data = query_string.encode( "ascii" )
	try:
		with urllib.request.urlopen(url, data, timeout=timeout) as response:
		    response_text = response.read()
	except:
		return None
	return response_text

def sequenceMining(block, pattern, start=0, step=1):
	nonce = start
	print('[*] mining pending block....')
	while block is not None or block.header.nonce is None:
		prev_hash = block.header.prev_hash.encode()
		timestamp = hashlib.sha256(block.header.timestamp.encode()).hexdigest().encode()
		nonce = hashlib.sha256(str(nonce).encode()).hexdigest().encode()
		thash = hashlib.sha256(prev_hash + timestamp + nonce + block.hash.encode()).hexdigest()
		if pattern in thash:
			print('[*] success')
			block.header.nonce = nonce
			break
		nonce += step
	print('[*] mining pending block aborted')

def servantProcess():
	_thread.start_new_thread(syncMaster, ())
	_thread.start_new_thread(syncBlockChain, ())
	_thread.start_new_thread(syncPendingBlock, ())
	_thread.start_new_thread(syncPoint, ())
	_thread.start_new_thread(getReward, ())

def syncBlockChain():
	global blockchain
	for addr in known:
		resp = json.loads(requestGet(addr + '/blocks/index/' + blockchain.last_block.index))
		if resp['hash'] == blockchain.last_block.block.hash:
			resp = json.loads(requestGet(addr + '/blocks/from' + blockchain.last_block.index))
			if resp is not None:
				pass

def syncMaster():
	global position
	master = None
	for addr in known:
		resp = json.loads(requestGet(addr + '/position'))
		if resp['position'] == 'master':
			if position == 'master' and resp['timeup'] < timeup:
				print('[*] position dropped')
				position = 'local'
			break
		elif resp['position'] == 'local':
			pass

def syncPoint():
	global point
	for addr in known:
		temp = json.loads(requestGet(addr + '/point'))['point']
		if temp > 0:
			point = temp

def syncPendingBlock():
	global pending_block
	for addr in known:
		resp = requestGet(addr + '/blocks/pending')
		if resp is not None:
			break
	if resp is None:
		pending_block = None
		return
	resp = json.loads(resp)
	if pending_block is None or resp['timestamp'] > pending_block.header.timestamp:
		pending_block = None
		time.sleep(10)
		pending_block = Block()
		pending_block.header.prev_hash = resp['prev_hash']
		pending_block.header.timestamp = resp['timestamp']
		pending_block.header.nonce = resp['nonce']
		pending_block.header.hash = resp['hash']

readArgs(sys.argv)
blockchain = BlockChain().recoverBackup()
_thread.start_new_thread(masterServantProcess, (timeout,))
app.run(host='0.0.0.0', port=port)