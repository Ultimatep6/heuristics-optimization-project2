# Optimization and Heuristics Project 2
By:
- Matteo Oliver Bekink : 
- Aleksander Nowak, 576069

## Constraint Satisfaction Problem
All the problem configuration files can be found in `parte_1/in_files`. The layout of the file should follow the `template.in` files one-to-one for it to work.

Running the solver will produce a solution in the `parte_1/out_files` folder.

By default, the solver will solve on `default.in` and generate a `default.out` file. 

To run the solver with the **default** confuguration. 

```
python parte_1/parte-1.py 
```

To run the solver on your own configuration, run.
```
python parte_1/parte-1.py yourFile.in yourFile.out
```

Code blocks used in the project can be found in `parte_1/code`

### Search Algorithms Problem
All the problem files can be found in `parte_2/`, with the following files containing:
- `abierta.py`- implementation of open list (priority queue)
- `algoritmo.py` - implementation of used search algortihms
- `grafo.py` - read data from provided files

To run the code on the default configuration, simply run

`python parte_2/parte-2.py start_node_id end_node_id USA-road-d.BAY solution.txt`.

If you'd like to use this code on your own files, these files **must** be located within the folder `/parte_2/data`. 
Furthermore, the files must conform to the 9th DIMACS challenge format.
To run the code on your own files, use the following command:

`python parte_2/parte-2.py start_node_id end_node_id your_map_name your_output_file.txt`
