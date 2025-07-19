from helpers.InvertedIndexCounts import load_inverted_index_with_counts, words_with_letter_maxcount, words_with_letter_mincount
from helpers.FindMatches import findMatchingWords
from helpers.SerialiseRoot import loadRoot,buildTrie
from helpers.InvertedIndexCounts import build_inverted_index_with_counts
from helpers.Trie import TrieNode
from collections import defaultdict

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

def update_curr_struct_intersect(current_word_set:set,available_word_set:set):
    new_word_set = current_word_set.intersection(available_word_set)
    reduced_trie_root = buildTrie(new_word_set)
    reduced_inv_index = build_inverted_index_with_counts(new_word_set)
    return new_word_set,reduced_trie_root,reduced_inv_index

if __name__ == '__main__':
    set_list = [words_with_letter_mincount(inv_idx,"A",3),words_with_letter_mincount(inv_idx,"T",1)]
    print(combine_sets_intersect(set_list))