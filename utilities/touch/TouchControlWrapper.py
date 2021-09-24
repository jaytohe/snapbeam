class TouchControlWrapper:

	def __init__(self, device):
		self.dev = device

	def swipe(self, vector_start, vector_end, dt):
		vector_start = self.to_str(vector_start)
		vector_end = self.to_str(vector_end)
		self.dev.shell(f"input touchscreen swipe {vector_start} {vector_end} {dt}")

	def tap_and_hold(self, vector, dt):
		vector = self.to_str(vector)
		self.dev.shell(f"input touchscreen swipe {vector} {vector} {dt}")

	def tap(self, vector):
		vector = self.to_str(vector)
		self.dev.shell(f"input touchscreen tap {vector}")

	def kbpress(self, keycode):
		self.dev.shell(f"input keyevent {keycode}")
	
	def type(self, txt):
		self.dev.shell(f"input text {txt}")
		
	def to_str(self, vector):
		shell_string=""
		for coord in vector:
			shell_string += str(coord)+" "
		#DEBUG
		print("Sending touch event on pos :", shell_string)
		return shell_string[:-1]
