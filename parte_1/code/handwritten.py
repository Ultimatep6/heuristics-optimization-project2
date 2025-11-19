from data_gen import read_data
from constraints_pack import no_three_horizontal,no_three_vertical, same_cell_const, num_var_const

init_config = read_data(r'../in_files/handwritten.in')
state = {}

rows = init_config.shape[0]
cols = init_config.shape[1]

cells = [(i, j) for i in range(rows) for j in range(cols)]
for i,j in cells:
    if init_config[i, j] == 'X':
        # print(f"Adding variable X_{i}_{j} fixed to 1")
        state[f'X_{i}_{j}'] = [1]
        state[f'O_{i}_{j}'] = [0]
    elif init_config[i, j] == 'O':
        # print(f"Adding variable O_{i}_{j} fixed to 1")
        state[f'O_{i}_{j}'] = [1]
        state[f'X_{i}_{j}'] = [0]

for i in range(rows):
    num_var_const_args = [state[f'X_{i}_{j}'][0] for j in range(cols)] + [state[f'O_{i}_{j}'][0] for j in range(cols)]
    cond1 = num_var_const(num_var_const_args, arg=True)
    if not cond1:
        print(f'num_var_const row_{i}: {cond1}')

    for j in range(cols):
        X_cell_var = f'X_{i}_{j}'
        O_cell_var = f'O_{i}_{j}'   
        cond2 = same_cell_const(state[X_cell_var][0], state[O_cell_var][0])
        if not cond2:
            print(f"same_cell_const {X_cell_var}, {O_cell_var}: {cond2}")

        if i+2 < rows:
            cond3 = no_three_vertical(state.get(f'X_{i-1}_{j}', [0])[0],
                                     state[X_cell_var][0],
                                     state[f'X_{i+1}_{j}'][0])
            if not cond3:
                print(f'no_three_vertical X at {i},{j}: {cond3}')

            cond4 = no_three_vertical(state.get(f'O_{i-1}_{j}', [0])[0],
                                     state[O_cell_var][0],
                                     state[f'O_{i+1}_{j}'][0])
            if not cond4:
                print(f'no_three_vertical O at {i},{j}: {cond4}')
        else:
            cond3 = True
            cond4 = True
        if j+2 < cols:
            cond5 = no_three_horizontal(state.get(f'X_{i}_{j-1}', [0])[0],
                                       state[X_cell_var][0],
                                       state[f'X_{i}_{j+1}'][0])
            if not cond5:
                print(f'no_three_horizontal X at {i},{j}: {cond5}')

            cond6 = no_three_horizontal(state.get(f'O_{i}_{j-1}', [0])[0],
                                       state[O_cell_var][0],
                                       state[f'O_{i}_{j+1}'][0])
            if not cond6:
                print(f'no_three_horizontal O at {i},{j}: {cond6}')
        else:
            cond5 = True
            cond6 = True

        if not all([cond2, cond3, cond4, cond5, cond6]):
            print(f"Cells {i},{j} constraints evaluated: {all([cond2, cond3, cond4, cond5, cond6])}")
            print("\n")

        
