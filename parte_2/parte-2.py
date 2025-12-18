from algoritmo import AStarSearch, haversine, sqrt_euclidian
from grafo import load_nodes, load_paths
from argparse import ArgumentParser
import time
import math
import random
from classes.Node import Node
from tqdm import tqdm
import copy


def parse_args():
    parser = ArgumentParser(description="A script to process nodes and files.")

    parser.add_argument("start_node", type=int, help="Starting node ID")
    parser.add_argument("end_node", type=int, help="End node ID")
    parser.add_argument(
        "map_name",
        nargs="?",
        type=str,
        default="USA-road-d.BAY",
        help="Base name of the map files",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        type=str,
        default="solution.txt",
        help="Name of the output file",
    )
    parser.add_argument("--brute_force", action="store_true")

    return parser.parse_args()


def print_output(node_dict, path_dict, cost, time, nr_expanded):
    exec_time = max(time * 10e-9, 10e-9)

    print("# Vertices: \t\t", len(node_dict))
    print("# Edges: \t\t", sum([len(path_dict[key]) for key in path_dict.keys()]))
    print(f"Optimal solution found with cost {cost}\n")
    print(f"Execution time: {exec_time} seconds")
    print(
        f"# Expansions: \t\t {nr_expanded} ({round(nr_expanded / exec_time, 3)} nodes/sec)\n"
    )


def create_output_file(fn_name, path):
    with open(fn_name, "w") as f:
        for i, nd in enumerate(path):
            if i == 0:
                f.write(str(nd.id))
                continue
            f.write(f" - ({nd.cost - path[i - 1].cost}) - ")
            f.write(str(nd.id))


def gen_random_start_end(
    num_pairs: int,
    node_dict: dict[int, Node],
    min_dist: float,
    max_dist: float = math.inf,
) -> list[tuple[int, int]]:
    pairs = []
    while len(pairs) < num_pairs:
        rand1, rand2 = random.choices(list(node_dict.values()), k=2)
        if rand1.id == rand2.id:
            continue
        if min_dist > haversine(rand1, rand2) or max_dist < haversine(rand1, rand2):
            continue
        pairs.append((rand1.id, rand2.id))
    return pairs


def run_experiment(rand_pairs, searcher: AStarSearch):
    times = []
    costs = []
    expanded_nodes = 0
    for pair in tqdm(rand_pairs):
        new_searcher = (
            AStarSearch(  # new searchers needed as node_dicts are edited in algorithm
                copy.deepcopy(searcher.node_dict),
                path_dict=searcher.path_dict,
                heuristic=searcher.heuristic,
            )
        )
        start_time = time.process_time_ns()
        _, cost = new_searcher.run(pair[0], pair[1])
        calc_time = time.process_time_ns() - start_time

        times.append(calc_time)
        costs.append(cost)
        expanded_nodes += new_searcher.get_num_expanded_nodes()

    return costs, times, expanded_nodes


if __name__ == "__main__":
    args = parse_args()
    node_dict = load_nodes(node_fn=args.map_name + ".co")
    path_dict = load_paths(path_fn=args.map_name + ".gr")

    if args.brute_force:
        searcher = AStarSearch(
            copy.copy(node_dict), path_dict, heuristic=lambda x, y: 1
        )  # epsilon heuristic
    else:
        searcher = AStarSearch(
            copy.copy(node_dict), path_dict=path_dict, heuristic=haversine
        )

    # rand_pairs = gen_random_start_end(5, node_dict, min_dist=200000)

    exec_time = time.perf_counter_ns()
    path, cost = searcher.run(args.start_node, args.end_node)
    exec_time = time.perf_counter_ns() - exec_time

    # print("----------------- Brute Force -----------------")
    # searcher = AStarSearch(node_dict, path_dict, heuristic=lambda x, y: 1)  # epsilon heuristic
    # costs, times, expanded_nodes = run_experiment(rand_pairs, searcher)
    # print_output(node_dict, path_dict, cost=sum(costs), time=sum(times), nr_expanded=expanded_nodes)

    # print("----------------- A* haversine -----------------")
    # searcher = AStarSearch(node_dict, path_dict, heuristic=haversine)  # epsilon heuristic
    # costs, times, expanded_nodes = run_experiment(rand_pairs, searcher)

    print_output(
        node_dict,
        path_dict,
        cost=cost,
        time=exec_time,
        nr_expanded=searcher.get_num_expanded_nodes(),
    )
    create_output_file(args.output_file, path)
