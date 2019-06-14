import string

def encode(self, id):
	'''shorten a url link'''
	
	characters = string.digits+string.uppercase+string.lowercase
	base = len(characters)
	ret = []

	while id > 0:
		val = id % base
		ret.append(charcaters[val])
		id = id // base
	
	return "".join(ret[::-1])