from helpers.TrieSearch import searchTrie
from helpers.Trie import TrieNode

def findMatchingWords(trieRoot:TrieNode, constraints:tuple[str]) -> list[str]:
    result = []
    searchTrie(trieRoot, constraints, 0, "", result)
    return set(result)