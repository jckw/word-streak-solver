import dawg
import networkx as nx

b = [[]*4]*4

for i in range(4): 
    b[i] = input().lower()
    if len(b[i]) != 4:
        raise ValueError("Incorrect number of letters in line")

with open('words.txt') as f:
    words = f.read().splitlines()

cdawg = dawg.CompletionDAWG(words)

def fmtnode(i, j):
    return (b[i][j], (i,j))

e = []

for i in range(3):
    for j in range(3):
        e += [  (fmtnode(i,j), fmtnode(i, j+1)),
                (fmtnode(i,j), fmtnode(i+1, j+1)),
                (fmtnode(i,j), fmtnode(i+1, j)),
                (fmtnode(i+1,j), fmtnode(i+1, j+1)),
                (fmtnode(i,j+1), fmtnode(i+1, j+1)),
                (fmtnode(i+1,j), fmtnode(i, j+1))]

g = nx.Graph()
g.add_edges_from(e)

def build(ssf, start, visited):
    p = []
    xs = set(g.neighbors(start)).difference(visited)
    if len(xs) == 0:
        return []
    for t,n in xs:
        ns = ssf + t
        if ns in cdawg:
            p += [ns]
        if cdawg.has_keys_with_prefix(ns):
            p += build(ns, (t,n), visited + [(t,n)])
    return p

sols = []

for i in range(4):
    for j in range(4):
        sols += build(b[i][j], fmtnode(i,j), [fmtnode(i,j)])

for s in sorted(set(sols), key=len, reverse=True):
    print(s)
