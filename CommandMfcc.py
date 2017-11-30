def extract_name_from_dir(dir_arg):
	return dir_arg[dir_arg.rindex('_'):-4]


class CommandMfcc:
	def __init__(self, name, temp_mfcc):
		self.name = name
		self.mfcc = temp_mfcc

	def __str__(self):
		temp_string_out = 'Name: ' + self.name
		return temp_string_out
