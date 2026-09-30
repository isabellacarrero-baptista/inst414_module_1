import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

nodes = pd.read_csv('student_nodes.csv')
edges = pd.read_csv('cheating_network_edges.csv')

#Directed graph
g = nx.from_pandas_edgelist(edges, source="source", target="target", edge_attr=True, create_using=nx.DiGraph())

#in-degree dictionary:
in_degree = dict(g.in_degree())
#out-degree dictionary:
out_degree = dict(g.out_degree())

#Adding in-degree and out-degree numbers to nodes dataset
nodes["in_degree"] = nodes["student_id"].map(in_degree)
nodes["out_degree"] = nodes["student_id"].map(out_degree)

#Converting NaN to 0  
nodes.fillna(0, inplace=True)

#Calculating total degree
nodes["total_degree"] = nodes["in_degree"] + nodes["out_degree"]

#Printing the top 10 distributors of cheating material
top_distributors = nodes.sort_values(by="out_degree", ascending=False)
print(top_distributors.head(10))

#Printing the top 10 receivers of cheating material
top_receivers = nodes.sort_values(by="in_degree", ascending=False)
print(top_receivers.head(10))

#Printing top students with total degree
print("Total degree:")
print(nodes.sort_values(by="total_degree", ascending=False).head(10))

#Correlation between distributors and receivers
d_r_correlation = nodes["out_degree"].corr(nodes["in_degree"])
print(d_r_correlation)

#Scatter plot to compare the out degree and in degree
plt.scatter(nodes["out_degree"], nodes["in_degree"])
plt.xlabel("Distributors of cheating material")
plt.ylabel("Receivers of cheating material")
plt.title("Cheating distribution vs Cheating receiving")
plt.show()


