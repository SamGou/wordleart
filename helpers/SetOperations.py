from helpers.InvertedIndexCounts import load_inverted_index_with_counts, words_with_letter_maxcount, words_with_letter_mincount
from helpers.FindMatches import findMatchingWords
from helpers.SerialiseRoot import loadRoot

PATH_INVIDX = './roots/inverted_index.json'
PATH_ROOT = './roots/trie_root.json'

root = loadRoot(PATH_ROOT)
inv_idx = load_inverted_index_with_counts(PATH_INVIDX)

def combine_sets_intersect(set_list):
    ret_set = set()
    for i in range(len(set_list)):
        if i == 0:
            ret_set.update(set_list[i])
        else:
            ret_set.intersection_update(set_list[i])
    return ret_set

def combine_sets_union(set_list):
    ret_set = set()
    for i in range(len(set_list)):
        ret_set.update(set_list[i])
    return ret_set


if __name__ == '__main__':
    set_list = [words_with_letter_mincount(inv_idx,"A",3),words_with_letter_mincount(inv_idx,"T",1)]
    print(combine_sets_intersect(set_list))