import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

nodes = pd.read_csv('student_nodes.csv')
edges = pd.read_csv('cheating_network_edges.csv')

#Directed graph
g = nx.from_pandas_edgelist(edges, source="source", target="target", edge_attr=True, create_using=nx.DiGraph())

#in-degree dictionary:
