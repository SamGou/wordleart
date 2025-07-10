import pickle
import json
from helpers.Trie import buildTrie, TrieNode, serializeTrie, deserializeTrie

# Save the Trie
# TODO implement into class so that I can call and save easily

def writeRoot(path):
    # Build Trie    
    with open("./DB/combined_wordlist.txt", "r") as f:
        words = [line.strip().upper() for line in f if len(line.strip()) == 5]
    trie_root = buildTrie(words)
    
    
    # Serialize the trie to a Python dict
    serialized_trie = serializeTrie(trie_root)

    # Save to JSON file
    with open(f"{path}", "w") as f:
        json.dump(serialized_trie, f)
        
def loadRoot(path):
    # Load from JSON file
    with open(f"{path}", "r") as f:
        loaded_data = json.load(f)
    
    # Deserialize back to a TrieNode object
    trie_root = deserializeTrie(loaded_data)
    return trie_root


if __name__ == "__main__":
    PATH = './roots/trie_root.json'
    # Write to disk
    writeRoot(PATH)
    
    
    