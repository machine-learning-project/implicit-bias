import pandas
import numpy as np
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
import statsmodels.api as sm
from sklearn.model_selection import KFold
import math

def regression_cross_valid(fname):
	df = pandas.read_csv(fname, delimiter=',', skiprows=1,
		 names=["caseid", "year", "songername", "songerfirstname", "circuit", "govt_wins", "x_republican", "x_weat", 'amon', 'ayear', 'city', 'state', 'aba', 
		'party', 'ageon', 'sother', 'yearb', 'csb', 'gender', 'religion', 'ls'],
		 dtype={"year":int, "circuit":int, "govt_wins":float, "x_republican":float, "x_weat":float})
	
	print "loading", fname, df.shape

	demean = lambda df: df - df.mean()
	groupby_ct = df.groupby(['year', 'circuit'])
	transformed = groupby_ct.transform(demean)

	# output
	Y = transformed['govt_wins'].values
	# treatment variable
	D = transformed['x_weat'].values
	# control variable
	Z = transformed[['x_republican', 'amon', 'ayear', 'city', 'state', 'aba', 
		'party', 'ageon', 'sother', 'yearb', 'csb', 'gender', 'religion', 'ls']].values

	# treatment effect
	TEs = []
	# standard error
	STDEs = []
	K = 5
	print "sample splitting: ", K
	k_fold = KFold(n_splits=K)
	for train, test in k_fold.split(Y):
		D_aux = D[train]
		Y_aux = Y[train]
		Z_aux = Z[train]
		Z_ = Z[test]
		D_ = D[test]
		Y_ = Y[test]
		param, tvalue, se = regression(D_aux, D_, Y_aux, Y_, Z_aux, Z_)
		TEs.append(param[0])
		STDEs.append(se[0])

	# average treatment effect
	ATE = sum(TEs)/float(len(TEs))
	# standard error
	STDE = 0.0
	for i in range(len(TEs)):
		STDE += (STDEs[i]**2 + (TEs[i] - ATE)**2)
	STDE /= float(len(STDEs))

	print "average treatment effect:", ATE
	print "standard error:", math.sqrt(STDE)

def regression(D_aux, D_, Y_aux, Y_, Z_aux, Z_):

	print 'fitting m0...'
	# m0 = MLPRegressor()
	m0 = RandomForestRegressor(n_estimators=10)
	m0.fit(Z_aux, D_aux)

	print 'fitting l0...'
	l0 = RandomForestRegressor(n_estimators=10)
	l0.fit(Z_aux, Y_aux)

	print 'calculating residualization...'
	
	W = Y_.reshape(Y_.shape[0]) - l0.predict(Z_)
	V = D_.reshape(D_.shape[0]) - m0.predict(Z_)

	# calculating theta using OLS
	print 'fitting OLS...'
	model = sm.OLS(W,V)
	results = model.fit()
	print "params", results.params[0]
	print "tvalues", results.tvalues[0]
	print "stderr", results.bse[0], results.params/results.tvalues

	return results.params, results.tvalues, results.bse


def main():
	combined_data_fname = 'data/combined_govern_data.csv'
	regression_cross_valid(combined_data_fname)

if __name__ == "__main__":
	main()