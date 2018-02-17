import pandas as pd
import networkx as nx


#
# Main routine
#
def readedgelist(fn):
    """
    reads edgelist form csv and creates pandas dataframe
    scv file needs to have the following column header:

    S,T,VOL,"ZUGA_DATE","MELD_DATE",MELD_DELAY

    all columns except VOL and MELD_DELAY (which are of type int) are of type string

    :param fn:
    """
    dtypes = {"S": str, "T": str, "VOL": int, "ZUGA_DATE": str, "MELD_DATE": str, "MELD_DELAY": int}

    return pd.read_csv(fn, sep=',', dtype=dtypes,
                       parse_dates=["ZUGA_DATE", "MELD_DATE"],
                       infer_datetime_format=True,
                       )


def getsourcenodes(df):
    s = df['S'].values.tolist()
    # print(s)
    return s


def gettargetnodes(df):
    t = df['T'].values.tolist()
    # print(t)
    return t


def getedgevolume(df):
    v = df['VOL'].values.tolist()
    # print(v)
    return v


def getnodes(df):
    # returns triple
    return set(getsourcenodes(df) + gettargetnodes(df))


def getedges(df):
    sourcenodes = getsourcenodes(df)
    targetnodes = gettargetnodes(df)
    volume = getedgevolume(df)
    return list(zip(sourcenodes, targetnodes, volume))


def addvolumeedges(D, edges):
    for e in edges:
        s,t,v = e
        if D.has_edge(s,t):
            oldv = D[s][t]['VOL']
            newv = oldv + v
            D[s][t]['VOL'] = newv
        else:
            D.add_edge(s,t, VOL = v)
    return D


def getuniquedelayssorted(df):
    return sorted(set(df['MELD_DELAY'].values.tolist()))


if __name__ == "__main__":
    fn_edgelist = "/Users/TOSS/Documents/Projects/ReportingDelay/data/Delay2006.csv"
    """
    Networks are created from a edgelist. Minimal edgelists contain SOURCE and Target nodes.
    
    """
    #
    # read the edgelist data and create pandas dataframe
    # pandas data frame will contain variables:
    # S,T,VOL,"ZUGA_DATE","MELD_DATE",MELD_DELAY
    # The dataframe df_edgelist contains all the edges reported from the beginning of 2006
    # until end of 2010.
    # From this dataframe we can add all nodes to the Graph G which had traded livestock pigs in 2006, and
    # for which trade has been reported until the end of 2010.
    #
    df_edgelist = readedgelist(fn_edgelist)
    print(df_edgelist.shape)
    # print(df_edgelist.dtypes)
    #
    # get nodes form pandas data frame (unique (S nodes + T nodes))
    # nodes = getnodes(df_edgelist)
    # print(len(nodes))
    # G = nx.DiGraph()
    # G.add_nodes_from(nodes)
    #
    # get all realized reporting delays
    delays = getuniquedelayssorted(df_edgelist)
    # print(delays[7:])
    for delay in delays[7:]:
        dfd = df_edgelist[df_edgelist['MELD_DELAY'] <= delay]
        G = nx.DiGraph()
        # nodes = getnodes(df_edgelist)
        # G.add_nodes_from(nodes)
        edges = getedges(dfd)
        G = addvolumeedges(G, edges)
        print(delay, nx.density(G),
              G.size(weight='VOL'),     # Summe der Gewichte hier Handelsvolumne
              nx.number_of_nodes(G),    # Summe der Knoten
              nx.number_of_edges(G))    # Summe der Kanten


    #
    # The matrix elements of adjacency matrix of graph G are all zero, no edges had been added to the
    # graph so far.
    #
    # we now add those edges which were reported not later than 7 days after animals had been moved
    # df7 = df_edgelist[df_edgelist['MELD_DELAY'] <= 7]
    # print(df7.shape)
    # edges = getedges(df7)
    # print(len(edges))
    #
    # The resulting Graph is a directed graph. Could also be a multigraph.
    # In this case, if edges occur more than once, volume is increased by addition
    #
    # G = addvolumeedges(G, edges)
    #print(G.edges(data=True))

    # G.add_edges_from(edges)
    # create network G from pandas
    # G = createGraph(df_edgelist)
    # G = nx.from_pandas_dataframe(df_edgelist,"S", "T", edge_attr="VOL", create_using=nx.DiGraph())
    # print("Number of nodes in G: ", nx.number_of_nodes(G))
    # print("Number of edges in G: ", nx.number_of_edges(G))
