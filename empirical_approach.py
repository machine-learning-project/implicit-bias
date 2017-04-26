import pandas
import numpy as np
import csv

def load_dta(fname, res):
	itr = pandas.read_stata(fname, chunksize=10000)
	count = 0
	dic = {}

	csvfile_w = open(res, 'wb')
	csvfile_w.write("# caseid, year, songername, circuit, govt_wins, x_republican\n")
	reswriter = csv.writer(csvfile_w, delimiter=',')

	# iterate chunk in dataset
	for chunk in itr:
		# print column names in dataframe
		# print list(chunk.columns.values)

		for index, row in chunk.iterrows():
			count += 1

			x_republican = row['x_republican']

			if row['songername'] not in dic:
				dic[row['songername']] = row['x_republican']
			else:
				if np.isnan(dic[row['songername']]) and not np.isnan(row['x_republican']):
					dic[row['songername']] = row['x_republican']
				x_republican = dic[row['songername']]

			# filter cases related to government
			if row['govt_any'] != 1.0:
				continue

			print count, row['caseid'], row['govt_any'], row['year'], row['songername'], row['circuit'], row['govt_wins'], row['x_republican'], x_republican
			reswriter.writerow([row['caseid']] + [row['year']] + [row['songername']] + [row['circuit']] + [row['govt_wins']] + [x_republican])

	csvfile_w.close()

	# write into csv in the following format:
	# JudgeName, isRepublican
	with open("data/judge_republican.csv", 'wb') as csvfile:
		reswriter_ = csv.writer(csvfile, delimiter=',')
		for key, value in dic.items():
			reswriter_.writerow([key] + [value])

def main():
	gov_fname = 'data/govern_data.dta'
	res_fname = 'data/presessed_govern_data.csv'
	load_dta(gov_fname, res_fname)

if __name__ == "__main__":
	main()