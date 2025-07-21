import copy

def letter_pos_combinations_orange(orange_pos,letter_pos,counter):
    """Generate all possible combinations of letters in the specified positions
    Takes green positions into account and actively keeps track of letters left to use (words with multiple letters)

    Args:
        orange_pos (_type_): _Static_ Positions of orange blocks -> [1,3] -> positions 1 & 3
        letter_pos (_type_): _Static_ List of letters and their positions 
        counter (_type_): _Dynamic_ Dict of letters and their counts

    Returns:
        List: "RM" means _"R"_ in `orange_pos[0]` and _"M"_ in `orange_pos[1]`
    """
    result = []
    MAX_DEPTH = len(orange_pos) # max depth will be equal to the amount of orange letters we want to find
    ORANGE_POS_MAP = {depth:orange_pos for depth,orange_pos in zip(range(MAX_DEPTH),orange_pos)} # Avaialble letters are depth dependent
    
    def _build_tree(path, depth, max_depth,counter,letter_pos,orange_pos_map):
        if depth == max_depth:
            result.append(''.join(path))
            return

        green_letter = letter_pos[orange_pos_map[depth]][0]
        for letter in {letter:i for letter,i in counter.items() if i > 0}:
            if letter == green_letter:
                continue          
            temp_counter = copy.copy(counter)
            temp_counter[letter] -= 1
            temp_counter = {letter:i for letter,i in temp_counter.items() if i > 0}
            _build_tree(path + [letter], depth + 1, max_depth,temp_counter,letter_pos,orange_pos_map)

    _build_tree(
        path=[],
        depth = 0,
        max_depth = MAX_DEPTH,
        counter=counter,
        letter_pos=letter_pos,
        orange_pos_map=ORANGE_POS_MAP
        )
    
    return set(result)

if __name__ == "__main__":
    orange_pos = [0,4]
    letter_pos = [
        ("N",0),
        ("O",1),
        ("M",2),
        ("E",3),
        ("R",4),
    ]
    counter = {
        "N":1,
        "O":1,
        "M":1,
        "E":1,
        "R":1
    }
    print(letter_pos_combinations_orange(orange_pos,letter_pos,counter))