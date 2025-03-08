import igraph as ig
import leidenalg as la
import csv
import time
from collections import Counter
import argparse
import random

def read_edge_list_from_tsv(file_path):
    """
    Reads an edge list from a TSV file.

    :param file_path: Path to the TSV file
    :return: List of tuples representing edges
    """
    edge_list = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            edge_list.append((int(row[0]), int(row[1])))
    return edge_list


def create_graph_from_edge_list(edge_list):
    """
    Creates a graph from a given edge list using igraph and plots it.

    :param edge_list: List of tuples representing edges (e.g., [(0, 1), (1, 2), (2, 0)])
    :return: igraph Graph object
    """

    # Create graph
    g = ig.Graph(edges=edge_list, directed=False)

    # Set vertex labels to their indices
    g.vs['label'] = [str(v.index) for v in g.vs]

    return g


def count_nodes_and_edges(graph):
    """
    Counts the number of nodes and edges in a graph.

    :param graph: igraph Graph object
    :return: Tuple (number of nodes, number of edges)
    """
    num_nodes = graph.vcount()
    num_edges = graph.ecount()
    return num_nodes, num_edges


def cluster_graph_with_leiden_1(graph, seed=42):
    """
    Clusters the graph using the Leiden algorithm with CPM resolution 0.01 and measures run time.

    :param graph: igraph Graph object
    :return: Tuple (clustering object, run time in seconds)
    """
    start_time = time.time()
    random.seed(seed)
    partition = la.find_partition(graph, la.CPMVertexPartition, resolution_parameter=0.01)
    end_time = time.time()
    run_time = end_time - start_time
    print("Finished Leiden CPM 0.01 in {} seconds".format(run_time))

    return partition


def cluster_graph_with_leiden_2(graph, seed=42):
    """
    Clusters the graph using the Leiden algorithm with CPM resolution 0.001 and measures run time.

    :param graph: igraph Graph object
    :return: Tuple (clustering object, run time in seconds)
    """
    start_time = time.time()
    random.seed(seed)
    partition = la.find_partition(graph, la.CPMVertexPartition, resolution_parameter=0.001)
    end_time = time.time()
    run_time = end_time - start_time
    print("Finished Leiden CPM 0.001 in {} seconds".format(run_time))

    return partition


def cluster_graph_with_leiden_3(graph, seed=42):
    """
    Clusters the graph using the Leiden algorithm with modularity and measures run time.

    :param graph: igraph Graph object
    :return: Tuple (clustering object, run time in seconds)
    """
    start_time = time.time()
    random.seed(seed)
    partition = la.find_partition(graph, la.ModularityVertexPartition)
    end_time = time.time()
    run_time = end_time - start_time
    print("Finished Leiden Modularity in {} seconds".format(run_time))

    return partition


def save_cluster_sizes_to_csv(cluster_sizes, output_file):
    """
    Saves the cluster sizes to a CSV file.

    :param cluster_sizes: List of cluster sizes
    :param output_file: Output CSV file path
    """
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Cluster Size", "Count"])
        for size, count in Counter(cluster_sizes).items():
            writer.writerow([size, count])

def main():

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="perform Leiden clustering")
    parser.add_argument("input_file", help="Path to the input TSV file")
    parser.add_argument("label", help="label (an easy to remember name for the graph")

    args = parser.parse_args()

    # Read edge list from TSV
    file_path = args.input_file # Update with the correct file path
    edge_list = read_edge_list_from_tsv(file_path)

    # obtain label
    label = args.label

    # Create and display the graph
    graph = create_graph_from_edge_list(edge_list)

    n, m = count_nodes_and_edges(graph)
    print("Number of Nodes: {}".format(n))
    print("Number of Edges: {}".format(m))

    # get partition from Leiden CPM 0.01
    print("Computing: Leiden CPM 0.01...")
    partition_1 = cluster_graph_with_leiden_1(graph)
    print("Computing: Leiden CPM 0.001...")
    partition_2 = cluster_graph_with_leiden_2(graph)
    print("Computing: Leiden Modularity...")
    partition_3 = cluster_graph_with_leiden_3(graph)

    cluster_sizes_1 = [len(cluster) for cluster in partition_1]
    cluster_sizes_2 = [len(cluster) for cluster in partition_2]
    cluster_sizes_3 = [len(cluster) for cluster in partition_3]

    # save counter output to different csv files for local examination
    print("Saving results Leiden CPM 0.01...")
    save_cluster_sizes_to_csv(cluster_sizes_1, f"{label}_Leiden_CPM_01.csv")
    print("Saving results Leiden CPM 0.001...")
    save_cluster_sizes_to_csv(cluster_sizes_2, f"{label}_Leiden_CPM_001.csv")
    print("Saving results Leiden Modularity...")
    save_cluster_sizes_to_csv(cluster_sizes_3, f"{label}_Leiden_CPM_modularity.csv")

if __name__ == '__main__':
    main()
