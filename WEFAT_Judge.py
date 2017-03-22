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
	def __init__(self, dirname):
		self.dirname = dirname
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
			# iterate through all texts in zip file
			for fname in members:
				# use majority opinions text
				if not fname.endswith('-maj.txt'):
					continue
				print fname	            
				# open file and read line by line
				with zfile.open(fname) as f:
					for line in f:    
						yield self.normalize(line)

class WVModel(object):

	def __init__(self, text_dir):
		self.text_dir = text_dir
		self.model_name = 'tmp/mymodel'

	def train_model(self):
		# generate words from text
		sentences = Sentence(self.text_dir)
		# train word vectors
		print 'training model...'
		model = gensim.models.Word2Vec(sentences)
		# save model
		print 'saving model...'
		model.save(self.model_name)

	def load_word_vector(self, W, A, B):
		g_a = []
		g_b = []
		g_w = []
		g_x = []

		# get word vectors from model
		for w in W:
			if w in self.model.wv.vocab:
				g_w.append(self.model[w])
		for a in A:
			if a in self.model.wv.vocab:
				g_a.append(self.model[a])
		for b in B:
			if b in self.model.wv.vocab:
				g_b.append(self.model[b])			

		g_x = g_a + g_b

		return g_a, g_b, g_x, g_w

	def use_model(self):
		# load model
		self.model = gensim.models.Word2Vec.load(self.model_name)

		# use WEFAT method
		WEFAT.wefat(self.load_word_vector)

def main():
	# directory for text data 
	text_dir = 'cleaned'

	wvmodel = WVModel(text_dir)
	wvmodel.train_model()
	# wvmodel.use_model()

if __name__ == "__main__":
	main()


