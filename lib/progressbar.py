from datetime import datetime

class ProgressBar:	

	def __init__(self, max_ticks, width = 50):
		self.ticks       = 0
		self.max_ticks   = max_ticks
		self.width       = width
		self.print_width = 0
	
	def is_done(self):
		return self.ticks == self.max_ticks
	
	def tick(self):
		if self.is_done():
			return
		self.ticks += 1
		self.print()
		if self.ticks == self.max_ticks:
			print()
	
	def finish(self):
		if self.is_done():
			return
		self.ticks = self.max_ticks - 1
		self.tick()
	
	def print(self):
		p = lambda s: print(s, end = "", flush = True)
		
		p("\b" * self.print_width)
		
		percent          = int(self.ticks / self.max_ticks * 100)
		bar_len          = int(self.ticks / self.max_ticks * self.width)		
		info             = "█" * bar_len + "░" * (self.width - bar_len)
		info            += f" {percent}% ({self.ticks}/{self.max_ticks})"
		info            += f" {datetime.now().time().strftime('%I:%M:%S %p')}"
		self.print_width = len(info)
		
		p(info)

def tick(max_ticks, pb = []):
	if len(pb) == 0:
		pb.append(ProgressBar(max_ticks))
	pb[0].tick()
	if pb[0].is_done():
		pb.pop()