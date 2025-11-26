from classes.Node import Node
from classes.Path import Path
import pathlib

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent


def load_nodes():
    nodeDict = {}
    node_dir = SCRIPT_DIR / "./data/USA-road-d.BAY.co"

    with open(node_dir, "r") as node_file:
        for line in node_file:
            if line.startswith("v"):
                parts = line.split()
                node_id = int(parts[1])
                long = int(parts[2])
                lat = int(parts[3])
                nodeDict[node_id] = Node(node_id, lat, long)

    return nodeDict


def load_paths():
    pathDict: dict[int, list[Path]] = {}
    path_dir = SCRIPT_DIR / "./data/USA-road-d.BAY.gr"

    with open(path_dir, "r") as path_file:
        for line in path_file:
            if line.startswith("a"):
                line = line.split()
                from_node = int(line[1])
                to_node = int(line[2])
                cost = int(line[3])

                if from_node in pathDict:
                    pathDict[from_node].append(Path(from_node, to_node, cost))
                else:
                    pathDict[from_node] = [Path(from_node, to_node, cost)]
    return pathDict


if __name__ == "__main__":
    print("Loading nodes...")
    nodes = load_nodes()
    print(f"Loaded {len(nodes.keys())} nodes.\n")

    print("Loading paths...")
    paths = load_paths()
    print(f"Loaded {len(paths)} paths.")
