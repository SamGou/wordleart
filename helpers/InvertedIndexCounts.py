from collections import defaultdict
import json 
import os 
def build_inverted_index_with_counts(word_list):
    # Build the index: letter -> {word: count}
    inverted_index_with_counts = defaultdict(dict)
    for word in word_list:
        letter_counts = defaultdict(int)
        for letter in word:
            letter_counts[letter] += 1
        for letter, count in letter_counts.items():
            inverted_index_with_counts[letter][word] = count
    return inverted_index_with_counts

def save_inverted_index_with_counts(inverted_index_with_counts,path):
    # Save to JSON file
    with open(f"{path}", "w") as f:
        json.dump(inverted_index_with_counts, f)
    print("Inverted Index with counts structure saved to disk")
    return 0

def load_inverted_index_with_counts(path):
    # Load the saved json
    with open(f"{path}","r") as f:
        inverted_index_with_counts = json.load(f)
    return inverted_index_with_counts

def words_with_letter_mincount(inverted_index_with_counts,letter, min_count=1):
    # Retrieve words containing at least 'min_count' of a letter
    letter = letter.upper()
    if letter not in inverted_index_with_counts:
        return set()
    return set({word for word, count in inverted_index_with_counts[letter].items() if count >= min_count})

def words_with_letter_maxcount(inverted_index_with_counts,letter, max_count=1):
    # Retrieve words containing at least 'min_count' of a letter
    letter = letter.upper()
    if letter not in inverted_index_with_counts:
        return set()
    return set({word for word, count in inverted_index_with_counts[letter].items() if count <= max_count})


if __name__ == '__main__':
    PATH = 'roots/inverted_index.json'
    if not os.path.exists(PATH):
        build_inverted_index_with_counts()
    inv_index_with_counts = load_inverted_index_with_counts(PATH)
    word_more1a = words_with_letter_mincount(inv_index_with_counts,"J",2)
    word_1a = words_with_letter_maxcount(inv_index_with_counts,"J",1) 
    # print(word_1a)
    print(word_more1a &word_1a )
    
    