import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.FindMatches import findMatchingWords
from helpers.InvertedIndexCounts import load_inverted_index_with_counts,words_with_letter_count
from helpers.SerialiseRoot import loadRoot
from helpers.Trie import buildTrie

import os
import timeit
import random 
import numpy as np



def generateLetterPosPairs():
    LETTERS = ["C","T","S","A","E","O","U","Y","I"]
    POSITIONS = [0,1,2,3,4]
    NUM_CONSTRAINTS = 3
    ret_pairs = []
    
    # Sample without replacement three letters and positions
    letter = random.sample(LETTERS,NUM_CONSTRAINTS)
    pos = random.sample(POSITIONS,NUM_CONSTRAINTS)
    
    # Append constraint combinations to return list
    for pair in zip(letter,sorted(pos)):
        ret_pairs.append(pair)
        
    return ret_pairs


def runTrie():
    VERB = False
    PATH = "./roots/trie_root.json"
    constraints = generateLetterPosPairs()
    if VERB:
        print(f"Constraints: {constraints}")
    root = loadRoot(PATH)
    return findMatchingWords(constraints=constraints, trieRoot=root)

def runWordsWithLetterCount():
    PATH = './roots/inverted_index.json'
    inverted_index = load_inverted_index_with_counts(PATH)
    return words_with_letter_count(inverted_index,"A",3)

def runReducedSearchSet_ReduceInside():
    # Inv Idx
    PATH_IDX = './roots/inverted_index.json'
    inverted_index = load_inverted_index_with_counts(PATH_IDX)
    # Reduce search area
    reduced_space = words_with_letter_count(inverted_index, letter="E",min_count=2)
    
    # Trie
    constraints = [("A",1)]
    root = buildTrie(reduced_space)
    return findMatchingWords(constraints=constraints, trieRoot=root)    
    
# Time multiple executions and get the average
print("Running TRIE timing...")
elapsed = timeit.timeit(runTrie, number=1000) / 1000
print(f"Average time per run TRIE: {elapsed} seconds")

# Time invertedIndex        
print("Running InvIdx timing...")
elapsed = timeit.timeit(runWordsWithLetterCount, number=1000) / 1000
print(f"Average time per run InvIdx: {elapsed} seconds")

# Time Trie with reduced search space        
print("Running TRIE(REDUCED)...")
elapsed = timeit.timeit(runReducedSearchSet_ReduceInside, number=1000) / 1000
print(f"Average time per run TRIE(REDUCED): {elapsed} seconds")
