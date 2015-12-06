import re

#part 1
class light(object):
	def __init__(self):
		self.lit = False
	def toggle(self):
		self.lit = not self.lit
	def turn_on(self):
		self.lit = True
	def turn_off(self):
		self.lit = False
	def isLit(self):
		return 1 if self.lit else 0
		
grid = {}
for i in range(1000):
	grid[i] = {}

for i in range(1000):
	for j in range(1000):
		grid[i][j] = light()
		
turn_on = lambda x: x.turn_on()
turn_off = lambda x: x.turn_off()
toggle = lambda x: x.toggle()
functions = {'turn on': turn_on, 'turn off': turn_off, 'toggle': toggle}
extractor = re.compile(r'([\w\s]+) (\d+),(\d+) through (\d+),(\d+)')

def extract(line):
	return extractor.match(line).groups()
	
def run_rule(line):
	ins = extract(line)
	rule, x0, x1, y0, y1 = (functions[ins[0]], int(ins[1]), int(ins[2]), int(ins[3]), int(ins[4]))
	for i in range(x0, y0+1):
		for j in range(x1, y1+1):
			rule(grid[i][j])
	
def get_total_count():
	total = 0
	for i in range(1000):
		for j in range(1000):
			total += grid[i][j].isLit()
	return total
	
with open('day6.in') as f:
	for line in f:
		run_rule(line)

print(get_total_count())