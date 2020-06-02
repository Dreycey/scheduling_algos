#! usr/bin/python3
import sys
import numpy as np

"""
This script presents the algorithm for going from a .csv file with seperated
nodes to a gantt.
"""

def csv2dict(csv_file_path):
    """
    This function takes in the file path for the csv-delimited file representing
    the nodes in the protocol. It sorts this information and creates a
    dictionary with the information for each node and edge organized.

    INPUT: 
        a csv file with: <ParentNodeName>,<DaughterNodeName>,<time (in seconds)>
        example: node_A,node_B,500

    OUTPUT:
        if the DAG is:                    A -> B
        a dictionary like:
            output_dict = {node_A : {'parentnode' : {}, 
                                     'daughter_node' : {'node_B' : 500}
                                    }
                           node_B : {'parentnode' : {'node_A' : 500},
                                     'daughter_node' : {}
                                    }
                          }
    """
    output_dict = {}
    # add file contents to the dicitonary
    csv_file = open(csv_file_path).readlines()
    for csv_line in csv_file:
        parent_node, daughter_node, time = csv_line.strip('\n').split(',')
        
        if parent_node not in output_dict:
            output_dict[parent_node] = {'parent_node' : {},
                                        'daughter_node' : {}
                                       }
        if daughter_node  not in output_dict:
            output_dict[daughter_node] = {'parent_node' : {},
                                          'daughter_node' : {}
                                         }
        output_dict[parent_node]['daughter_node'][daughter_node] = time
        output_dict[daughter_node]['parent_node'][parent_node] = time
    return output_dict

def calc_criticality(node, graph, path_list, criticality):
    """
    This function calculates criticality.
    """
    daughter_nodes = graph[node]['daughter_node']
    if len(daughter_nodes) == 0:
        # can be used to find all paths: print(f"HIT {path_list} {criticality}")
        return criticality
    else:
        d_node_array, d_node_crit = [], []
        for node_to, time_val in daughter_nodes.items():
            criticality_new = criticality + float(time_val)
            current_path_list = path_list + [node_to]
            crit_dnode = calc_criticality(node_to,
                                          graph,
                                          current_path_list,
                                          criticality_new)
            d_node_array.append(node_to)
            d_node_crit.append(crit_dnode)
        chosen_criticailty = max(d_node_crit)
        d_node_index = d_node_crit.index(chosen_criticailty)
        chosen_daughter_node = d_node_array[d_node_index]

        return chosen_criticailty
            

def dict2stack(graph_dict):
    """
    This function takes in the graph represented as a dictionary and returns the
    operations ordered based on the critical path (termed critcal_index here)
 
    INPUT:
              graph_dict = {node_A : {'parentnode' : {},                         
                                      'daughter_node' : {'node_B' : 500}         
                                     }                                           
                            node_B : {'parentnode' : {'node_A' : 500},           
                                      'daughter_node' : {}                       
                                     }                                           
                           }                                                     
    OUTPUT:
        An array equal to the number of nodes in the graph:
        [['node_A',500], 
         ['node_B',0]]
    """
    node_array = []
    for node in graph_dict.keys():
        criticality = calc_criticality(node, graph_dict, [], 0)
        row_array = [node, float(criticality)]
        node_array.append(row_array)
    node_array = np.array(node_array, dtype=object)
    return node_array[node_array[:,1].argsort()][::-1]
 

# running the script
def main():
    graph_dict = csv2dict(sys.argv[1])
    sorted_stack = dict2stack(graph_dict)
    print(sorted_stack)

if __name__ == '__main__':
    main()
