import csv
import sys
from CommandMfccCreator import CommandMfccCreator
import datetime
import librosa

MIN_DIST = 3700


class CommandRecognitor:
	def __init__(self, learning_list):
		self.learning_list = learning_list

	def compare_test_record_2_learning_list(self,test_element):
		dist = list()
		for i in range(0, len(self.learning_list)):
			y = self.learning_list[i].mfcc
			D, wp = librosa.dtw(test_element, y, subseq=True)
			dist.append(D[- 1, - 1])
		if min(dist) > MIN_DIST:
			return "nie rozpoznano"
		else:
			return self.learning_list[dist.index(min(dist))].name
