import pickle
import json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.isWord = False
        
   
def buildTrie(wordList):
    root = TrieNode()
    for word in wordList:
        node = root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.isWord = True
    return root


def serializeTrie(node):
    return {
        'isWord': node.isWord,
        'children': {letter: serializeTrie(child) for letter, child in node.children.items()}
    }

def deserializeTrie(data):
    node = TrieNode()
    node.isWord = data['isWord']
    for letter, child_data in data['children'].items():
        node.children[letter] = deserializeTrie(child_data)
    return node


if __name__ == "__main__":
    a = buildTrie(set(['JINKS', 'WARPS', 'DWARF', 'TETHS', 'ALGUM', 'EXIST', 'DIENE', 'HONDS', 'FLAVA', 'CHILD', 'DEAWY', 'BELOW', 'THYME', 'CLAST', 'AGROS', 'PACED', 'REWON', 'TESTE', 
               'UNWET', 'KOBOS', 'MAUTS', 'DINKS', 'CLAIM', 'BOUGH', 'MOLAR', 'VAREC', 'YEGGS', 'FLASK', 'ALIEN', 'FUERO', 'CREPT', 'BRAID', 'WAINS', 'DOSEH', 'VIZIR', 'REGMA']))
    print(a.children["J"].children.items())