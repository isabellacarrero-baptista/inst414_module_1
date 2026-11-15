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

#Network Graph:

from matplotlib.lines import Line2D

student_info = nodes.set_index("student_id").to_dict("index")
nx.set_node_attributes(g, student_info)

#Graphing total degree
total_degree = {student: in_degree[student] + out_degree[student] for student in g.nodes()}

node_sizes = [100 + total_degree[node] * 180for node in g.nodes()]

majors = sorted(nodes["major"].dropna().unique())
color_map = plt.cm.tab10

major_colors = {
    major: color_map(i % 10)
    for i, major in enumerate(majors)
}

node_colors = [
    major_colors.get(g.nodes[node].get("major"), "gray")
    for node in g.nodes()
]

#Network layout
pos = nx.spring_layout(
    g,
    seed=42,
    k=0.7,
    iterations=100
)

plt.figure(figsize=(17, 13))

#Edges with directional arrows
nx.draw_networkx_edges(
    g,
    pos,
    edge_color="gray",
    alpha=0.35,
    arrows=True,
    arrowsize=12,
    width=1,
    connectionstyle="arc3,rad=0.08"
)

#Drawing the nodes
nx.draw_networkx_nodes(
    g,
    pos,
    node_size=node_sizes,
    node_color=node_colors,
    alpha=0.85,
    edgecolors="black",
    linewidths=0.5
)

#Labeling the top 10 most connected students
top_students = sorted(total_degree, key=total_degree.get, reverse=True)[:10]

labels = {student: student for student in top_students}

nx.draw_networkx_labels(
    g,
    pos,
    labels=labels,
    font_size=9,
    font_weight="bold"
)

#Legend for academic majors
legend_elements = [
    Line2D(
        [0], [0],
        marker="o",
        color="w",
        label=major,
        markerfacecolor=major_colors[major],
        markersize=9
    )
    for major in majors
]

plt.legend(
    handles=legend_elements,
    title="Student Major",
    loc="upper left",
    bbox_to_anchor=(1, 1)
)

plt.title(
    "Directed Student Cheating Network",
    fontsize=18,
    fontweight="bold"
)

plt.figtext(
    0.5, 0.02,
    "Node size represents total degree. "
    "Arrows indicate the direction of material transfer. "
    "Labels identify the 10 most connected students.",
    ha="center",
    fontsize=10
)

plt.axis("off")
plt.show()


