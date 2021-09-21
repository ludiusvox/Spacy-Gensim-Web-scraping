# SchedulingSkeleton.py
# Copyright 2021 Dr. Collin F. Lynch
#
# This provides skeleton code for the scheduling problem
# for Week 6 of the AI Academy course.  It provide a basic
# class structure for the problem and should be used as
# a guide for implementation.


# Imports
# ==================================

import re
import networkx as nx
import matplotlib.pyplot as pyplot
import pandas as pd


#
# ==================================


class SchedulingProblem(object):
    """
    This class wraps up the business of the scheduling problem
    for the sake of clarity.  On load it will pull in a problem
    file and then handle the calculations.  It has a built in 
    method to actually print the directed graph for the user.
    """

    # Initialization
    # ---------------------------------------
    def __init__(self, FileName):
        self.Graph = nx.DiGraph()
        self.V = set()
        """
        Load in the specified file.  And generate
        the relevant storage.

        Parameters
        ----------
        FileName : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        with open("Task2.txt", 'r') as Input:
            self.Variables = []
            NextLine = Input.readline()[:-1]
            while (NextLine):
                # print(NextLine)
                Match = VAR_ROW3.match(NextLine)
                if Match:
                    self.V = Match.groups()

                    self.Graph.add_edge(self.V[2], self.V[0], weight=int(self.V[1]))
                    self.Graph.add_node(self.V[0], weight=int(self.V[1]))

                    # nx.set_edge_attributes(g, values=self.V[1], name='Dur')

                    self.Variables.append(Match.groups())

                else:
                    Match1 = VAR_ROW2.match(NextLine)
                    if Match1:
                        self.V = Match1.groups()

                        self.Graph.add_edge(self.V[2], self.V[0], weight=int(self.V[1]))
                        self.Graph.add_node(self.V[0], weight=int(self.V[1]))
                        self.Variables.append(Match1.groups())
                    else:
                        Match2 = VAR_ROW1.match(NextLine)
                        if Match2:
                            self.V = Match2.groups()

                            self.Graph.add_node(self.V[0], weight=int(self.V[1]))
                            self.Variables.append(Match2.groups())
                NextLine = Input.readline()[:-1]

        # Generate storage.

        self.df = pd.DataFrame(self.Variables, columns=["Name", "Dur", "Parent"])
        # Do the file loading.
        # SchedulingProblem.add_task(self,self.df['Name'],self.df['Dur'],self.df['Parent'])

        print(self.Graph.nodes(data=True))

    def update_early_properties(self):
        end_nodes = []
        for node in (n for n, d in self.Graph.out_degree if d == 0):
            end_nodes.append(node)
        pass

    def add_task(self, Name, Dur, ParentNames):
        """
        Add in the specified task 

        Parameters
        ----------
        Name : TYPE
            DESCRIPTION.
        Duration : TYPE
            DESCRIPTION.
        Parents : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        for names in Name:
            self.Graph.add_node(names)
        print(self.Graph.nodes())

        self.G = nx.from_pandas_edgelist(self.df, 'Name', 'Dur', 'Parent')

    # Calculations
    # ---------------------------------------------

    def calc_es(self):
        """
        Calculate the early start of each item.
        

        Returns
        -------
        None."""

        myDict = {}
        # First set the ES of the start.
        # self.Graph.nodes["end"]["es"] = 0

        # Then we deal with the subsequent items.
        # WorkingNodes = [self.Graph.successors("start")]

        i = 0
        # Loop till the queue is done.
        for path in nx.all_simple_paths(self.Graph, source="start", target=["end"]):
            print(path)
            myDict[i] = path
            i = i + 1
        # print(myDict)

        subgraph0 = self.Graph.subgraph(myDict[0])
        subgraph1 = self.Graph.subgraph(myDict[1])
        subgraph2 = self.Graph.subgraph(myDict[2])
        subgraph3 = self.Graph.subgraph(myDict[3])
        G0 = self.Graph.subgraph(subgraph0.nodes())
        G1 = self.Graph.subgraph(subgraph1.nodes())
        G2 = self.Graph.subgraph(subgraph2.nodes())
        G3 = self.Graph.subgraph(subgraph3.nodes())
        # print(G0)
        # print(G0.edges(data=True))
        # print(G1)
        # print(G1.edges(data=True))
        # print(G2)
        # print(G2.edges(data=True))
        # print(G3)
        # print(G3.edges(data=True))

        len_path = dict(nx.all_pairs_dijkstra(G0, weight='weight'))

        nodes = list(G0.nodes())
        results = pd.DataFrame()

        starting_point = []
        for i in range(len(nodes)):
            results = results.append(pd.DataFrame(len_path[nodes[i]]).T.reset_index())
            starting_point = starting_point + [nodes[i]] * len(len_path[nodes[i]][1])

        paths_df = pd.DataFrame()
        paths_df['starting_point'] = starting_point

        results.columns = ['ending_point', 'weight', 'path']
        results = results.reset_index()
        del results['index']

        results = pd.concat((paths_df, results), axis=1)
        # print(results.loc[:])
        # -----------------------------------------
        len_path = dict(nx.all_pairs_dijkstra(G1, weight='weight'))

        nodes = list(G1.nodes())
        results = pd.DataFrame()

        starting_point = []
        for i in range(len(nodes)):
            results = results.append(pd.DataFrame(len_path[nodes[i]]).T.reset_index())
            starting_point = starting_point + [nodes[i]] * len(len_path[nodes[i]][1])

        paths_df = pd.DataFrame()
        paths_df['starting_point'] = starting_point

        results.columns = ['ending_point', 'weight', 'path']
        results = results.reset_index()
        del results['index']

        results = pd.concat((paths_df, results), axis=1)
        # print(results.loc[:])
        # ------------------------------------------
        len_path = dict(nx.all_pairs_dijkstra(G2, weight='weight'))

        nodes = list(G2.nodes())
        results = pd.DataFrame()

        starting_point = []
        for i in range(len(nodes)):
            results = results.append(pd.DataFrame(len_path[nodes[i]]).T.reset_index())
            starting_point = starting_point + [nodes[i]] * len(len_path[nodes[i]][1])

        paths_df = pd.DataFrame()
        paths_df['starting_point'] = starting_point

        results.columns = ['ending_point', 'weight', 'path']
        results = results.reset_index()
        del results['index']

        results = pd.concat((paths_df, results), axis=1)
        # print(results.loc[:])
        # ---------------------------------
        len_path = dict(nx.all_pairs_dijkstra(G3, weight='weight'))

        nodes = list(G3.nodes())
        results = pd.DataFrame()

        starting_point = []
        for i in range(len(nodes)):
            results = results.append(pd.DataFrame(len_path[nodes[i]]).T.reset_index())
            starting_point = starting_point + [nodes[i]] * len(len_path[nodes[i]][1])

        paths_df = pd.DataFrame()
        paths_df['starting_point'] = starting_point

        results.columns = ['ending_point', 'weight', 'path']
        results = results.reset_index()
        del results['index']

        results = pd.concat((paths_df, results), axis=1)
        # print(results.loc[:])
        # ---------------------------------
        return G0, G1, G2, G3

    def calc_node_es(self, NodeName):
        """
        Calculate the ES for the node.

        Parameters
        ----------
        NodeName : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        # Make sure all the parents are set.
        # Find the slowest parent.
        # Set my value.
        self.Nodes = self.Graph.predecessors("end")
        # print(self.Nodes)

    # Output
    # --------------------------------------------
    def drawgraph(self):
        """
        Draw out the graph for the user.

        Returns
        -------
        None.

        """
        nx.draw(self.Graph, with_labels=True, arrows=True)
        pyplot.show()
        nx.write_gexf(self.Graph, "plot.gexf")
        pyplot.show()


VAR_ROW1 = re.compile("^(?P<Node>[a-z]+) (?P<Dur>[0-9]+) :")
VAR_ROW2 = re.compile("^(?P<Node>[a-z]+) (?P<Dur>[0-9]+) : (?P<P1>[a-z]+)")
VAR_ROW3 = re.compile("^(?P<Node>[a-z]+) (?P<Dur>[0-9]+) : (?P<P1>[a-z]+) (?P<P2>[a-z]+)")


def update_early_properties(graph, node: "str"):
    """
    Calculate early_start and early_finish.
    Start with an end node. This function will recurse back to the
    start node(s) and calculate the early_start and early_finish
    properties along the way.
    """
    predecessors = list(graph.predecessors(node))

    if len(predecessors) == 0:
        # This node has no predecessors. By definition, it has an
        # early_start of zero and an early_finish of its duration.
        graph.nodes[node]['es'] = 0.0
        graph.nodes[node]['ef'] = graph.nodes[node]['weight']

    max_early_finish = 0.0
    for predecessor in predecessors:
        if graph[predecessor].get('ef', None) is None:
            update_early_properties(graph, predecessor)  # NOTE THE RECURSIVE CALL HERE
        if graph.nodes[predecessor]['ef'] > max_early_finish:
            max_early_finish = graph.nodes[predecessor]['ef']

    # OK, we can now update this node's "early" properties
    graph.nodes[node]['es'] = max_early_finish

    graph.nodes[node]['ef'] = (
            max_early_finish + graph.nodes[node]['weight'])

    print("Early Start: ")
    print(max_early_finish)


def update_late_properties(graph, node: "str"):
    """
    Calculate late_start and late_finish.
    Start with an end node. This function will recurse back to the
    start node(s) and calculate the late_start and late_finish
    properties along the way.
    """
    successors = list(graph.successors(node))

    if len(successors) == 0:
        # This node has no predecessors. By definition, it has an
        # early_start of zero and an early_finish of its duration.
        graph.nodes[node]['ls'] = graph.nodes[node]['weight']
        graph.nodes[node]['lf'] = graph.nodes[node]['weight'] + graph.nodes[node]['weight']

    max_late_finish = 0.00
    for successor in successors:
        if graph[successor].get('lf', None) is None:
            update_late_properties(graph, successor)  # NOTE THE RECURSIVE CALL HERE
        if graph.nodes[successor]['lf'] > max_late_finish:
            max_late_finish = graph.nodes[successor]['lf']

    # OK, we can now update this node's "late" properties
    graph.nodes[node]['ls'] = max_late_finish

    graph.nodes[node]['lf'] = (
            max_late_finish + graph.nodes[node]['weight'])

    print("late Start: ")
    print(max_late_finish)
def find_critical_path(graph, start_node: str, end_node: str) -> list[str]:
    """
    Find the critical path from start_node to end_node.

    This method is recursive and performs a depth-first search for a path
    of nodes from start_node to end_node that all have a slack of zero (0).

    NOTE: There may be more than one such path. This only returns the first
          one found.
    """
    def _find_critical_path(start_node: str, end_node: str) -> list[str]:
        graph.nodes[start_node]['slack'] = 0

        if start_node == end_node:
            return [start_node]

        if graph.nodes[start_node]['slack'] == 0:
            successors = graph.successors(start_node)
            for successor in successors:
                response = _find_critical_path(successor, end_node)
                if response is not None:
                    return [start_node] + response

    return _find_critical_path(start_node, end_node)

if __name__ == '__main__':
    G = SchedulingProblem("Task2.txt")

    G0, G1, G2, G3 = G.calc_es()
    update_early_properties(G0, 'end')
    update_late_properties(G0, 'start')
    print("end fork1")
    update_early_properties(G1, 'end')
    update_late_properties(G1, 'start')
    print("end fork2")
    update_early_properties(G2, 'end')
    update_late_properties(G2, 'start')
    print("end fork3")
    update_early_properties(G3, 'end')
    update_late_properties(G3, 'start')
    print("end fork4")
    print(find_critical_path(G0,'start', 'end'))
    print(find_critical_path(G1, 'start', 'end'))
    print(find_critical_path(G2, 'start', 'end'))
    print(find_critical_path(G3, 'start', 'end'))
    G.drawgraph()
