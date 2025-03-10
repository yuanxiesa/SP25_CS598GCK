import pandas as pd
from tabulate import tabulate
import argparse

def read_tsv_to_tuple_list(file_path):
    """
    Reads a two-column TSV file into a list of two-element tuples.

    :param file_path: Path to the TSV file
    :return: List of two-element tuples
    """
    df = pd.read_csv(file_path)
    tuple_list = list(df.itertuples(index=False, name=None))
    return tuple_list


# report min, quantiles, median, and max of cluster sizes
def process_basic_stats(freq_list, stats):
    data = []
    for cluster_size, freq in freq_list:
        if cluster_size > 1:
            for i in range(0, freq):
                data.append(cluster_size)

    series = pd.Series(data)
    stats['min'].append(series.min())
    stats['25% quantile'].append(series.quantile(0.25))
    stats['median'].append(series.median())
    stats['75% quantile'].append(series.quantile(0.75))
    stats['max'].append(series.max())

    return stats


# compute the number and percentage of singleton and non-singleton clusters

def singleton_vs_non_singleton(data, singleton_analysis):
    singleton_cluster_count = 0
    non_singleton_cluster_count = 0
    total_node_count = 0
    singleton_node_count = 0
    non_singleton_node_count = 0

    for x, y in data:
        if x != 1:
            non_singleton_cluster_count += y
            total_node_count += x * y
            non_singleton_node_count += x * y
        else:
            singleton_cluster_count += y
            total_node_count += x * y
            singleton_node_count += x * y

    total_cluster_count = singleton_cluster_count + non_singleton_cluster_count

    singleton_analysis['singleton node count'].append(str(singleton_node_count))
    singleton_analysis['non-singleton node count'].append(str(non_singleton_node_count))
    singleton_analysis['total cluster count'].append(str(total_cluster_count))
    singleton_analysis['node coverage (%)'].append(non_singleton_node_count / total_node_count * 100)
    singleton_analysis['singleton cluster count'].append(str(singleton_cluster_count))
    singleton_analysis['non-singleton cluster count'].append(str(non_singleton_cluster_count))
    singleton_analysis['percent singleton cluster (%)'].append(singleton_cluster_count / total_cluster_count * 100)
    singleton_analysis['percent non-singleton cluster (%)'].append(non_singleton_cluster_count / total_cluster_count * 100)

    return singleton_analysis

def create_file_path(prefix):
    file_path_1 = f'{prefix}_Leiden_CPM_01.csv'
    file_path_2 = f'{prefix}_Leiden_CPM_001.csv'
    file_path_3 = f'{prefix}_Leiden_modularity.csv'
    file_path_l = [file_path_1, file_path_2,file_path_3]
    return file_path_l

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="perform Leiden clustering")
    parser.add_argument("prefix", help="the prefix for the input files")

    args = parser.parse_args()

    file_path_l = create_file_path(args.prefix)

    stats = {
        'min': [],
        '25% quantile': [],
        'median': [],
        '75% quantile': [],
        'max': []
    }

    singleton = {

        "singleton node count": [],
        "non-singleton node count": [],
        "total cluster count": [],
        "node coverage (%)": [],
        "singleton cluster count": [],
        "non-singleton cluster count": [],
        "percent singleton cluster (%)": [],
        "percent non-singleton cluster (%)": []

    }

    for file_path in file_path_l:
        read_tsv_to_tuple_list(file_path)
        data = read_tsv_to_tuple_list(file_path)
        stats = process_basic_stats(data, stats)
        singleton = singleton_vs_non_singleton(data, singleton)

    # create final df
    df = pd.DataFrame.from_dict(singleton)
    df.rename(index={0: 'Leiden CPM 0.01',
                     1: 'Leiden CPM 0.001',
                     2: 'Leiden Modularity'}, inplace=True)
    df = df.T

    # first table: show four digits & scientific notation
    print(tabulate(df, headers='keys', floatfmt=".4f"))

    print()

    # second table: show zero digits
    print(tabulate(df, headers='keys', floatfmt=".0f"))

    print()

    df = pd.DataFrame.from_dict(stats)
    df.rename(index={0: 'Leiden CPM 0.01',
                     1: 'Leiden CPM 0.001',
                     2: 'Leiden Modularity'}, inplace=True)
    df = df.T
    # second table: show zero digits
    print(tabulate(df, headers='keys', floatfmt=".0f"))


if __name__ == '__main__':
    main()