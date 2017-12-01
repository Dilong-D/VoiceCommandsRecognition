import csv

import sys

from CommandMfccCreator import CommandMfccCreator
from CommandRecognitor import CommandRecognitor



LEARNING_DATABASE_ROOTDIR_PATH = sys.argv[1]
TEST_DATABASE_ROOTDIR_PATH = sys.argv[2]
command_mfcc_builder = CommandMfccCreator(LEARNING_DATABASE_ROOTDIR_PATH, TEST_DATABASE_ROOTDIR_PATH)
list_learning_records_mfcc = command_mfcc_builder.get_list_of_learning_records()
list_test_records_mfcc = command_mfcc_builder.get_list_of_testing_records()
command_recognitor = CommandRecognitor(list_learning_records_mfcc)
with open('275635.csv', "w") as f:
	writer = csv.writer(f)

for l in range(0, len(list_test_records_mfcc)):
	result = command_recognitor.compare_test_record_2_learning_list(list_test_records_mfcc[l].mfcc)
	print("Record ", list_test_records_mfcc[l].name, " recognized as", result)
	with open('275635.csv', "a") as f:
		writer = csv.writer(f, delimiter=' ', lineterminator='\n')
		writer.writerow(result)
