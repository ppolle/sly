def generate_shortcode(id):
	'''
	Generate urls shortcode
	'''
	import string
	characters = string.digits+string.ascii_uppercase+string.ascii_lowercase
	base = len(characters)
	ret = []

	while id > 0:
		val = id % base
		ret.append(characters[val])
		id = id // base
	
	return "".join(ret[::-1])