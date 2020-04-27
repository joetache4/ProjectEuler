import sys
import os
from datetime import datetime
from contextlib import contextmanager

@contextmanager
def do_print(verbose = True):
	"""Toggle printing to the console."""
	if verbose:
		yield
	else:
		old_stdout = sys.stdout
		sys.stdout = open(os.devnull, "w")
		yield
		sys.stdout = old_stdout

def log(message, **kwargs):
	"""
	Logs a message to _log.txt in cwd (creating it if it doesn't exist). Pass the named parameter shutdown = True to shutdown the computer after logging the message.
	"""
	try:
		message = str(message) + "\n\n"
		with open("_log.txt", "a+") as f:
			f.write(f"<{datetime.now()}>\n")
			f.write(message)

		if kwargs["shutdown"]:
			shutdown()
	except:
		pass

def shutdown():
	"""Shutdown the computer."""
	if os.name == "nt": # windows
		os.system("shutdown /s /f /t 0")
	else:
		os.system("shutdown -t now")