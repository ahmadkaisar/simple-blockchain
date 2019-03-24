from .block import *
from .requirement import *
from .transaction import *

class Mine:
	def __init__(self, addr, block, pending_block):
		self.addr = addr
		self.block = block
		self.pending_block = pending_block
	def sequence(self, difficulty, pattern, reward, start=0, step=1):
		pattern = ''.join([pattern for x in range(difficulty)])
		print('[*] mining block using sequence algorithm')
		while True:
			prev_hash = str(self.block.header.prev_hash).encode()
			timestamp = hashlib.sha256((self.block.header.timestamp).encode()).hexdigest().encode()
			nonce = hashlib.sha256(str(start).encode()).hexdigest().encode()
			data_hash = self.block.transactions.hash().encode()
			thash = hashlib.sha256(prev_hash + timestamp + nonce + data_hash).hexdigest()
			if pattern in thash and thash.index(pattern) == 0:
				print('[*] block mined with nonce number', start)
				self.block.header.nonce = start
				self.block.hash = thash
				break
			start += step
		transactions = Transactions()
		transactions.add(Value('', self.addr, reward))
		self.pending_block.transactions = transactions