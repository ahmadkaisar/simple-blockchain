from .requirement import *

class Mine:
	def __init__(self, block):
		self.block = block
	def sequence(self, pattern, start=0, step=1):
		print('[*] mining using sequence')
		while True:
			prev_hash = str(self.block.header.prev_hash).encode()
			timestamp = hashlib.sha256((self.block.header.timestamp).encode()).hexdigest().encode()
			nonce = hashlib.sha256(str(start).encode()).hexdigest().encode()
			data_hash = self.block.transaction.hash().encode()
			thash = hashlib.sha256(prev_hash + timestamp + nonce + data_hash).hexdigest()
			if pattern in thash:
				print('[*] nonce found', start)
				self.block.header.nonce = start
				break
			start += step