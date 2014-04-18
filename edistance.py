# -*- coding: utf-8 -*-


# I don't know which similarity or distance you need to compute.
# Some of distance rely on global distributiton.
# You may need several reduce processes to compute
# Here is an example I proposed for your sparse vector

def convert_keyword_set(keyword_vectors):
    ret = set()
    for key in keyword_vectors:
        ret.add(key)
    return ret

# For example page 1
# for example autom is the stem, and 2 is the number of occurrence
page1_word_vectors = {"autom": 2,
                      "indetif": 1,
                      "postop": 1,
                      "complic": 1}

page1_keyword_set = convert_keyword_set(page1_word_vectors)
page1_hash_id = hash(frozenset(page1_word_vectors.items()))


#  and page 2
page2_word_vectors = {"autom": 1,
                      "postop": 2,
                      "complic": 1,
                      "natural": 1}

page2_keyword_set = convert_keyword_set(page1_word_vectors)
page2_hash_id = hash(frozenset(page2_word_vectors.items()))


def euclidean_distance(page1_word_vectors, page1_keyword_set,
                       page2_word_vectors, page2_keyword_set):
    # for exmaple, we compute the euclidean distance
    inter = set.intersection(page1_keyword_set, page2_keyword_set)
    distance = 0
    for ikey in inter:
        tmp = abs(page1_word_vectors[ikey] - page2_word_vectors[ikey]) ** 2
        distance += tmp
    return distance

ret = euclidean_distance(page1_word_vectors, page1_keyword_set,
                         page2_word_vectors, page2_keyword_set)

dist_matrix = {}
# All distance pairs are independent so that you can easily apply MapReduce framework
dist_matrix[page1_hash_id][page2_hash_id] = ret


# I hope these code will help you
