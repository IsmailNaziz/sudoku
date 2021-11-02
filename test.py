class Test(object):

	def __init__(self):
		self.count = 0

	def add(self):
		print(count)
		self.count +=1


L = list(range(10))
test = Test()
map(test.add, L)
print(test.count)