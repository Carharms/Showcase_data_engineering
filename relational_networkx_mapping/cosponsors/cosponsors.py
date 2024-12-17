'''#! cosponsors.py
"""Create a graph using networkx and determines the relationship
between legislators, the bills they sponsor, and the their
affiliated party"""

__author__ = "Carter Harms"
__copyright__ = "Copyright, 2024"
__license__ = "GPL"
__version__ = "1.1"
__email__ = "harmsc@uchicago.edu"
'''

import networkx as nx
import csv
import os

class NodeData:
    """ Node information for each individual node within a graph """
    
    def __init__(self, kind, indentifier, name, party=None):
        
        # legislaor or bill depending on node
        self.kind = kind
        # identifier given to the obj
        self.identifier = indentifier
        # name of legislator or title of bill
        self.name = name
        # party of legislator, None if kind is bill
        self.party = party


def build_graph() -> nx.Graph:
    """
    Creates a graph using the networkx package

    Args:
    N/A

    Output:
    A graph composed of relevant edges and nodes, each with data related
    to specific csv files   
    """

    # helper function
    def dictionary_from_csv(local_file, key_index, value_indices):
        """
        Takes a csv file and outputs a dictionary

        Args:
        local_file = the name of the csv file
        key_index = the element that acts as the dictionary key
        value_indices = a list of indices associated with the key

        Output:
        A dictionary 
        """

        file_dict = {}
        file_name = os.path.join(os.getcwd(), local_file)

        with open(file_name, 'r', encoding='utf-8') as file_to_unpack:
            reader = csv.reader(file_to_unpack)

            # skip title line
            next(reader)
            for row in reader:
                key = row[key_index]
                # iterate through files with multiple commas in each line
                value = [row[index] for index in value_indices]
                file_dict[key] = value

        return file_dict

    # helper function
    def alternative_dict_from_csv(local_file):
        """
        Takes a csv file and outputs a dictionary

        Args:
        local_file = the name of the csv file
    
        Output:
        A dictionary 
        """
        # empty dictionary for csv info
        dictionary = {}

        with open(local_file, 'r', encoding='utf-8') as file_to_unpack:
            # skip title line
            next(file_to_unpack)
            # iterate through each line to add key, value pairs to the dictionary
            for line in file_to_unpack:
                key, value = line.strip().split(',', 1)
                dictionary[key] = value

        return dictionary

    # helper function
    def add_nodes_to_graph(graph, dictionary, node_info):
        """
        A helper function dedicated to iterating through a dictionary and
        adding nodes to a graph

        Args:
        graph = a networkx Graph
        dictionary = a key, value pairing of elements that should be added to the graph
        node_info = attributes to be added to each node within the graph
    
        Output:
        A series of nodes within the graph that have unique information related to node_data 
        """
        for key, value in dictionary.items():
            node_data = node_info(key, value)
            graph.add_node(node_data.identifier, data=node_data)

    
    def create_node_data(kind, identifier, name, party=None):
        """
        A helper function dedicated to assigning information to a specific node

        Args:
        kind = the assignment of bill or legislator
        identifier = the unique string detailing the specifics of the kind 
        name = the name of either the bill or legislator
        party = the party (if relevant) of the name of the legislator
    
        Output:
        A singular node with attributes 
        """
        created_node = NodeData(kind, identifier, name, party)
        return created_node
    

    # assigning G as the graph to adjust
    G = nx.Graph()
    
    # use helped functions to extract a dictionary of info from csv files
    bill_dictionary = alternative_dict_from_csv("cosponsors/data/bills.csv")
    legislator_dictionary = dictionary_from_csv("cosponsors/data/legislators.csv", 0, [1,2])

    # using helper functions to add nodes to graph based on created node data within a dictionary
    add_nodes_to_graph(G, bill_dictionary, lambda key, value: create_node_data("bill", key, value))
    add_nodes_to_graph(G, legislator_dictionary, lambda identifier, info: create_node_data("legislator", identifier, info[0], info[1]))


    with open("cosponsors/data/sponsorships.csv", 'r', encoding='utf-8') as file_to_unpack:
        # iterate through csv to identify two linked elements in each row
        for row in file_to_unpack:
            bill_identifier, legislator_identifier = row.strip().split(",", 1)
            # create associations in G between two nodes
            if bill_identifier in G and legislator_identifier in G:
                G.add_edge(bill_identifier, legislator_identifier)
    
    return G

    # at this point G should be the finalized graph


