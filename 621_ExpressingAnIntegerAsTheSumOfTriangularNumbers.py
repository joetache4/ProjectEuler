"""
Gauss famously proved that every positive integer can be expressed as the sum of three triangular numbers (including 0 as the lowest triangular number). In fact most numbers can be expressed as a sum of three triangular numbers in several ways.

Let G(n) be the number of ways of expressing n as the sum of three triangular numbers, regarding different arrangements of the terms of the sum as distinct.

For example, G(9)=7, as 9 can be expressed as: 3+3+3, 0+3+6, 0+6+3, 3+0+6, 3+6+0, 6+0+3, 6+3+0.
You are given G(1000)=78 and G(10^6)=2106

Find G(17526×10^9) 
17526000000000

ans: 11429712
"""

# TODO
# Hirschhorn and Sellers - ON REPRESENTATIONS OF A NUMBERAS A SUM OF THREE TRIANGLES
# http://www.personal.psu.edu/jxs23/p7.pdf
# G(17526×10^9) = 161 * G(2671239140)

import sys
import math
from lib.log import log

target = 17526*10**9

try:
	target = int(sys.argv[1])
except IndexError:
	pass

def get_tri(target):
	tri, i, n = [], 0, 0
	while n <= target:
		tri.append(n)
		i += 1
		n += i
	return tri

def max_ab(tri):
	max_a_index = -1
	max_b_index = -1
	for i, t in enumerate(tri):
		if max_a_index == -1 and t > target//3:
			max_a_index = i-1
		if t > target//2:
			max_b_index = i-1
			break
	return (max_a_index, max_b_index)

########################################################################################################

# for testing

def is_tri(n):
	n = 2*n
	m = int(math.sqrt(n))
	return m*m + m == n

def brute_force(n, tri):
	count = 0
	for a in tri:
		if a > n: break
		for b in tri:
			if a + b > n: break
			if is_tri(n - a - b): 
				count += 1
	return count

########################################################################################################

import numpy as np
from numba import cuda, int64

def info():
	gpu = cuda.get_current_device()
	print("name = %s" % gpu.name)
	print("maxThreadsPerBlock = %s" % str(gpu.MAX_THREADS_PER_BLOCK))
	print("maxBlockDimX = %s" % str(gpu.MAX_BLOCK_DIM_X))
	print("maxBlockDimY = %s" % str(gpu.MAX_BLOCK_DIM_Y))
	print("maxBlockDimZ = %s" % str(gpu.MAX_BLOCK_DIM_Z))
	print("maxGridDimX = %s" % str(gpu.MAX_GRID_DIM_X))
	print("maxGridDimY = %s" % str(gpu.MAX_GRID_DIM_Y))
	print("maxGridDimZ = %s" % str(gpu.MAX_GRID_DIM_Z))
	print("maxSharedMemoryPerBlock = %s" % str(gpu.MAX_SHARED_MEMORY_PER_BLOCK))
	print("asyncEngineCount = %s" % str(gpu.ASYNC_ENGINE_COUNT))
	print("canMapHostMemory = %s" % str(gpu.CAN_MAP_HOST_MEMORY))
	print("multiProcessorCount = %s" % str(gpu.MULTIPROCESSOR_COUNT))
	print("warpSize = %s" % str(gpu.WARP_SIZE))
	print("unifiedAddressing = %s" % str(gpu.UNIFIED_ADDRESSING))
	print("pciBusID = %s" % str(gpu.PCI_BUS_ID))
	print("pciDeviceID = %s" % str(gpu.PCI_DEVICE_ID))

# Count (a,b,c) where   target = a + b + c   and   a <= b <= c
# Note: two terms (a,b) must be < target/2 and 1 term (a) must be < target/3

block_count = 512
threads_per_block = 512

