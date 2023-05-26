from pyvis.network import Network
import networkx as nx
import json
nx_graph = nx.cycle_graph(10)
nx_graph.nodes[1]['title'] = 'Number 1'
nx_graph.nodes[1]['group'] = 1
nx_graph.nodes[3]['title'] = 'I belong to a different group!'
nx_graph.nodes[3]['group'] = 10
nx_graph.add_node(20, size=20, title='couple', group=2)
nx_graph.add_node(21, size=15, title='couple', group=2)
nx_graph.add_edge(20, 21, weight=5)
nx_graph.add_node(25, size=25, label='lonely', title='lonely node', group=3)
nt = Network("750px", '80%',directed=True)
# populates the nodes and edges data structures
nt.from_nx(nx_graph)
options = {
  "manipulation": {
    "enabled": True,
    "initiallyActive": True
  },
}
nt.options.configure.enabled = False
options_json = json.dumps(options)
nodes, edges, heading, height, width, options = nt.get_network_data()
nt.set_options(options_json)
nt.save_graph('nx.html')
nt_json=json.dumps(nodes)
print(nt_json)

