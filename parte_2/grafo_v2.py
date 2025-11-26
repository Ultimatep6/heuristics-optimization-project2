from classes.Node import Node
from classes.Path import Path

import os
script_dir = os.path.dirname(__file__)

def load_nodes():
    nodeDict = {}
    node_dir = os.path.join(script_dir, '../data/USA-road-d.BAY.co')

    with os.open(node_dir, 'r') as node_file:
        # find the first line with 'v' to get the index of the first node
        for line in node_file:
            if line.startswith('v'):
                first_node_index = int(line.split()[1])
                break
        for node in node_file[first_node_index:]:
            parts = node.split()
            node_id = int(parts[1])
            long = int(parts[2])
            lat = int(parts[3])
            nodeDict[node_id] = Node(lat,long)

    return nodeDict

def load_paths():
    pathDict = {}
    path_dir = os.path.join(script_dir, '../data/USA-road-d.BAY.gr')

    with os.open(path_dir, 'r') as path_file:
        for line in path_file:
            if line.startswith('a'):
                first_node_index = int(line.split()[1])
                break
        for path in path_file[first_node_index:]:
            parts = path.split()
            from_node = int(parts[1])
            to_node = int(parts[2])
            cost = int(parts[3])

            if from_node in pathDict:
                pathDict[from_node].append(Path(from_node, to_node, cost))
            else:
                pathDict[from_node] = [Path(from_node, to_node, cost)]
    return pathDict


if __name__ == "__main__":
    print("Loading nodes...")
    nodes = load_nodes()
    print(f"Loaded {len(nodes)} nodes.\n")


    print("Loading paths...")
    paths = load_paths()
    print(f"Loaded {len(paths)} paths.")