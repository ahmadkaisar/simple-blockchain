from .requirement import *
from .transaction import *

class Header:
	def __init__(self, prev_hash):
		self.prev_hash = prev_hash
		self.timestamp = str(datetime.datetime.utcnow())
		self.nonce = 0
	def convert(self):
		return {
			'prev_hash':self.prev_hash,
			'timestamp':self.timestamp,
			'nonce':self.nonce
		}

class Block:
	def __init__(self, transaction, prev_hash=0):
		self.header = Header(prev_hash)
		self.transaction = transaction
		self.hash = None
	def convert(self):
		return {
			'header':self.header.convert(),
			'transaction':self.transaction.convert(),
			'hash':self.hash
		}
	def sequenceMine(self, start, step, pattern):
		print('[*] mine lastest transaction')
		nonce = self.header.nonce
		while True:
			prev_hash = str(self.header.prev_hash).encode()
			timestamp = hashlib.sha256(self.header.timestamp.encode()).hexdigest().encode()
			tnonce = hashlib.sha256(str(nonce).encode()).hexdigest().encode()
			transaction = self.transaction.hash().encode()
			thash = hashlib.sha256(prev_hash + timestamp + tnonce + transaction).hexdigest()
			if pattern in thash:
				self.hash = thash
				self.header.nonce = nonce
				print('[*] mining success')
				break
			nonce += 1