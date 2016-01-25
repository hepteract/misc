# PyCFG

def d(str):
	#raw_input(str)
	pass

class CFG:
	"""This is an attempt to incorporate straight CFG into a Pythonic regular-expression style.

Example usage:
>>> chef = CFG()
Done.

This sets the main layout of the Chef file. Notice that keywords are encased by {}
	and * means '0 or more' and ? means 'optional' (potentially none, but at most one).
  The + operator indicates '1 or more'.
  To group expressions (eg to get one or more 'Hello's) one would use parentheses: (Hello)+
	(The master can also be set directly through the constructor.)
	All symbols can be escaped as normal using a backslash.
>>> chef.define('{Recipe}\n\n?({Serves}\n\n){Recipe}*', master=True)
Done.

>>> chef.define('Recipe', '{Title}.\n\n{Comments}Ingredients.\n{Ingredient}*\n\nMethod.\n{Command}*')
Done.

Simple keywords' CFGs are set thusly:
>>> chef.define('Comments', '{Sentence}*\n\n')
Done.

Keywords can have more than one definition:
>>> chef.define('Comments', ['{Sentence}*\n\n', 'poop'])
Done.

Or you can simply add a definition:
>>> chef.define('Comments', 'poop', add=True)

There is a protected keyword within CFG called nil to terminate recursive definitions.
>>> chef.define('Comments', ['{Sentence}.', '{Sentence}. {Comments}', '{nil}']
Done.

Attempting to overwrite this variable will result in an error,
	even if the redefinition is trivial:
>>> chef.define('nil', '{nil}')
CFGError: Redefinition of nil is prohibited.

The fruits of your work are embodied in the methods .check() and .parse().

.contains() checks a string for obedience of the grammer, returning True or False
>>> chef.contains("Whee!")
False

.parse() will return a deep list sorting the given string.
>>> chef.parse(hello_world)
["Hello World Souffle", "Comments...", "Ingredients.", ["ING1", "ING2"],
	"Method.", ["CMD1", "CMD2"], "Serves 1.", [[AUX1], [AUX2]]]

The CFG class can also return a regular expression.
>>> chef.as_regex()
Wut?
"""
	def __init__(self, master_pattern=None):
		# Subpatterns of the grammar
		self.patterns = dict()
		
		# Set the master pattern of the grammar
		self.patterns['__master__'] = master_pattern
		
		# Set the terminal pattern
		self.patterns['nil'] = None
		
		# Set 'sigma', the collection of all valid terminal tokens
		# For memory-ness, could this be specified by the user to be dynamically defined?
		self.sigma = list()
		
		self.__contains__ = self.contains
		self.__getitem__ = self.get_pattern
		self.__setitem__ = self.set_pattern
		d("CFG created successfully.")
	
	def __str__(self):
		return str(self.patterns['__master__'])
	
	def __repr__(self):
		return "Patterns: " + str(self.patterns) + "\n" + "Sigma: " + str(self.sigma)
	
	def define(self, keyword, pattern, add=False):
		"""Adds the given keyword to the grammer with the specified pattern.
	
		If add is specified, the pattern will be appended as opposed to replaced.
		"""
		if add:
			if isinstance(pattern, list):
				self.set_pattern(keyword, self.get_pattern(keyword) + pattern)
			elif isinstance(pattern, str):
				self.set_pattern(keyword, self.get_pattern(keyword) + [pattern])
			else:
				raise Exception("Invalid argument : pattern neither list nor string")
		else:
			self.set_pattern[keyword] = [pattern]
	
	def get_pattern(self, key):
		return self.patterns[key]
	
	def set_pattern(self, key, pattern):
		d("in set")
		if isinstance(key, str):
			d("key is instance of str")
			if isinstance(pattern, str):
				d("pattern is instance of str")
				self.patterns[key] = [pattern]
			elif isinstance(pattern, list):
				d("pattern is instance of list")
				allstrings = True
				for s in pattern:
					allstrings = allstrings and isinstance(s, str)
				if allstrings:
					d("all els are instances of str")
					self.patterns[key] = pattern
				else:
					raise Exception("Unable to set pattern : One or more arguments not of string type")
			else:
				raise Exception("Unable to set pattern : value neither list nor string")
		else:
			raise Exception("Unable to set pattern : key not string")
	
	def contains(self, string, subpattern='__master__'):
		"""Tests to see if the string given is in the set of strings described of this CFG."""
		# The use of recursion in this buddy is awesome.
		# Calling check on the string will check through the string as normal,
		# recursing on any keywords it finds until the string is empty.
		pass
	
	# returns a list whose elements are those explicitly defined
	def parse(self, string, subpattern='__master__'):
		"""Returns a representative list form of the string.
	
	This function returns a list whose elements are those
	explicitly defined within the subpattern; every element deferred via keyword
	will be inserted as another list.
	
	Recursive, no?
	"""
		pass
	
	# omg... I don't wanna...
	def as_regex(self):
		pass
