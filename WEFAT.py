import math

# trained word vectors, common crawl
glove = open('glove.840B.300d.txt')
w_f = open('target_words')
a_f = open('attribute_a')
b_f = open('attribute_b')

# target words
W = w_f.readlines()[0].strip().split(', ')

# attribute words
A = a_f.readlines()[0].strip().split(', ')
B = b_f.readlines()[0].strip().split(', ')

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
    return sum((cos_avg-x)**2 for x in cos_rst)/len(cos_rst)

# goal: calculate s(w, A, B) using formula at pg.10 Semantics derived automatically from language corpora necessarily contain human biases

# 1. traverse the glove file and get the cooresponding vectors
g_a=[]
g_b=[]
g_x=[]
g_w=[]

print "loading file"
lines = glove.readlines()

for l in lines:
    v = l.strip().split(' ')
    wi = v[0]
    v = [float(a) for a in v[1:]]
    for w in W:
        if wi == w:
            g_w.append(v)
    for w in A:
        if wi == w:
            g_a.append(v)
    for w in B:
        if wi == w:
            g_b.append(v)

g_x = g_a + g_b

print "finished loading"
#print g_a
#print g_b
#print g_x

# 2. get mean(cos(w,a)), mean(cos(w,b)
# 3. calculate std-dev(cos(w,x))
s_v = []
# s values:
for w in g_w:
    s_v.append((mean_cos(w,g_a)-mean_cos(w,g_b))/std_dev(w,g_x))
print s_v

w_f.close()
a_f.close()
b_f.close()
