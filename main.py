import copy
import os
import random
from helpers.FindMatches import findMatchingWords
from helpers.InvertedIndexCounts import load_inverted_index_with_counts, words_with_letter_mincount,words_with_letter_maxcount,build_inverted_index_with_counts
from helpers.SerialiseRoot import loadRoot
from helpers.Trie import buildTrie
from helpers.GetCurrentDaySolution import get_today_solution
from helpers.SetOperations import combine_sets_intersect, combine_sets_union
import json

def main(problem_str:str):
    # Load the word data structures
    PATH_TRIE = "./roots/trie_root.json"
    if os.path.exists(PATH_TRIE):
        root = loadRoot(PATH_TRIE)

    PATH_INVIND = "./roots/inverted_index.json"
    if os.path.exists(PATH_INVIND):
        inverted_index = load_inverted_index_with_counts(PATH_INVIND)

    with open("./DB/combined_wordlist.txt", "r") as f:
        OVERALL_WORD_SET = set([line.strip().upper() for line in f if len(line.strip()) == 5])
            
    # Get todays solution
    todays_word,letter_pos,counter = get_today_solution()
    print("TODAYS ANSWER", todays_word)
    
    # Modify response string to match grid
    def _problemstr2grid(s):
        return [s[i:i+5] for i in range(0, 30, 5)]
    
    problem_grid = _problemstr2grid(problem_str)
    solution=[""]*6
    print("PROBLEM GRID: ",problem_grid)
    
    solved = False
    unsolvable = False
    for n,line in enumerate(problem_grid):
        print(f"SOLUTION: {solution}")
        # if already solved, exit loop
        if solved or unsolvable:
            break
        
        # if line is a full green line, just return todays answer
        if line == 'G'*5:
            solution[n] = todays_word
            solved = True
            continue
        
        elif line == '#'*5:
            # NOTE: for fully #####, find all words that include at least 1 count of the letters in todays words and .difference iteratively from the total set
            todays_letters = set(todays_word)
            set_list = []
            for letter in todays_letters:
                set_list.append(words_with_letter_mincount(inverted_index,letter,1))
            ignore_word_list = combine_sets_union(set_list)
            available_word_list = OVERALL_WORD_SET - ignore_word_list # Remove the list of words which contain at least on letter from todays answer in any position  
            solution[n] = random.sample(list(available_word_list),1)[0]
            continue
        
        else:
            current_word_set = copy.copy(OVERALL_WORD_SET)
            for pos,block in enumerate(line):
                # If current wordset is empty then it is unsolvable
                if not current_word_set:
                    unsolvable = True
                    break
                
                # Rebuild the Trie per iteration to reduce search space
                if pos == 0:
                    root_reduced = copy.deepcopy(root) # just copy existing root with all words present for first iteration
                    # inverted_index_reduced = copy.deepcopy(inverted_index)
                else: 
                    root_reduced = buildTrie(current_word_set) # rebuild it based on previous constraints
                    # inverted_index_reduced = build_inverted_index_with_counts(current_word_set)
                    
                # If its green we know the exact letter and position
                if block == "G":
                    constraint = letter_pos[pos]
                    available_word_set = findMatchingWords(trieRoot=root_reduced,constraints=[constraint])
                    current_word_set.intersection_update(available_word_set)
                    # Take away number of remaining counts
                    counter[constraint[0]] -= 1
                
                # If orange we know it can be only a select few letters
                elif block == "O":
                    correct_letter = letter_pos[pos][0] # correct letter at current position
                    letters_in_todays_word = set({letter:i for letter,i in counter.items() if i > 0}.keys()) # set of all remaining letters in todays answer
                    available_letters = letters_in_todays_word.difference(correct_letter) # Get available letters 
                    
                    constraint_in_pos = [(i,pos) for i in available_letters]
                    set_list = []
                    for constraint in constraint_in_pos:
                        set_list.append(findMatchingWords(trieRoot=root_reduced,constraints=[constraint]))
                    available_word_set = combine_sets_union(set_list)
                    
                    current_word_set.intersection_update(available_word_set)
                
                # If gray it can be anything but what is in today's answer
                elif block == "#":
                    todays_letters = set(todays_word)
                    constraint_in_pos = [(i,pos) for i in todays_letters]
                    set_list = []
                    for constraint in constraint_in_pos:
                        set_list.append(findMatchingWords(trieRoot=root_reduced,constraints=[constraint]))
                    ignore_word_set = combine_sets_union(set_list)
                    current_word_set.difference_update(ignore_word_set)
            
            # Get all with matching counts if its final
            if line == 'O'*5:
                inverted_index_count_match = build_inverted_index_with_counts(current_word_set)
                set_list = []
                for letter,i in counter.items():
                    set_list.append(words_with_letter_maxcount(inverted_index_count_match,letter=letter,max_count=i))
                available_word_set = combine_sets_intersect(set_list)
                current_word_set.intersection_update(available_word_set) 
            
            # Draw a word from the remaining available word list and append to solution
            if not current_word_set:
                unsolvable = True
                break
            solution[n] = random.sample(list(current_word_set),1)[0]

    # TODO think about implementing logic which handles cases where if say answer is NOVEL and the input is NEVER the code will be G#GG# because the E is in the correct position to begin with.
    # If the answer was NEEDO put NEVER would be GG#O#
    # This will expand the list of available words and make solutions more likely
    if unsolvable:
        return json.dumps({"Response":500,"Message":"Unsolvable with current word and grid colours", "Solution":[]})

    return json.dumps({"Response":200, "Message":"Solution Found!", "Solution":solution})
