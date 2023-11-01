import collections
import json
import re
import random
import os
import ast
from natsort import natsorted


def CreateState(regex, index, next_state, start_state, prev_state, prev_start, states):
    if regex[index] == "*":
        # create two state and connect between them using tompthon rule as decribed in the slides
        next_state += 1
        states["S"+str(start_state)].update({"   ε  ": "S" +
                                             str(prev_state), "ε    ": "S"+str(next_state)})
        states["S"+str(prev_state)].update({"ε     ": "S"+str(next_state-1)})
        states.update({"S"+str(next_state): {"terminalState": False}})
        start_state = next_state
    else:
        next_state += 1
        states["S"+str(start_state)
               ].update({"Transition "+regex[index]: "S"+str(next_state)})
        states.update({"S"+str(next_state): {"terminalState": False}})
        prev_state = start_state
        start_state = next_state
    return next_state, start_state, prev_state, prev_start


def prepareForDrawing(states, next_state, prev_start):
    # make the last state as out state
    states["S"+str(next_state)]["terminalState"] = True
    # sort the state ascending
    states = collections.OrderedDict(sorted(states.items()))
    # loop over sorted states and save them as the given example to json file
    # return the json file content to be displayed in graph format
    states.update({"startingState": ("S" + str(prev_start))})
    with open('out/nfa.json', 'w') as fp:
        json.dump(states, fp, ensure_ascii=True)
    fp.close()
    print(states)
    return states


def isEdge(state1, state2, inp_automatons):
    result = True
    symbol = null
    for s in state1.get_parts():
        idx = state1.get_idx(s)
        if symbol is null:
            symbol = inp_automatons[idx].get_label(s, state2.get_parts()[idx])
        if not inp_automatons[idx].has_edge(s, state2.get_parts()[idx], symbol):
            result = False
    return result

def setStates(inp_automatons):
    states = []
    for aut in inp_automatons:
	states.append(aut.get_states())
    return permutations(states)

def input_automaton():
    inp_automatons = []
    a = input('Continue?')
    while a != "N":
        n = input("Set name")
        s = input("Set states")
        f = input("Set transitions")
        inp_automatons.append(create_automaton(n, s, f))
    return inp_automatons

def createFormalDescription():
    with open('out/nfa.json', 'r') as fp:
        states = json.load(fp)
    fp.close()
    print("*******************CREATE FORMAL DESCRIPTION************")
    print(states)
    # Initializating the Formal description object
    formalDescription = {
        "setOfStates": [""],
        "setOfSymbols": [""],
        "transitions": {},
        "startState": "",
        "setOfFinalStates": {""}
    }
    # Adding the start state to the formal description
    finalStates = set()
    # Taking a shallow copy of the original dictionary
    modifiedStates = states.copy()
    # Adding value of startState to the formalDescription
    formalDescription['startState'] = modifiedStates['startingState']
    # Removing startingState from the modifiedStates in order to loop
    # On the States
    del modifiedStates['startingState']
    # Re-initializing the setOfStates list to be
    # An empty set in order to add the states to it
    formalDescription['setOfStates'] = set()

    # Re-initializing the setOfSymbols to be an empty set
    # In order to add all the symbols used to it
    formalDescription['setOfSymbols'] = set()

    # Looping over modifiedStates items which contains
    # The states
    for state, stateDict in modifiedStates.items():
        # Adding each state to the setOfStates
        formalDescription['setOfStates'].add(state)
        # Looping over each state to find its
        # terminalState and add it to the
        # finalStates if it was True
        for key, value in stateDict.items():
            if key == 'terminalState':
                if value == True:
                    finalStates.add(state)
            # Looping over transitions to add it
            # to the setOfSymbols
            if key.startswith('Transition'):
                # Splitting the transition by the splitter space
                # which will be ['Transition','a'] for example
                # So we will always pick the second element to add
                # it to the setOfSymbols
                transition = key.split(' ')
                formalDescription["setOfSymbols"].add(transition[1])

    # Sorting and adding the finalStates to setOfFinalStates in formalDescription
    formalDescription["setOfStates"] = natsorted(
        formalDescription["setOfStates"])
    formalDescription["setOfFinalStates"] = finalStates

    # Loop again in order to add the transitions
    # to the formalDescription
    setOfTransitions = {}
    for state, stateDict in modifiedStates.items():
        for key, value in stateDict.items():
            if key.startswith('Transition') or key.startswith('ε'):
                setOfTransitions.update({state: {key: value}})

    # Sort the list of transitions ascendingly
    # Then adding it to the formalDescription
    setOfTransitions = collections.OrderedDict(
        sorted(setOfTransitions.items()))
    formalDescription["transitions"] = setOfTransitions
    return formalDescription

def asynchronous_product(automata):
    res = create_automaton('result', [], [])
    setStates(res)
    for pos_edge in res.get_all_edge_permuts():
        if isEdge(pos_edge[0], pos_edge[1], inp_automatons):
            res.add_edge(pos_edge[0], pos_edge[1], get_label(pos_edge[0], pos_edge[1], inp_automatons))
    shrinkStates(res)
    return res
