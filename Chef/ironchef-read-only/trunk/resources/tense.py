def get_past_tense(s):
	class detensor:
		def __init__(self):
			print "hey"
		def _t_y(self, word):
			return word[:-1] + "ies"
		
		def _t_e(self, word):
			return word + "d"
		
		def _t_n(self, word):
			return word + "ned"
		
		def _t_ch(self, word):
			return word + "ed"
		
		def _t_x(self, word):
			return word + "en"
		
	
	d = detensor()
	pre = "_t_"
	
	e = pre + s[-1:]
	if hasattr(d, e):
		return getattr(d, e)(s)
	
	e = pre + s[-2:]
	if hasattr(d, e):
		return getattr(d, e)(s)
	
	e = pre + s[-3:]
	if hasattr(d, e):
		return getattr(d, e)(s)
	
	raise Exception("Unknown ending")
	
print get_past_tense("baby")
print get_past_tense("fatten")