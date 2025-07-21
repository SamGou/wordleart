def deconstruct_line(line):
    block_loc_map = {"G":[],"O":[],"#":[]}
    for idx,block in enumerate(line):
        block_loc_map[block].append(idx)
    return block_loc_map

if __name__ == "__main__":
    line = "G#O#O"
    print(deconstruct_line(line))
