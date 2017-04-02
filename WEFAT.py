import math
import sys

# func for calcuate cos distance of two vectors
def cos(x,y):
    s = 0
    norm_x_2 = 0
    norm_y_2 = 0
    for i in range(len(x)):
        s += x[i]*y[i]
        norm_x_2 += x[i]**2
        norm_y_2 += y[i]**2
    return 1.0*s/math.sqrt(norm_x_2*norm_y_2)

# func for calculate mean cos distance between w and vectors in X
def mean_cos(w,X):
    return sum(cos(w,x) for x in X)/len(X)

# func for standard deviation between w and vectors in X
def std_dev(w,X):
    s = 0
    # stores temp cos results
    cos_rst = []
    for i in range(len(X)):
        cos_rst.append(cos(w,X[i]))
    cos_avg = sum(cos_rst)/len(cos_rst)
    return math.sqrt(sum((cos_avg-x)**2 for x in cos_rst)/len(cos_rst))

def load_from_glove(X, A, B, Y=[]):
    g_a = []
    g_b = []
    g_x = []
    g_union = []
    g_y = []

    print "loading file"

    for line in open('glove.840B.300d.txt'):
        v = line.strip().split(' ')
        wi = v[0]
        v = [float(a) for a in v[1:]]
        if wi in X:
            g_x.append(v)
        if wi in A:
            g_a.append(v)
        if wi in B:
            g_b.append(v)
        if wi in Y:
            g_y.append(v)

    g_union = g_a + g_b

    print "finished loading"
    return g_a, g_b, g_x, g_y, g_union

def wefat(load_word_vector, resfname = 'result_score'):
    # trained word vectors, common crawl
    file_dir = 'target-attr-words/'
    type_str = 'occupation'
    w_f = open(file_dir + 'target_words-' + type_str)
    a_f = open(file_dir + 'attribute_a-' + type_str)
    b_f = open(file_dir + 'attribute_b-' + type_str)

    # target words
    W = w_f.readlines()[0].strip().split(', ')

    # attribute words
    A = a_f.readlines()[0].strip().split(', ')
    B = b_f.readlines()[0].strip().split(', ')

    # goal: calculate s(w, A, B) using formula at pg.10 Semantics derived automatically from language corpora necessarily contain human biases

    # 1. traverse the glove file and get the cooresponding vectors
    g_a, g_b, g_x, g_y, g_union = load_word_vector(W, A, B)

    # 2. get mean(cos(w,a)), mean(cos(w,b)
    # 3. calculate std-dev(cos(w,x))
    s_v = []
    # s values:
    for w in g_x:
        s_v.append((mean_cos(w,g_a)-mean_cos(w,g_b))/std_dev(w,g_union))
    resdir = 'result-score/'
    print 'saving result score to...' + resdir + resfname
    resfile = open(resdir + resfname + '.txt', 'w')
    for item in s_v:
        resfile.write(str(item) + ', ')
    resfile.close()

    w_f.close()
    a_f.close()
    b_f.close()

def s_sum_word_attrs(target_words, g_a, g_b):
    # sigma_x s(x, A, B)
    s = 0
    for w in target_words:
        s += mean_cos(w, g_a) - mean_cos(w, g_b)
    return s

def std_dev_score(g_union, g_a, g_b):
    cos_rst = []
    for i in range(len(g_union)):
        cos_rst.append(mean_cos(g_union[i], g_a) - mean_cos(g_union[i], g_b))
    cos_avg = sum(cos_rst)/len(cos_rst)
    return math.sqrt(sum((cos_avg-x)**2 for x in cos_rst)/len(cos_rst))

def weat(load_word_vector, resfname = 'result_score'):
    file_dir = 'target-attr-words/'
    type_str = 'artsci2'
    x_f = open(file_dir + 'target_words_x-' + type_str)
    y_f = open(file_dir + 'target_words_y-' + type_str)
    a_f = open(file_dir + 'attribute_a-' + type_str)
    b_f = open(file_dir + 'attribute_b-' + type_str)

    # target words
    X = x_f.readlines()[0].strip().split(', ')
    Y = y_f.readlines()[0].strip().split(', ')

    # attribute words
    A = a_f.readlines()[0].strip().split(', ')
    B = b_f.readlines()[0].strip().split(', ')

    # load corresponding word vectors
    g_a, g_b, g_x, g_y, g_union = load_word_vector(X, A, B, Y)

    score = s_sum_word_attrs(g_x, g_a, g_b) - s_sum_word_attrs(g_y, g_a, g_b)

    effect_size = s_sum_word_attrs(g_x, g_a, g_b)/len(g_x) - s_sum_word_attrs(g_y, g_a, g_b)/len(g_y)
    effect_size /= std_dev_score(g_union, g_a, g_b)

    print score, effect_size

    return score


def main():

    if len(sys.argv) != 2:
        print 'usage: python WEFAT.py [-wefat|-weat]'
    elif sys.argv[1] == '-wefat':
        wefat(load_from_glove)
    elif sys.argv[1] == '-weat':
        weat(load_from_glove)


if __name__ == "__main__":
    main()
