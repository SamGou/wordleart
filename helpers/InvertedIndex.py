import json 

PATH = 'roots/inverted_index.json'
with open("./DB/combined_wordlist.txt", "r") as f:
    words = [line.strip().upper() for line in f if len(line.strip()) == 5]
    
words = words[:20]
# Build the inverted index
inverted_index = {}
for word in words:
    for letter in set(word):  # set() avoids duplicates
        if letter not in inverted_index:
            inverted_index[letter] = set()
        inverted_index[letter].add(word)
        
# Save to JSON file
print(inverted_index)
    
# Retrieve words containing a letter
def words_with_letter(letter):
    return inverted_index.get(letter.upper(), set())

if __name__ == "__main__":
    print(words_with_letter("A"))