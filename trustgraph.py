#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This simple example on how to do animations using graph-tool. Here we do a
# simple simulation of an S->I->R->S epidemic model, where each vertex can be in
# one of the following states: Susceptible (S), infected (I), recovered (R). A
# vertex in the S state becomes infected either spontaneously with a probability
# 'x' or because a neighbour is infected. An infected node becomes recovered
# with probability 'r', and a recovered vertex becomes again susceptible with
# probability 's'.

# DISCLAIMER: The following code is definitely not the most efficient approach
# if you want to simulate this dynamics for very large networks, and/or for very
# long times. The main purpose is simply to highlight the animation capabilities
# of graph-tool.

from graph_tool.all import *
from numpy.random import *
from trustmodel import *
import sys, os, os.path

seed(42)
seed_rng(42)

# We need some Gtk and gobject functions
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

g = Graph()

vertexToAgent = {}
agentToVertex = {}

edgeToRelation = {}
relationToEdge = {}

v_name = g.new_vertex_property("string")
e_typeTName = g.new_edge_property("string")

def displayTrustGraph(agents):
    for i,agent in agents.iteritems():
        vertex = g.add_vertex()
        vertexToAgent[vertex] = agent
        agentToVertex[agent] = vertex
        v_name[vertex] = agent.name
        
    for truster, fVrtx in agentToVertex.iteritems():
        for rel in truster.relations:
            tVrtx = agentToVertex[rel.trustee]
            edge = g.add_edge(fVrtx, tVrtx)
            edgeToRelation[edge] = rel
            relationToEdge[rel] = edge
            e_typeTName[edge] = rel.typeT.name
            
    graph_draw(g, vertex_text=v_name, edge_text=e_typeTName, vertex_font_size=18, output_size=(300, 300), output="trust_graph.png")
        







# We will give the user the ability to stop the program by closing the window.
#win.connect("delete_event", Gtk.main_quit)

# Actually show the window, and start the main loop.
#win.show_all()
#Gtk.main()