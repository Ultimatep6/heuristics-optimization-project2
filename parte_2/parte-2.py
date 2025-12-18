from algoritmo import AStarSearch
from grafo import load_nodes, load_paths

if __name__ == "__main__":
    node_dict = load_nodes()
    path_dict = load_paths()
    searcher = AStarSearch(node_dict=node_dict, path_dict=path_dict)
    path, cost = searcher.run(1, 10)
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
