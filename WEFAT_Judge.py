import gensim
import os
from glob import glob
from zipfile import ZipFile
import sys
import re
import WEFAT

# set default utf8 encoding to open file
reload(sys)
sys.setdefaultencoding('utf8')

# sentence generator from text
class Sentence(object):
	def __init__(self, dirname, caseid_set=[]):
		self.dirname = dirname
		self.caseid_set = caseid_set
		# iterate through all the zip files (different years)
		self.zipfiles = glob(dirname + '/*zip')

	# normalization
	def normalize(self, text):
		# split on non-alphanumeric characters(space and punctuation)
		norm_words = re.split('\W+', text.lower())

		# can also remove stopwords

		return norm_words

	# get word from text
	def __iter__(self):

		for zfname in self.zipfiles:

			zfile = ZipFile(zfname)
			members = zfile.namelist()
			# filter text in specific years
			# year = int(zfname.split('/')[-1][:-4])
			# print year, year < 1980
			# if year < 1980:
			# 	continue
			# iterate through all texts in zip file
			for fname in members:
				# use majority opinions text
				if not fname.endswith('-maj.txt'):
					continue
				caseid = fname.split('/')[-1][:-4].split('-')[0]

				# if there is a specified case set, then only process cases in the set
				if len(self.caseid_set) != 0 and caseid not in self.caseid_set:
					continue
				print fname, caseid

				# open file and read line by line
				with zfile.open(fname) as f:
					for line in f:
						yield self.normalize(line)

class WVModel(object):

	def __init__(self, text_dir, judge_name = 'all', caseid_set = []):
		self.text_dir = text_dir
		self.model_name = 'tmp/model-' + judge_name
		self.judge_name = judge_name
		self.caseid_set = caseid_set

	def train_model(self, min_count_ = 5):
		# generate words from text
		sentences = Sentence(self.text_dir, self.caseid_set)
		# train word vectors
		print 'training model...' + self.model_name
		model = gensim.models.Word2Vec(sentences, min_count = min_count_)
		# save model
		print 'saving model...' + self.model_name
		model.save(self.model_name)

	def load_word_vector(self, X, A, B, Y=[]):
		g_a = []
		g_b = []
		g_x = []
		g_y = []
		g_union = []

		# get word vectors from model
		for x in X:
			if x in self.model.wv.vocab:
				g_x.append(self.model[x])
			else:
				print x, 'not in vocabulary'
		for a in A:
			if a in self.model.wv.vocab:
				g_a.append(self.model[a])
			else:
				print a, 'not in vocabulary'
		for b in B:
			if b in self.model.wv.vocab:
				g_b.append(self.model[b])
			else:
				print b, 'not in vocabulary'
		for y in Y:
			if y in self.model.wv.vocab:
				g_y.append(self.model[y])
			else:
				print y, 'not in vocabulary'

		g_union = g_a + g_b

		return g_a, g_b, g_x, g_y, g_union

	def use_model(self):
		# load model
		self.model = gensim.models.Word2Vec.load(self.model_name)

		# use WEFAT method
		WEFAT.wefat(self.load_word_vector)

	def calc_weat(self):
		# load model
		self.model = gensim.models.Word2Vec.load(self.model_name)

		# use WEAT method
		return WEFAT.weat(self.load_word_vector, self.judge_name)		

def main():
	# directory for text data
	text_dir = 'cleaned'

	wvmodel = WVModel(text_dir)

	if len(sys.argv) != 2:
		print 'usage: python WEFAT_Judge.py [-t|-u]'
		print '-t: train model; -u: use model'
	elif sys.argv[1] == '-t':
		wvmodel.train_model()
	elif sys.argv[1] == '-u':
		wvmodel.use_model()


if __name__ == "__main__":
	main()
