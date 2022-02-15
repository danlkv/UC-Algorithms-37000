import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sys

def dbg(*x):
    print('DBG', *x)

def get_level(G, leaves):
    level = []
    for u, v in G.edges:
        if v in leaves:
            level.append(u)
    return list(set(level))

def children(G, node):
    ch = []
    for u, v in G.edges:
        if u==node:
            ch.append(v)
    return ch

def descendants(G, node):
    return nx.algorithms.dag.descendants(G, node)

def solve_LIS(G: nx.Graph, vals, root=0):
    T = np.zeros(G.number_of_nodes(), dtype=int)
    nodes = list(G.nodes())
    leaves = [x for x in G.nodes if G.degree(x) == 1]
    if root in leaves:
        leaves = [x for x in leaves if x != root]

    dbg('leaves', leaves)
    dbg('root', root)
    tree = nx.bfs_tree(G, root)
    nodes = list(tree.nodes())
    print('tree', list(tree.edges))
    print('G', list(G.edges))
    print('des', descendants(tree, root))
    for leaf in leaves:
        T[nodes.index(leaf)] = 1

    def pop_level(tree, level):
        for node in level:
            ch = children(tree, node)
            valnode = vals[nodes.index(node)]
            tt = []
            for c in ch:
                des = list(descendants(tree, c)) + [c]
                if T[nodes.index(c)] == 0:
                    tt = None
                    break
                desv = [T[nodes.index(x)] for x in des if vals[nodes.index(x)]<=valnode]
                dbg('c', c, 'devs', desv, 'valnode', valnode, 'des', des)
                dbg('desv', [vals[nodes.index(x)] for x in des])
                if len(desv):
                    tt.append(np.max(desv))
                else:
                    tt.append(0)
            dbg('tt', node, tt, ' valnode', valnode)
            if tt is None:
                continue
            T[nodes.index(node)] = 1+sum(tt)
    level = get_level(tree, leaves)
    pop_level(tree, level)
    dbg('level0', level)
    k = 0
    while min(T) == 0:
        k+=1
        level = get_level(tree, level)
        dbg('level', level)
        pop_level(tree, level)
        if k>100:
            raise('Recursion limit')
            break



    print(nx.forest_str(tree))
    data = nx.DiGraph()
    for u, v in tree.edges:
        x, y = T[nodes.index(u)], T[nodes.index(v)]
        data.add_node(u, data=x)
        data.add_node(v, data=y)
        data.add_edge(u, v)
    print(nx.forest_str(data, sources=[13]))
    return data


def treemap(tree: nx.DiGraph, func, root):
    from functools import lru_cache
    valmap = {}
    @lru_cache()
    def get_val(node):
        desc = children(tree, node)
        if len(desc) == 0:
            r = func(node, [])
        else:
            vs = [get_val(d) for d in desc]
            r = func(node, vs)
        valmap[node] = r
        return r

    return get_val(root), valmap


def main(N = 15, Ntests=1, root=0):
    np.random.seed(10)

    Gs = [nx.random_tree(N, seed=s) for s in range(Ntests)]
    vals_g = [np.random.randint(-N, N, size=N) for s in range(Ntests)]
    sols = []
    for G, vals in zip(Gs, vals_g):
        solution = solve_LIS(G, vals, root=root)
        sols.append([solution, vals, root])
    return sols


def vis_sol(soldef):
    solution, vals, root = soldef
    pos = nx.spring_layout(solution)
    labels = nx.get_node_attributes(solution, 'data')
    nodes = list(solution.nodes)
    # redundant
    valm = [vals[nodes.index(x)] for x in nodes]
    labels = {k: f'N{k} V{v} T{t}' for v, (k, t) in zip(valm, labels.items())}
    tdata = np.array(list(nx.get_node_attributes(solution, 'data').values()))
    colors = [plt.cm.gnuplot(x) for x in tdata/np.max(tdata)]
    colors = ['red' if n==root else x for n, x in zip(solution.nodes, colors)]
    f, axs = plt.subplots(1, 2, figsize=(12, 6))
    plt.sca(axs[0])
    nx.draw_kamada_kawai(nx.Graph(solution), labels=labels, node_color=colors)

    def cumsum(node, cvals):
        vnode = tdata[nodes.index(node)]
        return max(vnode, sum(cvals))

    val, valmap = treemap(solution, cumsum, root)
    print('SOLUTION', val, valmap)
    #pos = nx.planar_layout(solution)
    plt.sca(axs[1])
    #nx.draw_networkx_edges(solution, pos, ax=plt.gca())
    nx.draw_kamada_kawai(nx.Graph(solution), labels=valmap, node_color=colors)
    print('Max changes', solution.number_of_nodes() - val)
    plt.savefig('/mnt/c/Users/danlk/Desktop/out.png')


if __name__=='__main__':
    if len(sys.argv)>1:
        sols = main(int(sys.argv[1]))
    else:
        sols = main()
    vis_sol(sols[-1])

