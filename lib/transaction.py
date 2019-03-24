from .requirement import *

class Value:
	def __init__(self, fromAddress=b'', toAddress=b'', value=b''):
		self.fromAddress = str(fromAddress)
		self.toAddress = str(toAddress)
		self.value = str(value)
	def convert(self):
		return {
			'fromAddress':self.fromAddress,
			'toAddress':self.toAddress,
			'value':self.value
		}
	def hash(self):
		return hashlib.sha256(self.fromAddress.encode() + self.toAddress.encode() + self.value.encode()).hexdigest()

class Transaction:
	def __init__(self, timestamp=str(datetime.datetime.utcnow()), value=Value()):
		self.timestamp = timestamp
		self.value = value
	def convert(self):
		return {
			'transaction':self.value.convert(),
			'timestamp':self.timestamp
		}
	def hash(self):
		return hashlib.sha256(self.timestamp.encode() + self.value.hash().encode()).hexdigest()

class Transactions:
	def __init__(self, transaction=None):
		self.transaction = transaction
		self.last = self
		self.next = None
	def add(self, transaction):
		print('[*] add new transaction....')
		if self.transaction is None:
			self.transaction = transaction
			return
		self.last.next = Transactions(transaction)
		self.last = self.last.next.last
		transactions = self
		while transactions is not None:
			transactions.last = self.last
			transactions = transactions.next
	def convert(self):
		res = []
		if self.transaction is None:
			return []
		transactions = self
		while transactions is not None:
			res += [
				transactions.transaction.convert()]
			transactions = transactions.next
		return res
	def hash(self):
		transactions = self
		thash = []
		while transactions is not None:
			thash += [transactions.transaction.hash()]
			transactions = transactions.next
		thash = list(sorted(thash))
		while float(int(math.log2(len(thash)))) != math.log2(len(thash)):
			thash += [thash[-1]]
		while len(thash) > 1:
			temp = []
			for i in range(0, len(thash), 2):
				temp += [hashlib.sha256(thash[i].encode() + thash[i + 1].encode()).hexdigest()]
			thash = temp
		return thash[0]