import os
import threading
import queue
import librosa

from CommandMfcc import CommandMfcc


class CommandMfccCreator:
	def __init__(self, learning_database_rootdir_path, test_database_rootdir_path):
		self.threads_number = 4
		self.results_queue = queue.Queue()
		self.task_queue = queue.Queue()
		self.learning_database_rootdir_path = learning_database_rootdir_path + '/'
		self.test_database_rootdir_path = test_database_rootdir_path + '/'
		self.category_list_dir = os.listdir(self.learning_database_rootdir_path)

	class MfccThread(threading.Thread):
		def __init__(self, i, task_queue):
			threading.Thread.__init__(self)
			self.task_queue = task_queue
			self.i = i

		def run(self):
			while True:
				req = self.task_queue.get()
				if req is None:
					self.task_queue.task_done()
					break
				name, path, output_queue = req
				try:
					temp = CommandMfccCreator.record_to_command_mfcc(name, path)
					print("Threat id:" + str(self.i) + " Transformed to mfcc: " + str(path))
					output_queue.put(temp)
					self.task_queue.task_done()
				except:
					print("Unable to load record: " + str(path))
					self.task_queue.task_done()

	@staticmethod
	def record_to_command_mfcc(name, file_list_dir_path):
		y, sr = librosa.load(file_list_dir_path)
		return CommandMfcc(name, librosa.feature.mfcc(y, sr))

	def init_multi_threading(self):
		for i in range(self.threads_number):
			self.MfccThread(i, self.task_queue).start()

	def put_tasks_to_thread_queues(self):
		for i in range(len(self.category_list_dir)):
			file_list_dir = os.listdir(self.learning_database_rootdir_path + self.category_list_dir[i])
			for j in range(len(file_list_dir)):
				load_file_path = (
					self.learning_database_rootdir_path + self.category_list_dir[i] + '/' + file_list_dir[j])
				self.task_queue.put((self.category_list_dir[i], load_file_path, self.results_queue))
		for _ in range(self.threads_number):
			self.task_queue.put(None)

	def get_threads_results(self):
		self.task_queue.join()
		results_commands_mfcc_list = list()
		for _ in range(self.results_queue.qsize()):
			results_commands_mfcc_list.append(self.results_queue.get())
		return results_commands_mfcc_list

	def get_list_of_learning_records(self):
		self.init_multi_threading()
		self.put_tasks_to_thread_queues()
		return self.get_threads_results()

	def get_list_of_testing_records(self):
		commands_mfcc_list = list()
		file_list_dir = os.listdir(self.test_database_rootdir_path)
		for i in range(len(file_list_dir)):
			load_file_path = (self.test_database_rootdir_path + file_list_dir[i])
			try:
				temp = self.record_to_command_mfcc(file_list_dir[i], load_file_path)
				print( "Transformed to mfcc:" + str(load_file_path))
			except:
				print("Unable to load record: " + str(load_file_path))
				temp = CommandMfcc(str(i), None)
			commands_mfcc_list.append(temp)
		return commands_mfcc_list
