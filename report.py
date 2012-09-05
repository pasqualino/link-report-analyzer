from link_report_analyzer import build_graph
import itertools
import networkx as nx
import os
import re
import sys
from time import time


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

module_re = re.compile('.*Module$')
application_re = re.compile('.*Main$')


def analyze_graph(G):
    print 'Analyzing graph'
    start_time = time()

    print '\n\n----------------------------------------'
    print 'module -> module:'
    find_dependencies(G, is_module)

    print '\n\n----------------------------------------'
    print 'application -> application:'
    find_dependencies(G, is_application)

    print '\n\n----------------------------------------'
    print 'application -> module:'
    find_dependencies(G, is_application, is_module)

    print '\n\n----------------------------------------'
    print 'module -> application:'
    find_dependencies(G, is_module, is_application)

    print '\nAnalysis done in %0.3fs.' % (time() - start_time)


def find_dependencies(G, source_filter_function, target_filter_function=None):
    source_nodes = filter(source_filter_function, G.nodes())
    target_nodes = filter(target_filter_function, G.nodes()) if target_filter_function is not None else source_nodes

    for source, target in itertools.product(source_nodes, target_nodes):
        if not source == target and nx.has_path(G, source, target):
            print '\n%s -> %s' % (source, target)
            print nx.shortest_path(G, source=source, target=target)


def is_module(node):
    return not module_re.match(node) is None


def is_application(node):
    return not application_re.match(node) is None


def main():
    files = os.listdir(DATA_DIR)

    G = build_graph([os.path.join(DATA_DIR, f) for f in files])
    analyze_graph(G)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print 'Interrupted!'
        sys.exit(-1)
