"""
Merge function for 2048 game.
"""

def merge(line):
    """Function that merges a single row or column in 2048."""
    merged_line = []
    previous_number = 0
    merged_indexes = []

    for number in line:
        index_to_update = len(merged_line) - 1

        if previous_number > 0 and previous_number == number and index_to_update not in merged_indexes:
            merged_line[index_to_update] = previous_number * 2
            previous_number = previous_number * 2
            merged_indexes.append(index_to_update)
        elif number > 0:
            merged_line.append(number)
            previous_number = number

    if len(merged_line) < len(line):
        merged_line += [0] * (len(line) - len(merged_line))

    return merged_line

def test_merge():
    """Test code for merge"""

    print "Testing merge - Computed:", merge([2, 0, 2, 4]), "Expected:", str([4, 4, 0, 0])
    print "Testing merge - Computed:", merge([0, 0, 2, 2]), "Expected:", str([4, 0, 0, 0])
    print "Testing merge - Computed:", merge([2, 2, 0, 0]), "Expected:", str([4, 0, 0, 0])
    print "Testing merge - Computed:", merge([2, 2, 2, 2, 2]), "Expected:", str([4, 4, 2, 0, 0])
    print "Testing merge - Computed:", merge([8, 16, 16, 8]), "Expected:", str([8, 32, 8, 0])

# test_merge()
