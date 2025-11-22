import time
import os
import sys
from code.data_gen import map_solution_dict, read_data, pretty_print
from code.constraints_pack import no_three_vertical, no_three_horizontal ,same_cell_const, num_var_const
import constraint

class Solver:
    def __init__(self, in_dir='../in_files/default.in'):
        self.in_dir = in_dir
        self.problem = constraint.Problem()
        self.constraint_count  = {
            'same_cell_const': 0,
            'no_three_horizontal': 0,
            'no_three_vertical': 0,
            'num_var_const_row': 0,
            'num_var_const_col': 0
        }

    def setup_variables(self):
        self.init_config = read_data(self.in_dir)

        self.rows = self.init_config.shape[0]
        self.cols = self.init_config.shape[1]
        
        # Create cells list
        self.cells = [(i, j) for i in range(self.rows) for j in range(self.cols)]

        # Iterate through cells and add variables based on value
        for i,j in self.cells:

            if self.init_config[i, j] == 'X':
                self.problem.addVariable(f'X_{i}_{j}', [1])
                self.problem.addVariable(f'O_{i}_{j}', [0])

            elif self.init_config[i, j] == 'O':
                self.problem.addVariable(f'O_{i}_{j}', [1])
                self.problem.addVariable(f'X_{i}_{j}', [0])

            else:    
                self.problem.addVariable(f'X_{i}_{j}', [1, 0])
                self.problem.addVariable(f'O_{i}_{j}', [1, 0])

    def setup_constraints(self):
        for i in range(self.rows):
            for j in range(self.cols):
                # Define the variable names
                X_cell_var = f'X_{i}_{j}'
                O_cell_var = f'O_{i}_{j}'

                # Constraint: A cell cannot be both X and O
                self.problem.addConstraint(same_cell_const, (X_cell_var, O_cell_var))
                # Increment constraint count
                self.constraint_count['same_cell_const'] += 1
                
                # Constraints for no three in a row/column
                if j + 2 < self.cols:
                    self.problem.addConstraint(no_three_horizontal,
                                               (f'X_{i}_{j}', f'X_{i}_{j+1}', f'X_{i}_{j+2}'))
                    
                    self.problem.addConstraint(no_three_horizontal,
                                               (f'O_{i}_{j}', f'O_{i}_{j+1}', f'O_{i}_{j+2}'))
                    
                    # Increment constraint count
                    self.constraint_count['no_three_horizontal'] += 2

                if i + 2 < self.rows:
                    self.problem.addConstraint(no_three_vertical,
                                               (f'X_{i}_{j}', f'X_{i+1}_{j}', f'X_{i+2}_{j}'))
                    self.problem.addConstraint(no_three_vertical,
                                               (f'O_{i}_{j}', f'O_{i+1}_{j}', f'O_{i+2}_{j}'))
                    
                    # Increment constraint count
                    self.constraint_count['no_three_vertical'] += 2

        # Constraints for equal number of X and O in rows and columns
        for i in range(self.rows):
            self.problem.addConstraint(
                num_var_const,
                [f'X_{i}_{j}' for j in range(self.cols)] + [f'O_{i}_{j}' for j in range(self.cols)]
            )
            self.constraint_count['num_var_const_row'] += 1
        for j in range(self.cols):
            self.problem.addConstraint(
                num_var_const,
                [f'X_{i}_{j}' for i in range(self.rows)] + [f'O_{i}_{j}' for i in range(self.rows)]
            )
            self.constraint_count['num_var_const_col'] += 1

    def solve(self):
        start = time.time()
        self.setup_variables()
        self.setup_constraints()
        solutions = self.problem.getSolutions()
        end = time.time()
        print(f"Time taken to solve: {end - start} seconds")
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
        output_file = os.path.join(script_dir, "out_files", "default.out")

    print(f"Input file: {os.path.relpath(input_file, script_dir)}")
    print(f"Output file: {os.path.relpath(output_file, script_dir)}")

    solver = Solver(in_dir=input_file)

    solutions, first_solution = solver.solve()
    if first_solution is not None:
        print(f"Total solutions found: {len(solutions)}")
        print(map_solution_dict(first_solution, solver.rows, solver.cols))
    else:
        print("No solution found.")
    pretty_print(solver.init_config, 
                 solutions=solutions,
                 file_input=input_file,
                 file_output=output_file,
                 n = 1)
    print("\nCONSTRAINTS")
    for constraint, count in solver.constraint_count.items():
        print(f"{constraint}: {count}")
        