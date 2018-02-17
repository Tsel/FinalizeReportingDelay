import numpy as np
import networkx as nx
import pandas as pd
import itertools

fn = "/Users/TOSS/PycharmProjects/ReportingDelay/sandbox/el.txt"
types = {'t':int, 'S':str, 'T':str}
df = pd.read_csv(fn, dtype=types, sep=',')
print(df)
n,m = df.shape

nodes = mergedlist = sorted(list(set(df['S'].values.tolist() \
								+ df['T'].values.tolist())))
print(nodes)

G = nx.DiGraph()
G.add_nodes_from(nodes)
I = np.eye(len(nodes))
print(I)


for t in range(n):
	print("              ")
	print("============> ", t)
	G = nx.DiGraph()
	dft = df[df['t'] == t]
	edges = list(zip(dft['S'].values.tolist(), dft['T'].values.tolist()))
	G.add_edges_from(edges)
	At = nx.to_numpy_matrix(G, nodes)
	At = At + I
	if t == 0:
		A = At.copy()
	else:
		print("A @ At")
		A = A @ At
		#A = np.matmul(A,At).copy()
		A = (A > 0).astype(int).copy()

	print(A)
print("Temporal range of nodes")
temprange = [x[0] for x in np.sum(A, axis=1).tolist()] # https://stackoverflow.com/questions/11264684/flatten-list-of-lists
print(temprange)
