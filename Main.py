import csv

from CommandMfccCreator import CommandMfccCreator
import datetime
import librosa

mindist = 3700


def wyszukiwanie_podobienstwa2(mfcc_list, mfcc_test):
	dyst = list()
	for i in range(0, len(mfcc_list)):
		y = mfcc_list[i].mfcc  # odwolanie do bazy danych
		D, wp = librosa.dtw(mfcc_test, y, subseq=True)
		# print(D[mfcc_test[1].size - 1, y[1].size - 1], self.name[i])
		dyst.append(D[- 1, - 1])
		# if D[- 1, - 1] < 3000:
		# print(self.name[i], "dystans: ", D[- 1, - 1])
	print("minimalna odleglosc to:", min(dyst))
	if min(dyst) > mindist:
		return "nie rozpoznano"
	else:
		return mfcc_list[dyst.index(min(dyst))].name


LEARNING_DATABASE_ROOTDIR_PATH = "/home/dominik/Pobrane/bazy/database"
TEST_DATABASE_ROOTDIR_PATH = "/home/dominik/Pobrane/bazy/test"
print(str(datetime.datetime.now()))
command_mfcc_builder = CommandMfccCreator(LEARNING_DATABASE_ROOTDIR_PATH, TEST_DATABASE_ROOTDIR_PATH)
lista_data = command_mfcc_builder.get_list_of_learning_records()
lista_test = command_mfcc_builder.get_list_of_testing_records()
print(str(datetime.datetime.now()))

with open('ttest.csv', "w") as f:
	writer = csv.writer(f)

for l in range(0, len(lista_test)):
	wynik = wyszukiwanie_podobienstwa2(lista_data, lista_test[l].mfcc)
	print("wynik pomiaru", lista_test[l].name, "to", wynik)
	with open('ttest.csv', "a") as f:
		writer = csv.writer(f, delimiter=' ', lineterminator='\n')
		writer.writerow(wynik)

print(str(datetime.datetime.now()))
