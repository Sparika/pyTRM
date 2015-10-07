# TRUSTMODEL DATA STRUCTURE 
#
#
#
#

# Dictionnaries
agents = {}
types = {}
tags = set()
# Agent
# Agent operating in the trust model.
# They are linked together by relations.
class Agent:
	def __init__(self, name):
		if name in agents: raise Exception("Agent already declared")
		self.name = name
		self.relations = []
		
def declaredAgent(name):
	if name in agents: return True	
	else: return False

def declareAgent(name):
	agent = Agent(name)
	agents[name] = agent

def getAgent(name):
	return agents[name]

# Type
# Types caracterize trust relations.
# Types may have dependencies between them. 
class Type:
	def __init__(self, name):
		if name in types: raise Exception("Type already declared")
		self.name = name
		self.dependsOf = []

def declaredType(name):
	if name in types: return True
	else: return False

def declareType(name):
	typeT = Type(name)
	types[name] = typeT

def getType(name):
	return types[name]

def defTag(name):
	tags.add(name)

# Relation
# Trust relation between two agent
class Relation:
	def __init__(self, truster, trustee, typeT, expr, tags, rec):
		self.truster = truster
		self.trustee = trustee
		self.typeT = typeT
		self.expr = expr
		self.tags = tags
		self.isRecommended = rec
