import itertools

def deconstruct_line(line):
    block_loc_map = {"G":[],"O":[],"#":[]}
    for idx,block in enumerate(line):
        block_loc_map[block].append(idx)
    return block_loc_map

def generate_all_combinations_line():
    # Allowed characters
    chars = ["G", "O", "#"]

    # Length of each string
    length = 5

    # Generate all combinations
    combinations = [''.join(p) for p in itertools.product(chars, repeat=length)]

    return combinations

if __name__ == "__main__":
    line = "G#O#O"
    print(deconstruct_line(line))
    print(generate_all_combinations_line())