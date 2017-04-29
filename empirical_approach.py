import pandas
import numpy as np
import csv
import argparse
import statsmodels.api as sm

def load_dta(fname, res, judge_co_fname):
	itr = pandas.read_stata(fname, chunksize=10000)
	count = 0
	dic = {}
	judge_list = []

	judge_list_fname = 'tmp/judges_list.csv'
	with open(judge_list_fname, 'rb') as judge_csvfile:
		cjreader = csv.reader(judge_csvfile)
		for row in cjreader:
			judge_list.append(row[0].strip())

	csvfile_w = open(res, 'wb')
	csvfile_w.write("# caseid, year, songername, songerfirstname, circuit, govt_wins, x_republican\n")
	reswriter = csv.writer(csvfile_w, delimiter=',')

	# iterate chunk in dataset
	for chunk in itr:
		# print column names in dataframe
		# print list(chunk.columns.values)

		for index, row in chunk.iterrows():
			count += 1

			x_republican = row['x_republican']

			# filter empty judge name
			if row['songername'] == '':
				continue

			# check if we have weat score for that judge
			songer_first_name = row['songername'].split(",")[0]
			if not (songer_first_name in judge_list or row['songername'] in judge_list):
				continue

			# record is_republican info for judge
			if songer_first_name not in dic:
				dic[songer_first_name] = row['x_republican']
			else:
				if np.isnan(dic[songer_first_name]) and not np.isnan(row['x_republican']):
					dic[songer_first_name] = row['x_republican']
				x_republican = dic[songer_first_name]

			# filter cases related to government
			if row['govt_any'] != 1.0:
				continue

			print count, row['caseid'], row['govt_any'], row['year'], row['songername'], songer_first_name, row['circuit'], row['govt_wins'], row['x_republican'], x_republican
			reswriter.writerow([row['caseid']] + [row['year']] + [row['songername']] +
				[songer_first_name] + [row['circuit']] + [row['govt_wins']] + [x_republican])

	csvfile_w.close()

	print "total judge num:", len(dic)

	# write into csv in the following format:
	# JudgeName, isRepublican
	with open(judge_co_fname, 'wb') as csvfile:
		reswriter_ = csv.writer(csvfile, delimiter=',')
		for key, value in dic.items():
			reswriter_.writerow([key] + [value])


def combine_data(data_fname, judge_co_fname, judge_weat_fname, combined_fname):
	judge_repub = {}
	judge_weat = {}
	with open(judge_co_fname, 'rb') as csvfile:
		cjreader = csv.reader(csvfile, delimiter=',')
		for row in cjreader:
			if np.isnan(float(row[1])):
				continue
			if row[0] not in judge_repub:
				judge_repub[row[0]] = float(row[1])

	print "loading", judge_co_fname ,len(judge_repub)

	with open(judge_weat_fname, 'r') as weat_file:
		for line in weat_file:
			strs = line.split(',')
			if len(strs) < 3:
				continue
			else:
				judge_weat[strs[0]] = float(strs[1])

	print "loading", judge_weat_fname, len(judge_weat)

	with open(data_fname, 'rb') as csvfile, open(combined_fname, 'wb') as csvfile_w:
		csvfile_w.write("# caseid, year, songername, songerfirstname, circuit, govt_wins, x_republican, x_weat\n")
		first_line = True
		cjreader = csv.reader(csvfile, delimiter=',')
		cjwriter = csv.writer(csvfile_w, delimiter=',')
		for row in cjreader:
			if first_line:
				first_line = False
				continue
			if row[3] not in judge_repub or row[3] not in judge_weat:
				continue
			else:
				x_republican = judge_repub[row[3]]
				x_weat = judge_weat[row[3]]
				cjwriter.writerow([row[0]] + [row[1]] + [row[2]] + [row[3]] 
					+ [row[4]] + [row[5]] + [x_republican] + [x_weat])


def OLS_regression(Y, X):
	print "regression.."
	model = sm.OLS(Y,X)
	results = model.fit()
	print "params", results.params
	print "tvalues", results.tvalues

def regression(fname):
	df = pandas.read_csv(fname, delimiter=',', skiprows=1,
		 names=["caseid", "year", "songername", "songerfirstname", "circuit", "govt_wins", "x_republican", "x_weat"],
		 dtype={"year":int, "circuit":int, "govt_wins":float, "x_republican":float, "x_weat":float})
	
	# drop last column
	# df = df.drop("x_republican", axis=1)
	print "loading", fname, df.shape

	demean = lambda df: df - df.mean()
	groupby_ct = df.groupby(['year', 'circuit'])
	
	transformed = groupby_ct.transform(demean)
	# print transformed
	Y = transformed['govt_wins']
	X = transformed[['x_republican', 'x_weat']]
	# print Y
	print X
	# for name, group in groupby_ct:
		# print name
		# print group

	OLS_regression(Y,X)

def main():
	gov_fname = 'data/govern_data.dta'
	res_fname = 'data/presessed_govern_data.csv'
	judge_co_fname = "data/judge_republican.csv"
	combined_fname = 'data/combined_govern_data.csv'
	judge_weat_fname = 'result-score/weat-res-government'

	# parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', help='process government related dta file', action='store_true')
	parser.add_argument('-t', help='use empirical approach (OLS)', action='store_true')
	args = parser.parse_args()

	# process govern_data and store useful information into res_fname.
	if args.p:
		# load_dta(gov_fname, res_fname)
		combine_data(res_fname, judge_co_fname, judge_weat_fname, combined_fname)

	# do OLS based on judicial data
	if args.t:
		regression(combined_fname)


if __name__ == "__main__":
	main()