from classes.Node import Node
from classes.Path import Path

import os
script_dir = os.path.dirname(__file__)

def load_nodes():
    nodeDict = {}
    node_dir = os.path.join(script_dir, r'./data/USA-road-d.BAY.co')

    with open(node_dir, 'r') as node_file:        
        # only read lines starting from first_node_index
        for i, node in enumerate(node_file):
            if not node.startswith('v'):
                continue
            parts = node.split()
            node_id = int(parts[1])
            long = int(parts[2])
            lat = int(parts[3])
            nodeDict[node_id] = Node(lat,long)

    return nodeDict

def load_paths():
    pathDict = {}
    path_dir = os.path.join(script_dir, r'./data/USA-road-d.BAY.gr')

    with open(path_dir, 'r') as path_file:
        for i, path in enumerate(path_file):
            if not path.startswith('a'):
                continue
            parts = path.split()
            from_node = int(parts[1])
            to_node = int(parts[2])
            cost = int(parts[3])

            if from_node in pathDict:
                pathDict[from_node].append(Path(from_node, to_node, cost))
            else:
                pathDict[from_node] = [Path(from_node, to_node, cost)]

    return pathDict


# if __name__ == "__main__":
#     print("Loading nodes...")
#     nodes = load_nodes()
#     print(f"Loaded {len(nodes.keys())} nodes.\n")

#     print("Loading paths...")
#     paths = load_paths()
#     print(f"Loaded {len(paths.keys())} paths.")
