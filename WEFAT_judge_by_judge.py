import csv
import pandas
import sys
import WEFAT_Judge
import operator

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
			if key == '' or val == '':
				continue
			if key in dic.keys():
				if val not in dic[key]:
					dic[key].append(val)
			else:
				dic[key] = [val]

	# write result into csv in the following format:
	# JudgeName, caseid_1 caseid_2 ...
	with open(res, 'wb') as csvfile:
		reswriter = csv.writer(csvfile, delimiter=',')
		# sort dictionary item list by number of cases
		for key, value in sorted(dic.items(), key=lambda x: len(x[1]), reverse = True):
			valstr = ' '.join(value)
			reswriter.writerow([key] + [valstr])

def train_models(judge_name, caseid_set):
	text_dir = 'cleaned'
	model = WEFAT_Judge.WVModel(text_dir, judge_name, caseid_set)
	# Since all text by one judge is a relatively small corpus, 
	# use min_count = 1 when training
	model.train_model(min_count_ = 1)

def use_models(fname):
	scores = {}
	text_dir = 'cleaned'
	csv.field_size_limit(sys.maxsize)
	with open(fname, 'rb') as csvfile:
		cjreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
		for row in cjreader:
			model = WEFAT_Judge.WVModel(text_dir, row[0])
			score, effect_size = model.calc_weat()
			scores[row[0]] = [score, effect_size]


	typestr = 'weapon'
	with open('weat-res-' + typestr, 'wb') as csvfile:
		reswriter = csv.writer(csvfile, delimiter=',')
		for key, value in scores.iteritems():
			reswriter.writerow([key] + [value])


def load_csv(fname):
	# set maxsize as limitsize to read huge fields
	csv.field_size_limit(sys.maxsize)
	# train the first 200 judges who has most cases 
	count = 0
	JUDGE_NUM = 200
	# record the cases used in training model
	used_cases = 0
	with open(fname, 'rb') as csvfile:
		cjreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
		for row in cjreader:
			if count > JUDGE_NUM:
				break
			train_models(row[0], row[1].split(' '))
			count += 1
			used_cases += len(row[1].split(' '))

	print 'total trained models (judge) count: ', JUDGE_NUM
	print 'total used cases count: ', used_cases

def main():
	dta_fname = 'data/BloombergVOTELEVEL_Touse.dta'
	cj_fname = 'tmp/judge_correspond_case.csv'

	if len(sys.argv) != 2:
		print 'usage: python WEFAT_judge_by_judge.py [-p|-t|-u]'
		print '-p: process dta data to get corresponding case and judge'
		print '-t: train model'
		print '-u: use model for computing corresponding score of each judge'
	elif sys.argv[1] == '-p':
		# process dataset to get corresponding relationship between cases and judges
		# save the result to cj_fname
		load_dta(dta_fname, cj_fname)
	elif sys.argv[1] == '-t':
		# use cj_fname to train word vector judge by judge
		load_csv(cj_fname)
	elif sys.argv[1] == '-u':
		use_models(cj_fname)


if __name__ == "__main__":
	main()
