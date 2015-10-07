# greeting.py
#
# Demonstration of the parsing module, on the prototypical "Hello, World!" example
#
# Copyright 2003, by Paul McGuire
#
from pyparsing import *
from trustmodel import *
from trustgraph import *
import sys

def addTag(tag):
    defTag(tag)

identifier = Word(alphas, alphanums+'_' )
trustType = Combine(Optional('@') + identifier)
trustTag = Combine('#'+identifier)
trustTag.setParseAction(addTag)
agent = identifier('name')
expr = identifier | Word(nums)
private = Literal('private')
private.setParseAction(lambda t: True)

#####################################################################
##        TRUST GRAPH                                              ##
#####################################################################

def declareRelation(relationTokens, truster):
    # Declare trustee if needed
    agentName = relationTokens.trustee
    if not declaredAgent(agentName):
        declareAgent(agentName)
    trustee = getAgent(agentName)
    
    # Declare type if needed
    typeName = relationTokens.typeT
    if not declaredType(typeName):
        declareType(typeName)    
    typeT = getType(typeName)

    # TODO Parse Expr
    
    recommend = not relationTokens.isPrivate

    rel = Relation(truster, trustee, typeT, relationTokens.expr, relationTokens.tags, recommend)
    print truster.name, '->', trustee.name, ':', typeT.name, '=', relationTokens.expr, recommend
    truster.relations.append(rel)

def declareNode(tokens):
    # Declare truster if needed
    trusterName = tokens.node.truster
    if not declaredAgent(trusterName):
        declareAgent(trusterName)
    truster = getAgent(trusterName)
    
    for r in tokens.node.relations:
        declareRelation(r, truster) 

# Relation declaration
# relation := '->' 'private'? agent ':' type tags* '=' expr
# A trust relationship between the truster and a trustee.
relation = Group( Suppress('->') + Optional(private).setResultsName("isPrivate") +
        agent.setResultsName("trustee") + Suppress(':') +
        trustType.setResultsName("typeT") + ZeroOrMore(trustTag).setResultsName("tags") +
        Suppress('=') + expr.setResultsName("expr") )
# Graph Node declaration
# node := agent ':' '{' transition* '}'
# An agent declaration (truster) contains several trust relationships declaration. 
node = Group(agent("truster") + Suppress(':') + 
         ZeroOrMore(relation)("relations"))("node")
node.setParseAction(declareNode)
# Graph declaration
# graph := node*
# A graph declaration contains several node declarations.
graph = ZeroOrMore(node)

#####################################################################
##              TYPE DEPENDENCIES                                  ##
#####################################################################
def declareDependency(tokens):
    for d in dependencies:
        # Declare type if needed
        childTypeName = d.child
        if not declaredType(childTypeName):
            declareType(childTypeName)
        typeC = getType(childTypeName)
        parentTypeName = d.parent
        if not declaredType(parentTypeName):
            declareType(parentTypeName)
        typeP = getType(parentTypeName)
        # Register dependence
        typeC.dependsOf.append(typeP)

# Dependency declaration
# dependency := trustType '->' trustType
# Describes a dependency relations between two trust types of the form A -> B. 
# The meaning is that A trust is supported by B trust. 
dependency = Group(trustType.setResultsName("child") + Suppress('->') + trustType.setResultsName("parent"))
# Dependencies declaration
# dependencies := 'dependency' dependency*
dependencies = Group(Suppress('dependency') + ZeroOrMore(dependency)("dependencies"))

#####################################################################
##              TRUST MODEL                                        ##
#####################################################################
# TrustModel declaration
# TRM := 'trustmodel' + dependencies? + graph
TRM = Suppress('trustmodel') + Optional(dependencies).setResultsName("dependencies") +  graph.setResultsName("graph") + Suppress(stringEnd)
TRM.ignore(cppStyleComment)





 
# input string
model = open(sys.argv[1]).read()

# parse input string
# print "->", TRM.parseString(model)
TRM.parseString(model)

print agents
displayTrustGraph(agents)