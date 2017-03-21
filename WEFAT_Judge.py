import gensim
import os
from glob import glob
from zipfile import ZipFile
import sys  
import re

# set default utf8 encoding to open file
reload(sys)  
sys.setdefaultencoding('utf8')

class Sentence(object):
	def __init__(self, dirname):
		self.dirname = dirname

	# normalization
	def normalize(self, text):
		# split on non-alphanumeric characters(space and punctuation)
		norm_words = re.split('\W+', text.lower())
		return norm_words

	# get word from text
	def __iter__(self):
		# iterate through all the zip files (different years)
		os.chdir(self.dirname)
		zipfiles = glob('*zip')

		for zfname in zipfiles:
			zfile = ZipFile(zfname)
			members = zfile.namelist()
			# iterate through all texts in zip file
			for fname in members:
				# use majority opinions text
				if not fname.endswith('-maj.txt'):
					continue
	            # open file and read line by line
				with zfile.open(fname) as f:
					for line in f:      
						yield self.normalize(line)

def train_model(text_dir):
	# generate words from text
	sentences = Sentence(text_dir)

	# train word vectors
	model = gensim.models.Word2Vec(sentences)
	model.save(model_name)

def use_model():
	# load model
	model = gensim.models.Word2Vec.load(model_name)

	w_f = open('target_words')
	a_f = open('attribute_a')
	b_f = open('attribute_b')

	# target words
	W = w_f.readlines()[0].strip().split(', ')

	# attribute words
	A = a_f.readlines()[0].strip().split(', ')
	B = b_f.readlines()[0].strip().split(', ')

	# unfinished
	# use similarity() to measure the similarity between word vectors
	# model.similarity()


text_dir = 'cleaned'
model_name = 'mymodel'
train_model(text_dir)




