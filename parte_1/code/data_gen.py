# This script takes in an input.in file and generates an output.out 
# file which the solver.py will use to read the parameter matrix

import random
import os
import numpy as np

def read_data(file_input=r'../in_files/default.in'):
    # Resolve path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, file_input)

    print(f"\nReading data from {os.path.relpath(input_path, script_dir)}\n" + "*"*40 + "\n")
    with open(input_path, 'r') as f:
        lines = f.readlines()

    arr = []
    for line in lines:
        temp = []
        for char in line.strip():
            if char == 'X':
                temp.append('X')
            elif char == 'O':
                temp.append('O')
            else:
                temp.append(None)
        arr.append(temp)

    print("Data read successfully.")
    # pretty_print(arr, file_input=file_input)
    
    
    return np.array(arr)

def pretty_print(begin_arr=None,solutions=None, file_input=r'../in_files/default.in',file_output=r'../out_files/default/output.txt',n=0):
    """Pretty prints the matrix and saves it to an output file."""
    """Use append to add to existing file instead of overwriting."""
    
    pretty_string = ""
    pretty_string = convert_to_print(begin_arr)
    
    if solutions is not None:
        if n != 0:
            solutions = solutions[:n]
            for sol in solutions:
                pretty_string += '\n'
                pretty_string += convert_to_print(map_solution_dict(sol, begin_arr.shape[0], begin_arr.shape[1]))

            
        
    with open(file_output, 'w') as f:
        f.write(pretty_string)

    print(f"Output saved to {file_output}")

def convert_to_print(arr):
    pretty_string = "---".join(["+" for _ in range(len(arr[0]) + 1)]) + "\n"
    for row in arr:
        for i, char in enumerate(row):
            cell = " " if char is None else char
            if i == len(row) - 1:
                pretty_string += f"| {cell} |\n"
            else:
                pretty_string += f"| {cell} "
    pretty_string += "---".join(["+" for _ in range(len(row) + 1)]) + "\n"
    return pretty_string

def map_solution_dict(solution:np.array, rows:int, cols:int):
    """Maps the solution dictionary to a 2D numpy array."""
    sol_array = np.full((rows, cols), None)
    for key, value in solution.items():
        var_type, i, j = key.split('_')
        i, j = int(i), int(j)
        if value == 1:
            sol_array[i, j] = var_type
    return sol_array
