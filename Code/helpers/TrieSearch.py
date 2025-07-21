from helpers.Trie import TrieNode
def searchTrie(node:TrieNode, constraints:tuple[str], pos:int, currentWord:str, result:list[str]):
    if pos == 5:
        if node.isWord:
            result.append(currentWord)
        return
    # Check if there is a constraint for this position
    letter_constraint = None
    for (letter, cpos) in constraints:
        if cpos == pos:
            letter_constraint = letter
            break
    if letter_constraint:
        if letter_constraint in node.children:
            searchTrie(node.children[letter_constraint], constraints, pos+1, currentWord+letter_constraint, result)
    else:
        for letter, child in node.children.items():
            searchTrie(child, constraints, pos+1, currentWord+letter, result)