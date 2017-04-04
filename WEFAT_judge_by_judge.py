import csv
import pandas
import sys
import WEFAT_Judge
import operator

JUDGE_NUM = 200

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

def use_models(judge_list_fname, stimuli_set_fname):
	# iterate through all stimuli set
	with open(stimuli_set_fname, 'rb') as txtfile:
		for line in txtfile:
			line = line.strip()
			use_model(judge_list_fname, line)


def use_model(judge_list_fname, type_str):
	scores = {}
	text_dir = 'cleaned'
	count = 0
	# iterate through all judges
	with open(judge_list_fname, 'rb') as csvfile:
		cjreader = csv.reader(csvfile)
		for row in cjreader:
			if count > JUDGE_NUM:
				break
			count += 1
			model = WEFAT_Judge.WVModel(text_dir, row[0])
			score, effect_size = model.calc_weat(type_str)
			# check if not None
			if score and effect_size:
				scores[row[0]] = [score, effect_size]

	# write the weat score of each judge back in corresponding file
	with open('result-score/weat-res-' + type_str, 'wb') as csvfile:
		reswriter = csv.writer(csvfile, delimiter=',')
		for key, value in scores.iteritems():
			reswriter.writerow([key] + [value])


def load_csv(fname, judge_list_fname):
	# set maxsize as limitsize to read huge fields
	csv.field_size_limit(sys.maxsize)
	# train the first 200 judges who has most cases 
	count = 0
	# record the cases used in training model
	used_cases = 0
	with open(fname, 'rb') as csvfile, open(judge_list_fname, 'wb') as csvfile_:
		cjreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
		reswriter = csv.writer(csvfile_)
		for row in cjreader:
			if count > JUDGE_NUM:
				break
			train_models(row[0], row[1].split(' '))
			count += 1
			used_cases += len(row[1].split(' '))
			reswriter.writerow([row[0]])

	print 'total trained models (judge) count: ', JUDGE_NUM
	print 'total used cases count: ', used_cases

def main():
	dta_fname = 'data/BloombergVOTELEVEL_Touse.dta'
	cj_fname = 'tmp/judge_correspond_case.csv'
	stimuli_set_fname = 'target-attr-words/stimuli-set-type'
	judge_list_fname = 'tmp/judges_list.csv'

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
		load_csv(cj_fname, judge_list_fname)
	elif sys.argv[1] == '-u':
		use_models(judge_list_fname, stimuli_set_fname)


if __name__ == "__main__":
	main()
