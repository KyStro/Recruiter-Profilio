'''
Kyle Strokes
Computational HW 3
4/16/19
'''

import math

'''
Calculates the entropy of given probability distribution dictionary
'''
def entropy(prob_dict):
    entropy = 0
    for key, prob in prob_dict.items():
        info = prob * math.log((1/prob), 2)
        entropy += info
    return entropy

'''
Returns the normalized probability distribution of the n-grams
of given length n, located in given filename file
'''
def ngram_dist(file, n):
    ngram_dist = {}
    file = open(file)
    words = file.read().strip("\n")
    grams = [words[i:i+n] for i in range(len(words) - n + 1)]
    total = len(grams)
    for gram in grams:
        if gram not in ngram_dist:
            ngram_dist[gram] = 1
        else:
            ngram_dist[gram] = ngram_dist[gram] + 1
    for key in ngram_dist:
        ngram_dist[key] = ngram_dist[key] / total
    return ngram_dist

def main():
    '''
    print("H1: " + str(entropy(ngram_dist("hp6.txt", 1))))
    print("H2: " + str(entropy(ngram_dist("hp6.txt", 2)) - 
                       entropy(ngram_dist("hp6.txt", 1))))
    print("H3: " + str(entropy(ngram_dist("hp6.txt", 3)) - 
                       entropy(ngram_dist("hp6.txt", 2))))
    '''

main()