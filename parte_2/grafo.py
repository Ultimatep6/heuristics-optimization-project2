import networkx as nx
from tqdm import tqdm


def parse_gr(f):
    DG = nx.DiGraph()

    for raw in tqdm(f, desc="Parsing .gr"):
        line = raw.strip()
        if not line or line[0] == "c":
            continue
        parts = line.split()
        if parts[0] == "a":
            try:
                _, u_s, v_s, w_s = parts[:4]
            except ValueError:
                # Skip malformed line
                continue
            u = int(u_s)
            v = int(v_s)
            # weights may be integers (signed) in the DIMACS format
            try:
                w = int(w_s)
            except ValueError:
                # fallback to float
                w = float(w_s)
            # Add nodes (NetworkX will create them automatically)
            DG.add_edge(u, v, weight=w)

    f.close()
    return DG


def parse_co(f):
    """
    Parse .co coordinate content and return dict: node_id -> (x, y)
    """
    coords = {}

    for raw in f:
        line = raw.strip()
        if not line or line[0] == "c":
            continue
        parts = line.split()
        if parts[0] == "p":
            continue
        if parts[0] == "v":
            try:
                _, id_s, x_s, y_s = parts[:4]
            except ValueError:
                continue
            nid = int(id_s)
            x = float(x_s)
            y = float(y_s)
            coords[nid] = (x, y)

    return coords


if __name__ == "__main__":
    with open(
        "/home/agentolek/UC3M/heuristics/heuristics-optimization-project2/parte_2/data/USA-road-d.BAY.gr",
        "r",
    ) as f:
        DG = parse_gr(f)

    with open(
        "/home/agentolek/UC3M/heuristics/heuristics-optimization-project2/parte_2/data/USA-road-d.BAY.co",
        "r",
    ) as f:
        coords = parse_co(f)

    print(f"Attaching coords for {len(coords)} nodes (if present)...")
    nx.set_node_attributes(
        DG, values={nid: {"pos": coords[nid]} for nid in coords if nid in DG.nodes}
    )

    print("Graph loaded.")
    print("Nodes:", DG.number_of_nodes(), "Edges:", DG.number_of_edges())
    print(list(DG.successors(4)))
