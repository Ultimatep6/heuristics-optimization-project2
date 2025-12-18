from algoritmo import AStarSearch
from grafo import load_nodes, load_paths
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(
        description="A script to process nodes and files."
    )

    parser.add_argument("start_node", type=int, help="Starting node ID")
    parser.add_argument("end_node", type=int, help="End node ID")
    parser.add_argument("map_name", nargs="?", type=str, default="USA-road-d.BAY", help="Name of the input file")
    parser.add_argument("output_file", nargs="?", type=str, default="solution.txt", help="Name of the output file")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    node_dict = load_nodes(node_fn=args.map_name + ".co")
    path_dict = load_paths(path_fn=args.map_name + ".gr")
    searcher = AStarSearch(node_dict=node_dict, path_dict=path_dict)
    path, cost = searcher.run(args.start_node, args.end_node)
    # for i, nd in enumerate(path):
    #     print(f"Step {i}: id -", nd.id, "cost -", round(nd.cost / 1000, 3))
    # print("--------------")
    print("A* Cost:", cost / 1000, "km")

    brute_force_searcher = AStarSearch(node_dict, path_dict, heuristic=lambda x, y: 1)  # epsilon heuristic
    path, cost = searcher.run(1, 10)
    # for i, nd in enumerate(path):
    #     print(f"Step {i}: id -", nd.id, "cost -", round(nd.cost / 1000, 3))
    # print("--------------")
    print("Brute Force (Dijkstra) Cost:", cost / 1000, "km")
