from xml.dom.minidom import parse
import networkx as nx
# import matplotlib.pyplot as plt
import itertools
import os
import re


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

INHERITANCE = 'inh'
VARIABLE = 'var'

third_party_res = [
    re.compile('^flash.*'),
    re.compile('^com\.adobe.*'),
    re.compile('^mx.*')
]

rot_module_re = re.compile('.*Module$')

external_dependencies = set()
G = nx.DiGraph()


def build_graph():
    files = os.listdir(DATA_DIR)

    for f in files:
        if f.endswith(".xml"):
            build_graph_from_xml_report(os.path.join(DATA_DIR, f))


def build_graph_from_xml_report(report_path):
    print 'Processing mxmlc link report: %s' % report_path
    dom = parse(report_path)

    handle_external_defs(dom.getElementsByTagName('external-defs')[0])
    handle_scripts(dom.getElementsByTagName('script'))

    dom.unlink()

    print 'Graph built: %d nodes and %d edges' % (G.number_of_nodes(), G.number_of_edges())


def handle_scripts(scripts):
    print 'Handling script nodes'
    for script in scripts:
        script_name = get_script_name(script)
        if not is_third_party(script_name):
            G.add_node(script_name, is_rot_module=is_rot_module(script_name))

            for pre in script.getElementsByTagName('pre'):
                pre_name = get_id(pre)
                if not is_third_party(pre_name):
                    G.add_edge(script_name, pre_name, dep_type=INHERITANCE)

            for dep in script.getElementsByTagName('dep'):
                dep_name = get_id(dep)
                if not is_third_party(dep_name):
                    G.add_edge(script_name, dep_name, dep_type=VARIABLE)


def get_script_name(script_node):
    return get_id(script_node.getElementsByTagName('def')[0])


def get_id(node):
    return node.getAttribute('id')


def handle_external_defs(externals):
    print 'Handling external references'
    for ext in externals.getElementsByTagName('ext'):
        external_dependencies.add(get_id(ext))
    print 'Found %d external dependencies' % len(external_dependencies)


def is_third_party(name):
    if name in external_dependencies:
        return True
    for regexp in third_party_res:
        if regexp.match(name):
            return True
    return False


def is_rot_module(name):
    return True if rot_module_re.match(name) else False


def analyze_graph():
    print 'Analyzing graph'
    modules = get_rot_module_nodes()

    for source_node, target_node in itertools.permutations(modules, 2):
        source = source_node[0]
        target = target_node[0]
        if nx.has_path(G, source, target):
            print '\n%s -> %s' % (source, target)
            print nx.shortest_path(G, source=source, target=target)


def get_rot_module_nodes():
    return [n for n in G.nodes(data=True) if n[1]['is_rot_module']]


if __name__ == "__main__":
    build_graph()
    analyze_graph()