# The start and stride params indicate where to start looking for the 1st and 2nd terms 
# and how far to look. They are used to divide the problem into a series of GPU calls 
# so it doesn't time out and give an error.
@cuda.jit
def count(target, tri_arr, count_arr, start_a, start_b, max_a_index, max_b_index, stride_a, stride_b):
	th_ind = cuda.grid(1)
	
	if th_ind >= stride_a:
		return
	
	a_ind = th_ind + start_a
	
	if a_ind >= tri_arr.shape[0] or a_ind > max_a_index:
		return
		
	a = tri_arr[a_ind]
	
	step = 1
	if target % 3 == 0 and a % 3 == 1:
		# a, b, and c must all be 1 mod 3
		step = 3
	
	#for b_ind in range(a_ind, max_b_index+1):
	for b_ind in range(a_ind + start_b, min(a_ind + start_b + stride_b, max_b_index+1), step):
		
		b = tri_arr[b_ind]
		c = target - a - b
		
		if c < b:
			break
		
		tmp = math.floor(math.sqrt(2.0*c))
		if tmp*tmp + tmp == 2*c:
			# is triangular
			if a == b and b == c:
				count_arr[a_ind] += 1
			elif a == b or b == c:
				count_arr[a_ind] += 3
			else:
				count_arr[a_ind] += 6
	
def main():
	#info()
	print("***")

	tri = get_tri(target)
	max_a_index, max_b_index = max_ab(tri)
	
	print(f"target  : {target}")
	print(f"len(tri): {len(tri)}")
	print(f"max(tri): {tri[-1]}")
	print(f"max 1st index: {max_a_index}")
	print(f"max 2nd index: {max_b_index}")
	print(f"threads : {block_count*threads_per_block}")
	print("***")
	
	total = 0
	tri_arr = np.array(tri, np.int64)[:max(max_a_index, max_b_index)+1]
	count_arr = np.zeros(tri_arr.shape, np.int64)
	
	stride_a = block_count * threads_per_block
	stride_b = 25002 # must be divisible by 3 to make use of modulo qualities in count()
	for start_a in range(0, max_a_index+1, stride_a):
		print(f"a: {start_a}...")
		for start_b in range(0, max_b_index+1, stride_b):
			print(f"  b: {start_b}...")
			count[block_count, threads_per_block] \
			(target, tri_arr, count_arr, start_a, start_b, max_a_index, max_b_index, stride_a, stride_b)
	total = sum(( count_arr ))
	
	print(total)
	log(f"G({target}) = {total}")
	
	# test
	if target <= 10000000:
		print(brute_force(target, tri))
	
	return total

#main()


########################################################################################################
# multithreading

'''

import threading
from lib.log import log

def is_tri(n):
	n = 2*n
	m = int(math.sqrt(n))
	return m*m + m == n
	
terms, terms_lock = set(), threading.Lock()

def found_set(new_found):
	terms_lock.acquire()
	for f in new_found:
		terms.add(f)
	terms_lock.release()



def count_two_term_sums(a_index, a, target):
	
	found = set()
	target2 = target - a
	
	if target % 3 == 0:
	
		if a % 3 == 0:
			# b must also be 0 mod 3
			for b_index in range(a_index, len(tri), 3):
				b = tri[b_index]
				if b > target//2:
					break
				c = target2 - b
				if b <= c and is_tri(c): # TODO break if c < b
					found.add((a, b, c))
			
			a_index += 1
			if tri[a_index] % 3 == 1:
				a_index += 1
			
			for b_index in range(a_index, len(tri), 3):
				b = tri[b_index]
				if b > target//2:
					break
				c = target2 - b
				if b <= c and is_tri(c):
					found.add((a, b, c))
					
		else:
			# b must also be 1 mod 3
			for b_index in range(a_index, len(tri), 3):
				b = tri[b_index]
				if b > target//2:
					break
				c = target2 - b
				if b <= c and is_tri(c):
					found.add((a, b, c))
	else:
		for b_index in range(a_index, len(tri)):
			b = tri[b_index]
			if b > target//2:
				break
			c = target2 - b
			if b <= c and is_tri(c):
				found.add((a, b, c))
	
	found_set(found)

# assume a <= b <= c
def main(target):
	print(f"main loop end: {len(tri)//3}")
	# two terms must be < target/2, 1 term must be < target/3
	for a_index, a in enumerate(tri):
		if a > target//3:
			break
		if a_index % 10 == 0:
			print(a_index)
		
		threading.Thread(target=count_two_term_sums, args=(a_index, a, target)).start()
	
	# wait for all threads to finish
	main_thread = threading.currentThread()
	for t in threading.enumerate():
		if t is main_thread:
			continue
		t.join()
	
	#print(terms)
	ans = sum(( count_unique_perms(t) for t in terms ))
	print(ans)
	log(ans)
	return ans

#main(target)
'''
