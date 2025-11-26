from algoritmo import AStarSearch
from grafo import load_nodes, load_paths

if __name__ == "__main__":
    node_dict = load_nodes()
    path_dict = load_paths()
    searcher = AStarSearch(node_dict=node_dict, path_dict=path_dict)
    path, cost = searcher.run(1, 2137)
    for nd in path:
        print(nd.id)
    print("--------------")
    print(cost)
