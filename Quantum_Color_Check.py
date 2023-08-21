from qat.lang.AQASM import Program, QRoutine, Z, H, X, CNOT
from qat.lang.AQASM.misc import build_gate
import pkg_resources
from qat.lang.AQASM import Program, QRoutine, Z, H, X, CNOT
from qat.lang.AQASM.misc import build_gate
import pkg_resources
import networkx as nx
# we need an adder:
from qat.lang.AQASM.qftarith import add
# from qat.lang.AQASM.classarith import add
import numpy as np
from qat.lang.AQASM import Program
from qat.lang.AQASM.qint import QInt
from qat.qpus import get_default_qpu

class QuantumColorChecker:
    @build_gate("Check_Edge", [int], arity=lambda m:2 * m + 1)
    def check_edge(m):
        rout = QRoutine()
        #color1 equals to the first m wires
        color1 = rout.new_wires(m)
        #color2 equals to the m wires after that
        color2 = rout.new_wires(m)
        #output is equal to the single last wire and is used to store the information of the comparison
        output = rout.new_wires(1)
        with rout.compute():
            for wire1,wire2 in zip(color1, color2):
                CNOT(wire1, wire2)
            for wire in color2:
                X(wire)
        #Multi Controlled NOT gate
        #m for how many control qbits
        #color2 are the control qubits
        #output is the target qubit
        #The X gate is applied to the output qubit only if all color2 qubits are in state |1⟩
        X.ctrl(m)(color2, output)
        rout.uncompute()
        X(output)
        return rout
    
    @build_gate("CHECK_GRAPH", [nx.Graph, int], arity=lambda g, m: g.number_of_nodes() * m)
    def check_graph(graph, m):
        rout = QRoutine()

        # Colors array - m wires for every node we have in our graph
        colors = [rout.new_wires(m) for node in graph.nodes()]

    #     Our counter L - Holds the amount of bits to store the number of edges and initialize with |0⟩
    #     If for a edge the colors are not the same increase  L by one
    #     IF not do nothing

        #For 2 Edges its 2
        #For 3 Edges its 2
        #For 4 Edges its 3
        size_l = graph.number_of_edges().bit_length()
        print(size_l)

        L = rout.new_wires(size_l)
        # a work qubit to store the result of a check_edge
        tmp = rout.new_wires(1)
        # some routines (check_edge and an adder
    #     Create a check routine for checking the nodes of one edge
        check_routine = check_edge(m)
    #     Create an adder that adds the result of a single edge comparison
        adder = add(size_l, 1)
        with rout.compute():
    #         For every combination of nodes on one edge a,b
            for a, b in graph.edges():
                print(a,b)
                # checking the specific edge
                with rout.compute():
    #                 What happens here????
                    check_routine(colors[a], colors[b], tmp)
                # adding the result in our counter
                adder(L, tmp)

                # uncomputing 'tmp'
                rout.uncompute()

        # checking if l = |E|
        E = graph.number_of_edges()
        with rout.compute():
            for i in range(size_l):
                if ((E >> i) & 1) == 0:
                    X(L[i])

        Z.ctrl(size_l - 1)(L)

        # uncomputing the X's
        rout.uncompute()
        # uncomputing L
        rout.uncompute()
        # tmp and L are work qubits and should be flagged to that they can be re-used
        rout.set_ancillae(L, tmp)
        return rout