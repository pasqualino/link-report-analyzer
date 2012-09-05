from xml.dom.minidom import parse
import networkx as nx
import re
import time


INHERITANCE = 'inh'
VARIABLE = 'var'

third_party_res = [
    re.compile('^flash.*'),
    re.compile('^com\.adobe.*'),
    re.compile('^mx.*')
]

external_dependencies = set()
G = nx.DiGraph()


def build_graph(files):
    start_time = time.time() * 1000
    for f in files:
        if f.endswith(".xml"):
            build_graph_from_xml_report(f)

    end_time = time.time() * 1000
    print 'Graph built in %d ms. %d nodes and %d edges' % (end_time - start_time, G.number_of_nodes(), G.number_of_edges())
    return G


def build_graph_from_xml_report(report_path):
    print 'Processing mxmlc link report: %s' % report_path
    dom = parse(report_path)

    handle_external_defs(dom.getElementsByTagName('external-defs')[0])
    handle_scripts(dom.getElementsByTagName('script'))

    dom.unlink()


def handle_scripts(scripts):
    for script in scripts:
        script_name = get_script_name(script)
        if not is_third_party(script_name):
            G.add_node(script_name)

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
    for ext in externals.getElementsByTagName('ext'):
        external_dependencies.add(get_id(ext))


def is_third_party(name):
    if name in external_dependencies:
        return True
    for regexp in third_party_res:
        if regexp.match(name):
            return True
    return False
