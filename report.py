import link_report_analyzer
import networkx as nx
import itertools
import re
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

module_re = re.compile('.*Module$')
application_re = re.compile('.*Main$')


def analyze_graph(G):
    print 'Analyzing graph'
    find_module_interdependendies(G)


def find_module_interdependendies(G):
    modules = filter(is_module, G.nodes())

    for source, target in itertools.permutations(modules, 2):
        if nx.has_path(G, source, target):
            print '\n%s -> %s' % (source, target)
            print nx.shortest_path(G, source=source, target=target)


def is_module(node):
    return not module_re.match(node) is None


def main():
    files = os.listdir(DATA_DIR)

    G = link_report_analyzer.build_graph([os.path.join(DATA_DIR, f) for f in files])
    analyze_graph(G)


if __name__ == "__main__":
    main()
