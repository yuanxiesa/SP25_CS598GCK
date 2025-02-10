import networkit as nk
import csv
import random
import statistics

def create_graph(file_path):
    """
    Load an undirected graph from a CSV file with columns 'citing' (source) and 'cited' (target).
    Converts it to an undirected Networkit graph.
    """
    node_mapping = {}  # Map from node IDs to Networkit indices
    edges = []  # Store edges before adding to the graph

    # Read the CSV file and process edges
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header
        citing_idx = header.index("citing")
        cited_idx = header.index("cited")

        for row in reader:
            src, tgt = row[citing_idx], row[cited_idx]

            # Map nodes to indices
            if src not in node_mapping:
                node_mapping[src] = len(node_mapping)
            if tgt not in node_mapping:
                node_mapping[tgt] = len(node_mapping)

            edges.append((node_mapping[src], node_mapping[tgt]))

    # Create the graph as directed
    G = nk.Graph(len(node_mapping), weighted=False, directed=True)

    # Add edges to the graph
    for src, tgt in edges:
        G.addEdge(src, tgt, addMissing=True)

    return G, node_mapping


def find_start_node(graph, degree_D):
    """
    Find a random node in the graph with degree D.
    If no exact match is found, return None.
    """
    candidates = [node for node in graph.iterNodes() if graph.degree(node) == degree_D]
    return random.choice(candidates) if candidates else None


def random_walk_component(graph, target_size, delta, degree_D):
    """
    Perform a random walk to find a connected component of size n ± delta,
    starting from a node with degree D.
    """
    start_node = find_start_node(graph, degree_D)

    if start_node is None:
        print(f"No node with degree {degree_D} found.")
        return set()

    visited = set([start_node])
    frontier = [start_node]

    while frontier and not (target_size - delta <= len(visited) <= target_size + delta):
        current = random.choice(frontier)
        neighbors = list(graph.iterNeighbors(current))
        random.shuffle(neighbors)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)
                break  # Move step-by-step

    return visited


def compute_degree_statistics(component_G):
    """
    Compute the max, min, and median of in-degree and total degree
    for the nodes in the given component.
    """

    component_G_undirected = nk.graphtools.toUndirected(component_G)

    indegree_centrality = nk.centrality.DegreeCentrality(component_G, normalized=False, outDeg=False)
    indegree_centrality.run()
    in_degrees = [indegree_centrality.score(v) for v in range(component_G.numberOfNodes())]

    total_degree_centrality = nk.centrality.DegreeCentrality(component_G_undirected, normalized=False)
    total_degree_centrality.run()
    total_degrees = [total_degree_centrality.score(v) for v in range(component_G_undirected.numberOfNodes())]

    in_degree_stats = {
        "max_in_degree": max(in_degrees),
        "min_in_degree": min(in_degrees),
        "median_in_degree": statistics.median(in_degrees)
    }

    total_degree_stats = {
        "max_total_degree": max(total_degrees),
        "min_total_degree": min(total_degrees),
        "median_total_degree": statistics.median(total_degrees)
    }

    return in_degree_stats, total_degree_stats


def main():
    # Load the graph from a CSV file
    csv_file = "open_citations_curated.csv"  # Update this with the actual file path
    G, node_mapping = create_graph(csv_file)
    undirected_G = nk.graphtools.toUndirected(G)

    # Set parameters
    target_size = 100000
    delta = 500

    for degree_D in [100, 300, 500, 1000, 2000]:

        print("starting from node of degree {}".format(degree_D))

        # Get a connected component via random walk
        component = random_walk_component(undirected_G, target_size, delta, degree_D)
        print("the size of the component found is {}".format(len(component)))
        component_G = nk.graphtools.subgraphFromNodes(G, component)

        # Compute degree statistics
        if component:
            in_degree_stats, total_degree_stats = compute_degree_statistics(component_G)

            print("In-degree statistics:", in_degree_stats)
            print("Total degree statistics:", total_degree_stats)
        else:
            print("No valid component found.")


if __name__ == "__main__":
    main()
