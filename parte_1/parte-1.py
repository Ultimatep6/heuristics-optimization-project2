# import constraint
# problem = constraint.Problem()
# x = [(0,0), (0,1), (1,0), (-1,0), (0,-1)]

# for i in range(len(x)):
#     problem.addVariable(f'X_{x[i]}', [1, 0])

# def constraint_func(c,u,d,l,r):
#     return not((c and u and d) or (c and l and r))

# problem.addConstraint(constraint_func, (f'X_{x[0]}', f'X_{x[1]}', f'X_{x[2]}', f'X_{x[3]}', f'X_{x[4]}'))
# solutions = problem.getSolutions()
# for s in solutions:
#     print(s)
# print(f"Total solutions: {len(solutions)}")


import os
import sys
import numpy as np
from code.data_gen import map_solution_dict, read_data, pretty_print
import constraint
import argparse

class Solver:
    def __init__(self, in_dir='../in_files/default.in', var_matrix=None):
        self.in_dir = in_dir
        self.problem = constraint.Problem()

    def setup_variables(self):
        self.init_config = read_data(self.in_dir)

        self.rows = self.init_config.shape[0]
        self.cols = self.init_config.shape[1]
        
        self.cells = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        for i,j in self.cells:
            if self.init_config[i, j] == 'X':
                # print(f"Adding variable X_{i}_{j} fixed to 1")
                self.problem.addVariable(f'X_{i}_{j}', [1])
                self.problem.addVariable(f'O_{i}_{j}', [0])
            elif self.init_config[i, j] == 'O':
                # print(f"Adding variable O_{i}_{j} fixed to 1")
                self.problem.addVariable(f'O_{i}_{j}', [1])
                self.problem.addVariable(f'X_{i}_{j}', [0])
            else:    
                self.problem.addVariable(f'X_{i}_{j}', [1, 0])
                self.problem.addVariable(f'O_{i}_{j}', [1, 0])

    def setup_constraints(self):
        from code.constraints_pack import no_three_vertical, no_three_horizontal ,same_cell_const, num_var_const

        for i in range(self.rows):
            for j in range(self.cols):
                X_cell_var = f'X_{i}_{j}'
                O_cell_var = f'O_{i}_{j}'   
                self.problem.addConstraint(same_cell_const, (X_cell_var, O_cell_var))
                
                if j + 2 < self.cols:
                    self.problem.addConstraint(no_three_horizontal,
                                               (f'X_{i}_{j}', f'X_{i}_{j+1}', f'X_{i}_{j+2}'))
                    self.problem.addConstraint(no_three_horizontal,
                                               (f'O_{i}_{j}', f'O_{i}_{j+1}', f'O_{i}_{j+2}'))
                if i + 2 < self.rows:
                    self.problem.addConstraint(no_three_vertical,
                                               (f'X_{i}_{j}', f'X_{i+1}_{j}', f'X_{i+2}_{j}'))
                    self.problem.addConstraint(no_three_vertical,
                                               (f'O_{i}_{j}', f'O_{i+1}_{j}', f'O_{i+2}_{j}'))

        # Constraints for equal number of X and O in rows and columns
        for i in range(self.rows):
            self.problem.addConstraint(
                num_var_const,
                [f'X_{i}_{j}' for j in range(self.cols)] + [f'O_{i}_{j}' for j in range(self.cols)]
            )
        for j in range(self.cols):
            self.problem.addConstraint(
                num_var_const,
                [f'X_{i}_{j}' for i in range(self.rows)] + [f'O_{i}_{j}' for i in range(self.rows)]
            )

    def solve(self):
        self.setup_variables()
        self.setup_constraints()
        solutions = self.problem.getSolutions()
        return solutions, solutions[0] if solutions else None
    
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Check if arguments are given
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        if "in_files" not in input_file:
            input_file = os.path.join(script_dir, "in_files", input_file)
        if "out_files" not in output_file:
            output_file = os.path.join(script_dir, "out_files", output_file)
        
    # If not provided, find them in pre-assumed location
    else:
        input_file = os.path.join(script_dir, "in_files", "default.in")
        output_file = os.path.join(script_dir, "out_files","default", "output.txt")

    print(f"Input file: {os.path.relpath(input_file, script_dir)}")
    print(f"Output file: {os.path.relpath(output_file, script_dir)}")

    solver = Solver(in_dir=input_file)

    solutions, first_solution = solver.solve()
    print(f"Total solutions found: {len(solutions)}")
    print(map_solution_dict(first_solution, solver.rows, solver.cols))
    pretty_print(solver.init_config, 
                 solutions=solutions,
                 file_input=input_file,
                 file_output=output_file,
                 n = 1)