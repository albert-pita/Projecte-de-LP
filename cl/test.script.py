import sys
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from antlr4 import *
from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from antlr4.InputStream import InputStream
from EnquestesVisitor import EnquestesVisitor

if len(sys.argv) > 1:
    input_stream = FileStream(sys.argv[1], encoding="utf-8")
else:
    input_stream = InputStream(input('? '))

lexer = EnquestesLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = EnquestesParser(token_stream)
tree = parser.root()
visitor = EnquestesVisitor()
G = visitor.visit(tree)

with open('graph.pkl', 'wb') as pickle_file:
    pickle.dump(G, pickle_file)

resKeeper = {}

with open('resKeeper.pkl', 'wb') as pickle_file:
    pickle.dump(resKeeper, pickle_file)

items = [(u, v) for (u, v, d) in G.edges(data=True) if d["tipus"] == 1]
enquestes = [(u, v) for (u, v, d) in G.edges(data=True) if d["tipus"] == 2]
alternatives = [(u, v) for (u, v, d) in G.edges(data=True) if d["tipus"] == 3]

pos = nx.circular_layout(G)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=600)

# edges
nx.draw_networkx_edges(G, pos, edgelist=items, edge_color='b')
nx.draw_networkx_edges(G, pos, edgelist=enquestes)
nx.draw_networkx_edges(G, pos, edgelist=alternatives, edge_color='g')

# node labels
nx.draw_networkx_labels(G, pos)

# edge labels
edge_labels_items = nx.get_edge_attributes(G, 'item')
nx.draw_networkx_edge_labels(G, pos, edge_labels_items, font_color='b')
edge_labels_alternatives = nx.get_edge_attributes(G, 'text')
nx.draw_networkx_edge_labels(G, pos, edge_labels_alternatives, font_color='g')

plt.savefig('graf.png')
plt.show()
