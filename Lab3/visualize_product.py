import graphviz
import collections
import json


def prepareForDrawing(states, end_state, prev_start):
    # make the last state as out state
    states["S"+str(end_state)]["terminalState"] = True
    # sort the state ascending
    states = collections.OrderedDict(sorted(states.items()))
    # loop over sorted states and save them as the given example to json file
    # return the json file content to be displayed in graph format
    states.update({"startingState": ("S" + str(prev_start))})
    with open('out/nfa.json', 'w') as fp:
        json.dump(states, fp, ensure_ascii=True)
    print(states)
    return states

def visualize_automaton():
    graph = graphviz.Digraph(comment='Moore Visualization')
    graph.graph_attr['rankdir'] = 'LR'
    graph.node('start', label='start', shape='plaintext')
    nodes = list()
    # loop over each NFA state
    for state in nfa_copy:
        # check whether state is created or not
        if not state in nodes:
            # add state to created nodes
            nodes.append(state)
            # construct a graph node for the state
            construct_node(state, nfa_copy, starting_state, graph)
        # loop over each successor state
        for successor in nfa_copy[state]:
            # skip 'terminalstate' key
            if successor != 'terminalState':
                # check whether successor state is created or not
                if nfa_copy[state][successor] in nodes:
                    # create an edge between two states
                    graph.edge(state, nfa_copy[state][successor], label=successor)
                else:
                    # add state to created nodes
                    nodes.append(nfa_copy[state][successor])
                    # construct a graph node for the state
                    construct_node(nfa_copy[state][successor], nfa_copy, starting_state, graph)
                    # create an edge between two states
                    graph.edge(state, nfa_copy[state][successor], label=successor)
    # set output format to SVG
    graph.format = 'svg'
    # render final graph
    graph.render('out/nfa-graph', view=False)


def render(filename):
    for aut in inp_automatons:
        visualize_automaton()
        graphviz.render(aut.get_name() + '.pdf', aut)
    visualize_automaton()
    graphviz.render(filename + '.pdf', get_res())
