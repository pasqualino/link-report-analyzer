import link_report_analyzer
import networkx as nx
import itertools
import re
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

rot_module_re = re.compile('.*Module$')


def analyze_graph(G):
    print 'Analyzing graph'
    modules = get_rot_module_nodes(G)

    for source, target in itertools.permutations(modules, 2):
        if nx.has_path(G, source, target):
            print '\n%s -> %s' % (source, target)
            print nx.shortest_path(G, source=source, target=target)


def get_rot_module_nodes(G):
    return [n for n in G.nodes() if is_rot_module(n)]


def is_rot_module(node):
    return rot_module_re.match(node)


def main():
    files = os.listdir(DATA_DIR)

    G = link_report_analyzer.build_graph([os.path.join(DATA_DIR, f) for f in files])
    analyze_graph(G)


if __name__ == "__main__":
    main()
