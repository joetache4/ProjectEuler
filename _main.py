import sys
import os
import time
import timeit

def get_file(prefix):
	try:
		prefix = prefix.zfill(3)
		for file in os.listdir("."):
			if file.startswith(prefix):
				return file
	except:
		pass
	return None

def run(args):
	file = args[0]
	args = " ".join(args[1:])
	print()
	print(time.strftime("%I:%M:%S %p"))
	print(file)
	print("-" * len(file))
	print()
	start = timeit.default_timer()	
	try:
		success = False
		success = os.system(f"python {file} {args}") == 0
	except KeyboardInterrupt:
		pass	
	stop = timeit.default_timer()
	print()
	print("-" * len(file))
	print("Completion time: {0:.2f}s".format(stop - start))
	print()
	return success

def main_loop():
	while True:
		# get input
		args = input("Enter a problem number: ")
		if not args:
			continue
		if args.lower() in ["quit", "exit", "qqq"]:
			break
		args = args.split(" ")
		file = get_file(args[0])
		# run
		if file is None:
			print("File not found.")
		else:
			args[0] = file
			while not run(args):
				if input("Retry? [Y/n]").lower() == 'n':
					break

if __name__ == '__main__':
	try:
		main_loop()
	except (EOFError, KeyboardInterrupt):
		pass