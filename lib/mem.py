"""
A collection of useful methods for getting and printing total memory usage of the running python process. In addition, the current memory usage will be printed right before the program exits.
"""

import os
import atexit

# define this method just so its there even if psutil isn't installed
def snapshot():
	pass
	
try:
	import psutil

	mem_usage = []

	def get_mem_usage():
		"""Get memory usage in MB."""
		
		process = psutil.Process(os.getpid())
		mem     = int(process.memory_info().rss / 1000**2) # in MB
		return mem

	def snapshot():
		"""Record the current memory usage for end-of-program statistics."""
		
		mem_usage.append(get_mem_usage())

	def print_mem_usage():
		"""Prints summary of memory usage just before program exits."""
		
		print("~~~~~~~~~~~~")
		print("Memory usage")
		if len(mem_usage) > 0:
			print(f"Max    : {int(max(mem_usage))               } MB")
			print(f"Average: {int(sum(mem_usage)/len(mem_usage))} MB")
		print(f"At exit: {    int(get_mem_usage())              } MB")

	atexit.register(print_mem_usage)
	
except ImportError:
	print("Package 'psutil' not installed. Memory usage will not be reported.")
	print()