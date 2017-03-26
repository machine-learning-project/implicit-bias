import csv
import pandas
import sys
import csv

#load csv file
# def loadcsv(fname):
# 	with open(fname, 'rb') as csvfile:
# 		reader = csv.reader(csvfile, delimiter = ',')
# 		for row in reader:
# 			print row


def load_dta(fname, res):
	itr = pandas.read_stata(fname, chunksize=10000)
	count = 0
	dic = {}
	# iterate chunk in dataset
	for chunk in itr:
		for index, row in chunk.iterrows():
			count += 1
			print count, row['caseid'], row['Author']
			key = row['Author']
			val = row['caseid']
			# disregard empty entry
			if key == '':
				continue
			if key in dic.keys() and val not in dic[key]:
				dic[key].append(val)
			else:
				dic[key] = [val]

	# write result into csv
	with open(res, 'wb') as csvfile:
		reswriter = csv.writer(csvfile, delimiter=',')
		
		for key, value in dic.iteritems():
			valstr = ''
			for i in value:
				valstr += i + ' '
			reswriter.writerow([key] + [valstr])
    	


def main():
	dta_fname = 'data/BloombergVOTELEVEL_Touse.dta'
	cj_fname = 'tmp/judge_correspond_case.csv'

	if len(sys.argv) != 2:
		print 'usage: python WEFAT_judge_by_judge.py [-p|-u]'
		print '-p: process dta data to get corresponding case and judge'
		print '-u: use model'
	elif sys.argv[1] == '-p':
		# process dataset to get corresponding relationship between cases and judges
		# save the result to cj_fname
		load_dta(dta_fname, cj_fname)
	elif sys.argv[1] == '-u':
		# use cj_fname to train word vector judge by judge
		print 'unfinished'

	


if __name__ == "__main__":
	main()
