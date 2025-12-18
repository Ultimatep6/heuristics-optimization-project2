from algoritmo import AStarSearch
from grafo import load_nodes, load_paths
from argparse import ArgumentParser
import time


def parse_args():
    parser = ArgumentParser(
        description="A script to process nodes and files."
    )

    parser.add_argument("start_node", type=int, help="Starting node ID")
    parser.add_argument("end_node", type=int, help="End node ID")
    parser.add_argument("map_name", nargs="?", type=str, default="USA-road-d.BAY", help="Name of the input file")
    parser.add_argument("output_file", nargs="?", type=str, default="solution.txt", help="Name of the output file")

    return parser.parse_args()


def print_output(node_dict, path_dict, cost, time, nr_expanded):

    exec_time = round(time * 10e-9, 6)

    print("# Vertices: \t\t", len(node_dict))
    print("# Edges: \t\t", sum([len(path_dict[key]) for key in path_dict.keys()]))
    print(f"Optimal solution found with cost {round(cost/1000, 3)} km\n")
    print(f"Execution time: {exec_time} seconds")
    print(f"# Expansions: \t\t {nr_expanded} ({round(nr_expanded / exec_time, 3)} nodes/sec)")


if __name__ == "__main__":
    args = parse_args()
    node_dict = load_nodes(node_fn=args.map_name + ".co")
    path_dict = load_paths(path_fn=args.map_name + ".gr")
    searcher = AStarSearch(node_dict=node_dict, path_dict=path_dict)
    brute_force_searcher = AStarSearch(node_dict, path_dict, heuristic=lambda x, y: 1)  # epsilon heuristic

    start_time = time.process_time_ns()
    path, cost = searcher.run(args.start_node, args.end_node)
    calc_time = time.process_time_ns() - start_time

    print_output(node_dict, path_dict, cost, calc_time, searcher.get_num_expanded_nodes())
    # for i, nd in enumerate(path):
    #     print(f"Step {i}: id -", nd.id, "cost -", round(nd.cost / 1000, 3))
    # print("--------------")
    # print("A* Cost:", cost / 1000, "km")

    # brute_force_searcher = AStarSearch(node_dict, path_dict, heuristic=lambda x, y: 1)  # epsilon heuristic
    # path, cost = searcher.run(1, 10)
    # # for i, nd in enumerate(path):
    # #     print(f"Step {i}: id -", nd.id, "cost -", round(nd.cost / 1000, 3))
    # # print("--------------")
    # print("Brute Force (Dijkstra) Cost:", cost / 1000, "km")
