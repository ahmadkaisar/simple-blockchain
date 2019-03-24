from .requirement import *
from .block import *
from .mine import *

class BlockChain:
	def __init__(self, new_block=None, genesis=b'Genesis Block', pattern='0', difficulty=1):
		self.index = 0
		self.difficulty = difficulty
		self.pattern = self.handlePattern(pattern)
		self.block = new_block if new_block is not None else self.generateGenesis(genesis)
		self.next = None
		self.last_block = self
	def add(self, new_block):
		print('[*] add block')
		if new_block.hash is None:
			print('[*] add block failed')
			return
		temp_blockchain = BlockChain(new_block=new_block, pattern=self.pattern)
		if temp_blockchain.block.header.prev_hash != self.last_block.block.hash:
			print('[*] prev hash in this block is invalid')
			return
		temp_blockchain.index = self.last_block.index + 1
		self.last_block.next = temp_blockchain
		self.last_block = temp_blockchain
		self.last_block.last = self.last_block
		self.last_block.pattern = self.pattern
		blockchain = self.next
		while blockchain.next is not None:
			blockchain.last = self.last_block
			blockchain = blockchain.next
	def backupFile(self):
		path = 'blocks/'
		if not os.path.exists(path):
			print('[*] backup directory not exists')
			print('[*] make new directory')
			os.makedirs(path)
		blockchain = self
		try:
			while True:
				temp = blockchain.block.convert()
				temp['index'] = blockchain.index
				with open(path + str(blockchain.index) + '.json', 'w') as f:
					json.dump(temp, f)
				if blockchain.next is None:
					break
				blockchain = blockchain.next
			with open(path + 'config.json', 'w') as f:
				temp = {'pattern':self.pattern, 'difficulty':self.difficulty}
				json.dump(temp, f)
			print('[*] backup to file successfully completed')
		except:
			print('[*] backup to file failed')
	def convert(self):
		blockchain = self
		result = []
		while True:
			temp = blockchain.block.convert()
			temp['index'] = blockchain.index
			result += [temp]
			if blockchain.next is None:
				break
			blockchain = blockchain.next
		return {
			'pattern':self.pattern,
			'blockchain':result
		}
	def describe(self):
		print('[*] describe blockchain')
		blockchain = self
		while True:
			print(blockchain.block.convert())
			if blockchain.next is None:
				break
			blockchain = blockchain.next
		print('[*] end describe')
	def generateGenesis(self, genesis):
		genesis_transaction = Transactions()
		genesis_transaction.add(Value('', '', genesis))
		genesis_block = Block(genesis_transaction, prev_hash=0)
		Mine(genesis_block).sequence(pattern=self.pattern, difficulty=self.difficulty)
		return genesis_block
	def getIndex(self, index=0):
		blockchain = self
		while index > blockchain.index:
			if blockchain.next is None:
				return {'block':None}
			blockchain = blockchain.next
		return {'block':blockchain.block.convert()}
	def getFrom(self, index=0):
		blockchain = self
		while index > blockchain.index:
			if blockchain.next is None:
				return {'pattern':self.pattern, 'blockchain':None}
			blockchain = blockchain.next
		return blockchain.convert()
	def handlePattern(self, pattern):
		pattern = pattern.lower()
		pattern = ''.join([x for x in pattern if (x >= 'a' and x <= 'f') or (x >= '0' and x <= '9')])
		pattern = pattern if len(pattern) > 0 else '0'
		print('[*] accepted pattern', pattern)
		return pattern
	def recoverBackupFile(self, path='blocks/'):
		index = 0
		blockchain = None
		try:
			with open(path + 'config.json', 'r') as f:
				difficulty = json.loads(f.read())['difficulty']
				pattern = json.loads(f.read())['pattern']
		except:
			difficulty = self.difficulty
			pattern = self.pattern
		print('[*] recovering blockchain from file....')
		while True:
			try:
				print('[*] recovering block', str(index))
				with open(path + str(index) + '.json', 'r') as f:
					data_block = json.loads(f.read())
					if blockchain is None:
						blockchain = BlockChain()
						blockchain.block.decodeJson(data_block)
					else:
						block = Block()
						block.decodeJson(data_block)
						blockchain.add(block)
					index += 1
				print('[*] block', str(index - 1), 'recovered')
			except:
				print('[*] block', str(index), 'not found')
				break
		print('[*] recovering blockchain completed')
		if blockchain is None:
			return BlockChain()
		return blockchain
	def validate(self):
		blockchain = self
		while blockchain.next is not None:
			if blockchain.block.hash != blockchain.next.block.header.prev_hash:
				blockchain.next = None
				return (False, self.index, self.last_block.index)
			blockchain = blockchain.next
		return (True, self.index, self.last_block.index)