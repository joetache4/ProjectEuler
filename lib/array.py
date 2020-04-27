def subsets(collection, min_size = 0, max_size = -1):
	"""Generator of subsets of an list or set."""
	
	def _subsets(arr, min_size, max_size, _subarr = None, _index = 0):
		# TODO this will cause a RecursionError if len(arr) >= 1000
		if _subarr is None:
			_subarr = []
		if max_size == -1:
			max_size = len(arr)
		if len(_subarr) > max_size or len(_subarr) + len(arr) - _index < min_size:
			return
		if _index == len(arr):
			yield _subarr.copy()
		else:
			yield from _subsets(arr, min_size, max_size, _subarr, _index + 1)
			_subarr.append(arr[_index])
			yield from _subsets(arr, min_size, max_size, _subarr, _index + 1)
			_subarr.pop()
	
	if isinstance(collection, list):
		yield from _subsets(collection, min_size, max_size)
	else:
		for x in _subsets(list(collection), min_size, max_size):
			yield set(x)



def permutations(arr, _ind = None):
	"""Generator of permutations of an list."""
	
	if _ind is None:
		_ind = []
	if len(_ind) == len(arr):
		yield [arr[i] for i in _ind]
	else:
		for i in range(len(arr)):
			if i not in _ind:
				_ind.append(i)
				yield from permutations(arr, _ind)
				_ind.pop()



def binary_search(arr, target, accessor = None):
	"""Return (index, item) if accessor is not none, else just index."""
	
	L = 0
	R = len(arr) - 1
	if accessor is None:
		while L <= R:
			mid = (L+R) // 2
			if arr[mid] < target:
				L = mid + 1
			elif arr[mid] > target:
				R = mid - 1
			else:
				return mid
		return -1
	else:
		while L <= R:
			mid = (L+R) // 2
			if accessor(arr[mid]) < target:
				L = mid + 1
			elif accessor(arr[mid]) > target:
				R = mid - 1
			else:
				return (mid, arr[mid])
		return (-1, None)

def bs_contains(arr, target, accessor = None):
	"""Binary searches for an item in a list."""
	
	if accessor is None:
		return binary_search(arr, target, accessor) != -1
	else:
		return binary_search(arr, target, accessor) != (-1, None)


def perm(n, arr):
	"""
	Returns the n-th permutation of arr.
	
	Requirements:
	  len(arr) > 1
	  n needs to between 0 and len(arr)! - 1
	"""
	
	# create list of factorials
	factorials = [0, 1]
	while(len(arr) != len(factorials)):
		factorials.append(factorials[-1] * len(factorials))
	factorials.reverse()
	# convert n to its representation in the factorial numbering system
	fact_index = 0
	m = 10 # 10 is used instead of 0 so m can be a a bunch of 0's if needed
	while(n > 0):
		if (n >= factorials[fact_index]):
			m += 1
			n -= factorials[fact_index]
		else:
			fact_index += 1
			m = 10 * m
	while(fact_index < len(factorials)-1):
		m = 10 * m
		fact_index += 1
	m = [int(x) for x in str(m)]
	m.pop(0)
	# create permuted list
	new_arr = []
	for x in m:
		new_arr.append(arr.pop(int(x)))
	return new_arr

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K