# Global Declarations
assignments = []
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def sudoku_init():
    global rows
    rows = 'ABCDEFGHI'
    global cols 
    cols = '123456789'
    global boxes
    boxes = cross(rows, cols)
    global row_units
    row_units = [cross(r, cols) for r in rows]
    ##print(row_units)
    global column_units
    column_units = [cross(rows, c) for c in cols]
    ##print(column_units)
    global square_units
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    ##print(type(square_units), square_units)
    global maj_dia
    maj_dia = [major_dia(rows, cols)]
    global min_dia
    min_dia = [minor_dia(rows, cols)]
    global dia_units
    dia_units = maj_dia + min_dia
    ##print(type(dia_units), dia_units)
    global unitlist
    unitlist = row_units + column_units + square_units  + dia_units
    ##print(type(unitlist))
    global units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    #print(units)
    global peers
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    #print(peers)
    return

def check_if_peer(box1, box2):
    global peers
    if box1 in peers[box2] and box2 in peers[box1]:
        return True
    else:
       return False

def find_naked_twins(probable_twins):
    newtwins = dict()
    for a,v in probable_twins.items():
        for b,u in probable_twins.items():
            if a != b and v == u and check_if_peer(a, b) and b not in newtwins:
                newtwins.update({a:b})
    return newtwins

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    """
    Find all instances of naked twins
    Eliminate the naked twins as possibilities for their peers
    """
    # initialize sudoku processing...
    import collections
    sudoku_init()
    global row_units
    global column_units
    global square_units
    #global peers
    global boxes
    global unitlist
    global dia_units
    ulist = [x for x in unitlist if x not in dia_units]
    units = dict((s, [u for u in ulist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    row_units = dict((s, [u for u in row_units if s in u]) for s in boxes)
    col_units = dict((s, [u for u in column_units if s in u]) for s in boxes)
    sqr_units = dict((s, [u for u in square_units if s in u]) for s in boxes)
    row_peers = dict((s, set(sum(row_units[s],[]))-set([s])) for s in boxes)
    col_peers = dict((s, set(sum(col_units[s],[]))-set([s])) for s in boxes)
    sqr_peers = dict((s, set(sum(sqr_units[s],[]))-set([s])) for s in boxes)

    stalled = False
    key_pairs_d = dict((box,values[box]) for box in values.keys() if len(values[box]) == 2)
    display(values, boxes, rows, cols)
    #print(key_pairs_d)

    twins = find_naked_twins(key_pairs_d)
    #print(twins)
    new_sudoku = values.copy()
    for k, v in twins.items():
        if v in row_peers[k] and k in row_peers[v] and new_sudoku[k] == new_sudoku[v]:
            #print(v, " in row_peers of ", k, "and viceversa")
            for peer in row_peers[k]:
                if len(new_sudoku[peer]) > 1:
                    #print("row peers of : ",k, " is ", peer, new_sudoku[peer])
                    if new_sudoku[peer] != new_sudoku[k]:
                        for substring in new_sudoku[k]:
                            if substring in new_sudoku[peer]:
                                new_sudoku = assign_value(new_sudoku, peer, new_sudoku[peer].replace(substring,""))
                                #print("new_sudoku updated: ", new_sudoku[peer])
                    else:
                        pass
                        #print("new_sudoku[",peer,"] = ", new_sudoku[peer])
                        #print("new_sudoku[", k,"] = ", new_sudoku[k])

        elif v in col_peers[k] and k in col_peers[v]:
            #print(v, " in col_peers of ", k, "and viceversa")
            for peer in col_peers[k]:
                if len(new_sudoku[peer]) > 1:
                    #print("col peers of : ",k, " is ", peer, new_sudoku[peer])
                    if new_sudoku[peer] != new_sudoku[k]:
                        for substring in new_sudoku[k]:
                            if substring in new_sudoku[peer]:
                                new_sudoku = assign_value(new_sudoku, peer, new_sudoku[peer].replace(substring,""))
                                #print("new_sudoku updated: ", new_sudoku[peer])
                    else:
                        pass
                        #print("new_sudoku[",peer,"] = ", new_sudoku[peer])
                        #print("new_sudoku[", k,"] = ", new_sudoku[k])
        else:
            pass

        if v in sqr_peers[k] and k in sqr_peers[v]:
            #print(v, " in sqr_peers of ", k, "and viceversa")
            for peer in sqr_peers[k]:
                if len(new_sudoku[peer]) > 1:
                    #print("sqr peers of : ",k, " is ", peer, new_sudoku[peer])
                    if new_sudoku[peer] != new_sudoku[k]:
                        for substring in new_sudoku[k]:
                            if substring in new_sudoku[peer]:
                                #print("new_sudoku before updated: ", new_sudoku[peer])
                                new_sudoku = assign_value(new_sudoku, peer, new_sudoku[peer].replace(substring,""))
                                #print("new_sudoku after updated: ", new_sudoku[peer])
                    else:
                        pass
                        #print("new_sudoku[",peer,"] = ", new_sudoku[peer])
                        #print("new_sudoku[", k,"] = ", new_sudoku[k])

    display(new_sudoku, boxes, rows, cols)
    #print("############################################################################################")
    return new_sudoku

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def major_dia(A, B):
    "Concatenate elements in A and elements in B."
    return [s+t for s,t in zip(A,B)]

def minor_dia(A, B):
    "Reverse elements in A and concatenate elements in A and elements in B."
    return [s+t for s,t in zip(A[::-1],B)]

def grid_values(grid, boxes):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # Check if grid input is valid
    assert len(grid) == 81
    
    values = []
    possible_vals = "123456789"
    
    for v in grid:
        if v == '.' :
            values.append(possible_vals)
        elif v in possible_vals:
            values.append(v)

    return dict(zip(boxes,values))

def display(values, boxes, rows, cols):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values, peers, maj_dia, min_dia, boxes, rows, cols):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers. For diagonal
    elements, check for diagonal peers and eliminate.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    solved_boxes = [key for key in values.keys() if len(values[key]) == 1]
    for box in solved_boxes:
        val = values[box]
        ##print("Box:", box, "Peers:", peers[box])
        for peer in peers[box]:
            #if peer == 'A5':
                ##print("_____________________________________________________")
                ##print("_____________________________________________________")
            values = assign_value(values, peer, values[peer].replace(val,""))
            #Major Diagonal Peer elimination
        
        if box in maj_dia[0]:
                ###print(key,":", values[key], "key:value in Major Diagonal")
            for peer in maj_dia[0]:
                if peer != box:
                    values = assign_value(values, peer, values[peer].replace(val,""))

        elif box in min_dia[0]:
            #Minor Diagonal Peer elimination
            for peer in min_dia[0]:
                if peer != box:
                    values = assign_value(values, peer, values[peer].replace(val,""))
        else:
            pass

    return values

def only_choice(values, unitlist):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # only choice strategy 
    for unit in unitlist:
        for digit in '123456789':
            loc = [box for box in unit if digit in values[box]]
            ###print(loc,values[loc[0]], digit)
            if len(loc) == 1:
                values[loc[0]] = digit
                ###print(loc,values[loc[0]])

    return values

def reduce_puzzle(values, peers, maj_dia, min_dia, unitlist, rows, cols, boxes):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        ##print(solved_values_before)
        # Eliminate Stratergy    
        #display(values, boxes, rows, cols)
        #print("====================== Eliminate ===================================")
        values = eliminate(values, peers, maj_dia, min_dia, boxes, rows, cols)
        #display(values, boxes, rows, cols)
        #input("Press Enter...")
        # Only Choice Stratergy
        #print("====================== Only Choice =================================")
        values = only_choice(values, unitlist)
        #display(values, boxes, rows, cols)
        #input("Press Enter...")
        # Naked Twins Stratergy
        #print("====================== Naked Twins =================================")
        values = naked_twins(values)
        #display(values, boxes, rows, cols)
        #print("====================================================================")
        #input("Press Enter...")
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        #print("Stalled Flag is ", stalled)
        #input("Press Enter...")
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values, boxes, peers, maj_dia, min_dia, unitlist, rows, cols):
    "Using depth-first search and propagation, create a search tree and to solve the sudoku."
    " First, reduce the puzzle"
    values = reduce_puzzle(values, peers, maj_dia, min_dia, unitlist, rows, cols, boxes)
    
    if values is False:
        return False # Failed in reduce_puzzle function.
    
    if all(len(values[s]) == 1 for s in boxes): 
        return values
 
    " Choose one of the unfilled squares with the fewest possibilities"
    " Create a subset dictory of boxes with length value."
    unsolved_dict = dict((box,len(values[box])) for box in values.keys() if len(values[box]) != 1)
    ###print (unsolved_dict)
    " Find minimum length box to solve"
    box_to_solve =  min(unsolved_dict, key=unsolved_dict.get)
    ###print(box_to_solve, values[box_to_solve])
    " Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!"
    digits = values[box_to_solve]
    for digit in digits:
        ###print(type(values[box_to_solve]), type(digit))
        ###print(values[box_to_solve], digit)
        new_sudoku = values.copy()
        new_sudoku[box_to_solve] = digit
        #print("Solving Box ", box_to_solve, " contains ", digit) 
        ##print(new_sudoku[box_to_solve], digit)
        new_sudoku = search(new_sudoku, boxes, peers, maj_dia, min_dia, unitlist, rows, cols)
        if new_sudoku:
            return new_sudoku

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    sudoku_init()
    global row_units
    #print(row_units)
    global column_units
    #print(column_units)
    global dia_units
    #print(dia_units)
    global unitlist
    #print(unitlist)
    global units
    #print(units)
    values = grid_values(grid, boxes)
    display(values, boxes, rows, cols)
    values = search(values, boxes, peers, maj_dia, min_dia, unitlist, rows, cols)
    #values = search(values, boxes, peers, maj_dia, min_dia, unitlist, rows, cols)
    display(values, boxes, rows, cols)
    ##print(type(square_units), square_units)
    return values 

if __name__ == '__main__':
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    #solve(diag_sudoku_grid)
    print("========================================================================================================")
    naked_twins({"G7": "1234568", "G6": "9", "G5": "35678", "G4": "23678", "G3":
    "245678", "G2": "123568", "G1": "1234678", "G9": "12345678", "G8":
    "1234567", "C9": "13456", "C8": "13456", "C3": "4678", "C2": "68",
    "C1": "4678", "C7": "13456", "C6": "368", "C5": "2", "A4": "5", "A9":
    "2346", "A8": "2346", "F1": "123689", "F2": "7", "F3": "25689", "F4":
    "23468", "F5": "1345689", "F6": "23568", "F7": "1234568", "F8":
    "1234569", "F9": "1234568", "B4": "46", "B5": "46", "B6": "1", "B7":
    "7", "E9": "12345678", "B1": "5", "B2": "2", "B3": "3", "C4": "9",
    "B8": "8", "B9": "9", "I9": "1235678", "I8": "123567", "I1": "123678",
    "I3": "25678", "I2": "123568", "I5": "35678", "I4": "23678", "I7":
    "9", "I6": "4", "A1": "2468", "A3": "1", "A2": "9", "A5": "3468",
    "E8": "12345679", "A7": "2346", "A6": "7", "E5": "13456789", "E4":
    "234678", "E7": "1234568", "E6": "23568", "E1": "123689", "E3":
    "25689", "E2": "123568", "H8": "234567", "H9": "2345678", "H2":
    "23568", "H3": "2456789", "H1": "2346789", "H6": "23568", "H7":
    "234568", "H4": "1", "H5": "35678", "D8": "1235679", "D9": "1235678",
    "D6": "23568", "D7": "123568", "D4": "23678", "D5": "1356789", "D2":
    "4", "D3": "25689", "D1": "123689"})
    print("========================================================================================================")
    naked_twins({"G7": "2345678", "G6": "1236789", "G5": "23456789", "G4": "345678",
    "G3": "1234569", "G2": "12345678", "G1": "23456789", "G9": "24578",
    "G8": "345678", "C9": "124578", "C8": "3456789", "C3": "1234569",
    "C2": "1234568", "C1": "2345689", "C7": "2345678", "C6": "236789",
    "C5": "23456789", "C4": "345678", "E5": "678", "E4": "2", "F1": "1",
    "F2": "24", "F3": "24", "F4": "9", "F5": "37", "F6": "37", "F7": "58",
    "F8": "58", "F9": "6", "B4": "345678", "B5": "23456789", "B6":
    "236789", "B7": "2345678", "B1": "2345689", "B2": "1234568", "B3":
    "1234569", "B8": "3456789", "B9": "124578", "I9": "9", "I8": "345678",
    "I1": "2345678", "I3": "23456", "I2": "2345678", "I5": "2345678",
    "I4": "345678", "I7": "1", "I6": "23678", "A1": "2345689", "A3": "7",
    "A2": "234568", "E9": "3", "A4": "34568", "A7": "234568", "A6":
    "23689", "A9": "2458", "A8": "345689", "E7": "9", "E6": "4", "E1":
    "567", "E3": "56", "E2": "567", "E8": "1", "A5": "1", "H8": "345678",
    "H9": "24578", "H2": "12345678", "H3": "1234569", "H1": "23456789",
    "H6": "1236789", "H7": "2345678", "H4": "345678", "H5": "23456789",
    "D8": "2", "D9": "47", "D6": "5", "D7": "47", "D4": "1", "D5": "36",
    "D2": "9", "D3": "8", "D1": "36"})
    print("========================================================================================================")

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
