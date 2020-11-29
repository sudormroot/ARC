#!/usr/bin/python

""" NUI Galway CT5132/CT5148 Programming and Tools for AI

Assignment 3: ARC

This code is written and finished in vim.

Student name: Jiaolin Luo
Student ID: 20230436

Project URL: https://github.com/sudormroot/ARC

"""


import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.


"""
    Task ID:
        f8a8fe49

    Required transformation:
        a. Identify the direction pattern for color 2 (red) square brackets:

           Vertical pattern (i):
           rrrrrrrrrrrrrrr
           r             r


           r             r
           rrrrrrrrrrrrrrr

           Horizontal pattern (ii):

           rr        rr    
           r          r
           r          r
           rr        rr

        b. Flip the included shapes outside of the square brackets according:

           (i). Vertical pattern:
                (1) Flip the upper shape to the upper outside of the red square brackets.
                (2) Flip the bottom shape to the bottom outside of the red square brakcets.
            (ii). Horizontal pattern:
                (1) Fip the left shape to the left outside of the red square brackets.
                (2) Flip the right shape to the righ outside of the red square brackets.

    Algorithm:
        1. Identify the direction by matching:
           
           Vertical pattern:
           
           rrr
           r

           Horizontal pattern:

           rr
           r
           r
        
        2. Flip shapes according the directions.

"""


# Find the direction of given color
def find_direction(x, c):

    # We scan all points
    for i in range(x.shape[0] - 3):
        for j in range(x.shape[1] - 3):
            
            # pattern matched.
            if x[i, j] == c and x[i + 1, j] == c and x[i, j + 1] == c:

                # vertical pattern
                if x[i, j + 2] == c:
                    return i, i + 7, "v"

                # horizontal pattern
                if x[i + 2, j] == c:
                    return j, j + 7, "h"

    return None, None


# flip the shape with color 'c' vertically
def flip_vertically(x, x1, x2, c):

    # flip the first shape.
    x[x1 - 2, :] = x[x1 + 2, :]
    x[x1 + 2, :] = np.zeros(x.shape[1], dtype = np.int)

    x[x1 - 3, :] = x[x1 + 3, :]
    x[x1 + 3, :] = np.zeros(x.shape[1], dtype = np.int)


    # flip the second shape.
    x[x2 + 2, :] = x[x2 - 2, :]
    x[x2 - 2, :] = np.zeros(x.shape[1], dtype = np.int)


# flip the shape with color 'c' horizontally
def flip_horizontally(x, y1, y2, c):

    # flip the first shape.
    x[:, y1 - 2] = x[:, y1 + 2]
    x[:, y1 + 2] = np.zeros(x.shape[0], dtype = np.int)

    x[:, y1 - 3] = x[:, y1 + 3]
    x[:, y1 + 3] = np.zeros(x.shape[0], dtype = np.int)


    # flip the second shape.
    x[:, y2 + 2] = x[:, y2 - 2]
    x[:, y2 - 2] = np.zeros(x.shape[1], dtype = np.int)



def solve_f8a8fe49(x):

    # define colors
    GRAY = 2
    RED = 5

    c1, c2, direction = find_direction(x, GRAY)

    if direction == "v":
        flip_vertically(x, c1, c2, RED)

    if direction == "h":
        flip_horizontally(x, c1, c2, RED)

    return x

"""
    Task ID: 
        1e0a9b12

    Required transformation:
        This task requires of moving all colored blocks to the bottom of the column.

    Algorithm:
        1. Iterate all columns.
        2. For each columns, we count the number (as N) of non-zero element (as x_i) for this column (as i).
        3. We find out the non-zero element (as c).
        4. We generate a new column starting with (K - N) zeros -- K is the height of column, and, following with N zeros.

"""

def solve_1e0a9b12(x):

    # iterate all columns in x
    for col in range(x.shape[1]):

        # find out the total number of non-zero elements for given column.
        n = np.count_nonzero(x[:, col])

        # find out the non-zero element for given column
        c = x[:, col].nonzero()
        c = x[:, col][c]

        # for special cases if all elements are zero.
        if len(c) > 0:
            c = c[0]
        else:
            c = 0

        # generate new column, zeros follow by non-zero elements.
        x[:, col] = [0] * (x.shape[0] - n) + [c] * n

    return x


"""
    Task ID:
        0ca9ddb6
    
    Required transformation:
        a. For color 2 (red), paint four diagnoal corners with color 4 (yellow), the pattern is:
           Y   Y
             R
           Y   Y

        b. For color 1 (blue), draw a cross with color 7 (orange), the pattern is:
             O
           O B O
             O
        c. For other colors, we ignore them.

    Algorithm:
        1. Iterate all non-zero points.
        2. If the non-zero point is the color we need to draw the patterns, we draw the patterns as in (a) and (b).
        3. If the non-zero point is not in the candidate color, we just ignore it.

"""


# Set given color at location (m, n)
def set_color(x, m, n, c):
    if m >= 0 and m < x.shape[0] and n >= 0 and n < x.shape[1]:
        x[m, n] = c

# We paint four corners with color 'c', the 
# center coordinate is at (i, j).
def paint_corners(x, i, j, c):
    # Left-upper corner
    m = i - 1
    n = j - 1
    set_color(x, m, n, c)

    # Right-upper corner
    m = i - 1
    n = j + 1
    set_color(x, m, n, c)

    # Left-bottom corner
    m = i + 1
    n = j - 1
    set_color(x, m, n, c)

    # Right-bottom corner
    m = i + 1
    n = j + 1
    set_color(x, m, n, c)


# We draw a cross with color 'c', the 
# center coordinate is at (i, j).
def draw_cross(x, i, j, c):

    # North.
    m = i - 1
    n = j
    set_color(x, m, n, c)

    # East.
    m = i 
    n = j + 1
    set_color(x, m, n, c)

    # South
    m = i + 1
    n = j 
    set_color(x, m, n, c)

    # West
    m = i 
    n = j - 1
    set_color(x, m, n, c)


def solve_0ca9ddb6(x):

    # define colors

    BLACK = 0
    RED = 2
    BLUE = 1
    YELLOW = 4
    ORANGE = 7

    # We iterate all elements
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            
            # the center
            c = x[i, j]
            
            # ignore black point
            if c == BLACK:
                continue

            # for red, we paint four corners.
            if c == RED:
                paint_corners(x, i, j, YELLOW)

            # for blue, we draw a cross.
            if c == BLUE:
                draw_cross(x, i, j, ORANGE)

    return x







def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": 
    main()

