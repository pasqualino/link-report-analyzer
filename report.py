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

    print '\nModule interdependencies:'
    find_interdependendies(G, is_module)

    print '\nApplication interdependencies:'
    find_interdependendies(G, is_application)


def find_interdependendies(G, filter_function):
    modules = filter(filter_function, G.nodes())

    for source, target in itertools.permutations(modules, 2):
        if nx.has_path(G, source, target):
            print '\n%s -> %s' % (source, target)
            print nx.shortest_path(G, source=source, target=target)


def is_module(node):
    return not module_re.match(node) is None


def is_application(node):
    return not application_re.match(node) is None


def main():
    files = os.listdir(DATA_DIR)

    G = link_report_analyzer.build_graph([os.path.join(DATA_DIR, f) for f in files])
    analyze_graph(G)


if __name__ == "__main__":
    main()
