# trained word vectors, common crawl
glove = open('glove.42B.300d.txt')
w_f = open('target_words')
a_f = open('attribute_a')
b_f = open('attribute_b')

# target words
W = w_f.readlines().strip().split(' ')

# attribute words
A = a_f.readlines().strip().split(' ')
B = b_f.readlines().strip().split(' ')

# union of A & B
X = A+B
N = len(W)

# goal: calculate s(w, A, B) using formula at pg.10 Semantics derived automatically from language corpora necessarily contain human biases

# 1. traverse the glove file and get the cooresponding vectors
g_a=[]
g_b=[]
g_w=[]
lines = glove.readline()
for l in lines:
    v = l.strip().split(' ')
    wi = v[0]
    v = v[1:]
    for w in W:
        if wi == w:
            g_w.append([w]+v)
    for w in A:
        if wi == w:
            g_a.append([w]+v)
    for w in B:
        if wi == w:
            g_b.append([w]+v)
# 2. get mean(cos(w,a)), mean(cos(w,b)

# 3. calculate std-dev(cos(w,x)

w_f.close()
a_f.close()
b_f.close()