# helper functions

def degree_node_comparison(graph, kind, n):
    """
    a helper function dedicated to identifying tuple pairs for each node: identifying
    the node and determining it's degrees

    Args:
    graph = a networkx graph
    kind = the type of node this comparison should apply to
    n = the top number of instances to return data on
    
    Output:
    A sorted list of tuples detailing the top n elements of a specific kind within the graph
    """

    node_degree_list = []
    
    # iterate through the nodes and create a full list of all identified nodes and degrees
    for node, data in graph.nodes(data="data"):
        if data.kind == kind:
            node_degree_list.append((data.name, graph.degree(node)))

    # final sorting of the list to determine top instances
    sorted_list = sorted(node_degree_list, key=lambda x: x[1], reverse=True)[:n]
    return sorted_list

    
def find_top_sponsors(graph, n) -> list[tuple[str, int]]:
    """
        Takes a graph with node information to determine similarities between nodes

        Args:
        graph = the graph to find top associated nodes
        n = an integer determining how many legislator tuples to return
    
        Output:
        A list of tuples detailing the top individuals who sponsored the most bills
        """
    return degree_node_comparison(graph, "legislator", n)


def find_top_bills(graph, n) -> list[tuple[str, int]]:
    """
    Takes a graph with node information to determine similarities between nodes

    Args:
    graph = the graph to find top associated nodes
    n = an integer determining how many bill tuples to return

    Output:
    A list of tuples detailing the bills with the most sponsors
    """

    # return order list of the names of the n bills with most sponsors
    return degree_node_comparison(graph, "bill", n)


def find_most_similar(graph, to_legislator: str) -> str:
    """
    Takes a graph with node information to which 

    Args:
    graph = the graph to find top associated nodes
    to_legislator = the legislator to act as the base node for comparison

    Output:
    A string of the legislator with the most equivalent bills sponsored
    """

    G = graph

    # determine if to_legislator input is valid
    legislator_base_node = False
    # search G for relevant node equivalent to to_legislator
    for node, data in G.nodes(data="data"):
        if data.kind == "legislator" and data.name == to_legislator:
            # once you have found the legistlator_base_node break the loop
            legislator_base_node = node
            break
    
    # set check if to_legislator input is not found
    if legislator_base_node == False:
        raise ValueError
    
    # create an immutable list of all bills the to_legislator has sponsored
    to_legislator_all_bills = frozenset(G.neighbors(legislator_base_node))

    #initialize the search parameters
    most_similar_legislator = None
    most_common_sponsorships = 0 
    
    # iterate through all nodes in G
    for node, data in G.nodes(data="data"):
        # create check to determine all nodes attached to legislator_base_node
        if data.kind == "legislator" and node != legislator_base_node:
            legislator_sponsored_bills = frozenset(G.neighbors(node))
            # determine sponsorships shared between to_legislators bills and the current legislator 
            same_sponsorships = len(to_legislator_all_bills & legislator_sponsored_bills)

            # continually update the most_similar_legislator based on whether or not their same_sponsorships is greater
            if ((most_similar_legislator is None or same_sponsorships > most_common_sponsorships) or \
                (same_sponsorships == most_common_sponsorships and data.name < most_similar_legislator)):
                
                # add details for next iteration of the loop
                most_similar_legislator = data.name
                most_common_sponsorships = same_sponsorships
    
    return most_similar_legislator
