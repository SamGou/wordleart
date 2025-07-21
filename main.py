import copy
import os
import random
from helpers.FindMatches import findMatchingWords
from helpers.InvertedIndexCounts import load_inverted_index_with_counts, words_with_letter_mincount,words_with_letter_maxcount,build_inverted_index_with_counts
from helpers.SerialiseRoot import loadRoot
from helpers.Trie import buildTrie
from helpers.GetCurrentDaySolution import get_today_solution
from helpers.SetOperations import combine_sets_intersect, combine_sets_union,update_curr_struct_intersect,update_curr_struct_difference
from helpers.DeconstructLine import deconstruct_line
from helpers.WordSearch import letter_pos_combinations_orange
from collections import Counter
import itertools
import json
from fastapi.responses import JSONResponse


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
    # todays_word -> "NEVER"
    # letter_pos -> [("N",0),("E",1),("V",2),("E",3),("R",4)]
    # Counter_const -> {"N":1,"E":2,"V":1,"R":1}
    todays_word,letter_pos,counter_const = get_today_solution()
    print("TODAYS ANSWER", todays_word)
    
    # Modify response string to match grid
    def _problemstr2grid(s):
        return [s[i:i+5] for i in range(0, 30, 5)]
    
    problem_grid = _problemstr2grid(problem_str)
    solution=[""]*6
    print("PROBLEM GRID: ",problem_grid)
    
    solved = False
    unsolvable = False
    prev_sols = {i:"" for i in problem_grid}
    for n,line in enumerate(problem_grid):
        # if already solved, exit loop
        if solved or unsolvable:
            break
        
        elif line != "#"*5 and prev_sols[line] != '':
            solution[n] = prev_sols[line]
            
                  
        # if line is a full green line, just return todays answer
        elif line == 'G'*5:
            solution[n] = todays_word
            solved = True
            
        
        elif line == '#'*5:
            # NOTE: for fully #####, find all words that include at least 1 count of the letters in todays words and .difference iteratively from the total set
            todays_letters = set(todays_word)
            set_list = []
            for letter in todays_letters:
                set_list.append(words_with_letter_mincount(inverted_index,letter,1))
            ignore_word_list = combine_sets_union(set_list)
            available_word_list = OVERALL_WORD_SET - ignore_word_list # Remove the list of words which contain at least on letter from todays answer in any position  
            solution[n] = random.sample(list(available_word_list),1)[0]
            
        else:
            # Init
            root_reduced = copy.deepcopy(root) # Structure to help find words with letters in exact positions
            inverted_index_reduced = copy.deepcopy(inverted_index) # Structure to help with finding min/max number of letters in a word or a word with any amount of said letter
            current_word_set = copy.copy(OVERALL_WORD_SET) # {"WORDS","WORDS"}
            temp_counter = copy.copy(counter_const) # {"N":1,"E":2,"V":1,"R":1}
            block_map = deconstruct_line(line) # {"G":[],"O":[],"#":[]}

            # Iterate through G's first
            for pos in block_map["G"]:
                constraint = letter_pos[pos]
                available_word_set = findMatchingWords(trieRoot=root_reduced,constraints=[constraint])
                current_word_set,root_reduced,inverted_index_reduced = update_curr_struct_intersect(current_word_set,available_word_set)
                temp_counter[constraint[0]] -= 1
            
            # Orange
            # Generate orange potential combinations
            if block_map["O"]:
                orange_pos = block_map["O"]
                combinations = letter_pos_combinations_orange(orange_pos=orange_pos,
                                                            letter_pos=letter_pos,
                                                            counter=temp_counter)
                orange_set_list = []
                for combo in combinations:
                    constraint_list = [(letter,position) for letter,position in zip(combo,orange_pos)]
                    combination_set_list = []
                    for constraint in constraint_list:
                        combination_set_list.append(findMatchingWords(trieRoot=root_reduced,constraints=[constraint]))
                    # Intersect these sets of potential words with letters in exact positions
                    orange_set_list.append(combine_sets_intersect(combination_set_list))
                # Union all potential words
                all_possible_orange_words = combine_sets_union(orange_set_list)
                # Intersect with current_word_set
                current_word_set,root_reduced,inverted_index_reduced = update_curr_struct_intersect(current_word_set,all_possible_orange_words)
                # End the search if unsolvable
                if not current_word_set:
                    unsolvable = True
                    break
                
            # Gray
            if block_map["#"]:
                gray_pos = block_map["#"]

                blacklist = set()
                for potential_word in current_word_set:
                    O_letters = Counter("".join([potential_word[i] for i in block_map["O"]]))
                    remaining_letters = temp_counter - O_letters
                    remaining_letters = set(remaining_letters.keys())
                    
                    # Build constraint list
                    constraint_combinations = list(itertools.product(remaining_letters, gray_pos))
                    
                    # Add additional constraints to not override Orange letters that come earlier
                    for O_pos in block_map["O"]:
                        if O_pos > 0: # Ignore if its the first letter
                            constraint_combinations += itertools.product(potential_word[O_pos],range(O_pos))
                        else:
                            continue
                        
                    for letter,pos in constraint_combinations:
                        if letter == potential_word[pos]:
                            blacklist.add(potential_word)
                            break
                    
                current_word_set.difference_update(blacklist)
                
            if not current_word_set:
                unsolvable = True
                break
            
            solution[n] = random.sample(list(current_word_set),1)[0]
            if prev_sols[line] == '':
                prev_sols[line] = solution[n]

    if unsolvable:
        print(solution)
        return JSONResponse({"Response":500,"Message":"Unsolvable with current word and grid colours", "Solution":solution})
    print(solution)
    return JSONResponse({"Response":200, "Message":"Solution Found!", "Solution":solution})

if __name__ == "__main__":
    string = "".join(['GG#GG', '#####', '#####', '#####', '#####', '#####'])
    print(main(string))
    
    # GNOME - ENEMY #G#G#