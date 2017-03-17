import gensim
import os
from glob import glob
from zipfile import ZipFile
import sys  

# set default utf8 encoding to open file
reload(sys)  
sys.setdefaultencoding('utf8')

# normalize word
def normalize(text):
	norm_words = []
	for word in text:
		norm_words.append(word.lower())
	return norm_words

# get word from text
def get_words(text_dir):
	# iterate through all the zip files (different years)
	os.chdir(text_dir)
	zipfiles = glob('*zip')

	for zfname in zipfiles:
		zfile = ZipFile(zfname)
		members = zfile.namelist()
		# iterate through all texts in zip file
		for fname in members:
			# use majority opinions text
			# if not fname.endswith('-maj.txt'):
				# continue
            # open file and read line by line
			with zfile.open(fname) as f:
				for line in f:      
					yield normalize(line.split())

def train_model(text_dir):
	# generate words from text
	words = get_words(text_dir)
	
	# train word vectors
	model = gensim.models.Word2Vec(words)
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




