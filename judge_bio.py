import pandas
import numpy as np
import csv
import matplotlib.pyplot as plt

def load_dta(fname, weat_fname):

	judge_list = []
	judge_in_list_count = 0
	judge_weat = {}
	judge_gender = {}
	judge_origin = {}
	judge_race = {}
	judge_year = {}
	city_map = {}
	south = ['KY','FL','AR','MD','NC','SC','TX','VA','GA']
	with open("./data/city_format.csv",'rb') as city_code:
		cjreader = csv.reader(city_code, delimiter=',')
		for row in cjreader:
			if len(row) == 3 and row[2] in south:
				city_map[int(row[0])] = row[2]

	with open(weat_fname, 'rb') as weat_file:
		for line in weat_file:
			strs = line.split(',')
			if len(strs) < 3:
				continue
			else:
				judge_weat[strs[0]] = float(strs[1])
				judge_list.append(strs[0])

	itr = pandas.read_stata(fname, chunksize=10000)
	count = 0

	for chunk in itr:
		for index, row in chunk.iterrows():
			count += 1
			judge_first_name = row['name'].split(",")[0]
			print count, row['name'], row['gender'], row['race'], row['yearb'], row['csb']

			if judge_first_name.upper() in judge_list:
				judge_list.remove(judge_first_name.upper())
				judge_in_list_count += 1
				judge_gender[judge_first_name.upper()] = row['gender']
				judge_race[judge_first_name.upper()] = row['race']
				judge_year[judge_first_name.upper()] = row['yearb']
				if row['csb'] in city_map:
					judge_origin[judge_first_name.upper()] = 1
				else:
					judge_origin[judge_first_name.upper()] = 0

	print "judge num:", judge_in_list_count
	with open("result-score/judge_csb.csv", 'wb') as csvfile:
		reswriter_ = csv.writer(csvfile, delimiter=',')
		for key, value in judge_origin.items():
			weat_score = judge_weat[key]
			reswriter_.writerow([weat_score] + [value])

	with open("result-score/judge_year_weat_gender.csv", 'wb') as csvfile:
		reswriter_ = csv.writer(csvfile, delimiter=',')
		for key, value in judge_year.items():
			weat_score = judge_weat[key]
			reswriter_.writerow([weat_score] + [value])

def plot():
	# scatter plot for judge birth year and weat score
	weat_score = []
	birth_year = []
	with open("result-score/judge_csb.csv", 'rb') as weat_file:
		for line in weat_file:
			strs = line.split(',')
			score = float(strs[0])
			year = int(float(strs[1].strip()))
			weat_score.append(score)
			birth_year.append(year)

	fig = plt.figure()
	fig.suptitle('test title', fontsize=20)
	plt.xlabel('birth year', fontsize=16)
	plt.ylabel('weat score', fontsize=16)
	plt.scatter(birth_year, weat_score)
	plt.show()
	fig.savefig('figure/byear-gender-weat')

def main():
	dta_fname = 'data/auburn_district_w_songer_codes.dta'
	weat_fname = 'result-score/weat-res-gender'
	#load_dta(dta_fname, weat_fname)
	plot()

if __name__ == "__main__":
	main()
