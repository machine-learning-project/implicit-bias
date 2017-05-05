import pandas
import numpy as np
import csv
from sklearn.ensemble import RandomForestRegressor

def regression(fname):
	df = pandas.read_csv(fname, delimiter=',', skiprows=1,
		 names=["caseid", "year", "songername", "songerfirstname", "circuit", "govt_wins", "x_republican", "x_weat"],
		 dtype={"year":int, "circuit":int, "govt_wins":float, "x_republican":float, "x_weat":float})
	
	print "loading", fname, df.shape

	demean = lambda df: df - df.mean()
	groupby_ct = df.groupby(['year', 'circuit'])
	transformed = groupby_ct.transform(demean)

	# output
	Y = transformed['govt_wins']
	# treatment variable
	D = transformed['x_weat']
	# control variable
	Z = transformed['x_republican']

	# copy over
	D_ = np.zeros((D.shape[0], 1))
	Z_ = np.zeros((Z.shape[0], 1))
	Y_ = np.zeros((Y.shape[0], 1))

	for i in range(D.shape[0]):
		D_[i] = D[i]

	for i in range(Z.shape[0]):
		Z_[i] = Z[i]

	for i in range(Y.shape[0]):
		Y_[i] = Y[i]

	print Z.shape, Z_.shape
	print D.shape, D_.shape
	print Y.shape, Y_.shape

	print 'fitting m0...'
	m0 = RandomForestRegressor(n_estimators=10)
	m0.fit(Z_, D_.ravel())

	print 'fitting l0...'
	l0 = RandomForestRegressor(n_estimators=10)
	l0.fit(Z_, Y_.ravel())

	theta = 0.0
	sum_v_sq = 0
	sum_vw = 0

	print 'calculating theta...'
	for index, row in transformed.iterrows():
		print index
		w = row['govt_wins'] - l0.predict(row['x_republican'])
		v = row['x_weat'] - 2*m0.predict(row['x_republican'])
		sum_v_sq += v*v
		sum_vw += w*v

	theta = (1.0/sum_v_sq) * sum_vw
	print 'theta:', theta

def main():
	combined_data_fname = 'data/combined_govern_data.csv'
	regression(combined_data_fname)

if __name__ == "__main__":
	main()