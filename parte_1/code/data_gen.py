# This script takes in an input.in file and generates an output.out 
# file which the solver.py will use to read the parameter matrix

import random
import os
import numpy as np

def read_data(file_input=r'../in_files/default.in'):
    print(f"\nReading data from {file_input}...\n" + "*"*40 + "\n")
    with open(file_input, 'r') as f:
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
    pretty_print(arr, file_input=file_input)

def pretty_print(arr, file_input=r'../in_files/default.in'):
    pretty_string = "---".join(["+" for _ in range(len(arr[0]) + 1)]) + "\n"
    for row in arr:
        for i, char in enumerate(row):
            cell = " " if char is None else char
            if i == len(row) - 1:
                pretty_string += f"| {cell} |\n"
            else:
                pretty_string += f"| {cell} "
    pretty_string += "---".join(["+" for _ in range(len(row) + 1)]) + "\n"

    print(pretty_string)

    base_name = os.path.splitext(os.path.basename(file_input))[0]
    output_path = os.path.join('..', 'out_files', base_name, 'output.txt')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(pretty_string)
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    read_data()