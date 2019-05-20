import sys 
from gurobipy import Model
from gurobipy import GRB
from tools.GurobiUtils import define2DBoolVarArrayArray
from tools.GurobiUtils import define1DBoolVarArray
from model import Layout
from gurobipy import disposeDefaultEnv
from gurobipy import LinExpr

# FIXME: Refactor this program so that the code is reentrant (i.e., thread safe).
gurobiModel = None
objective = None
#gurobiModel = Model("GLayoutCompare")
#objective = LinExpr()

def solve(firstLayout:Layout, secondLayout:Layout) -> float:
	# THIS is critical to get deterministic results, since the model and the objective are modified globally.
	# Therefore, we have to reinstantiate the model everytime.
	global gurobiModel, objective
	gurobiModel = Model("GLayoutCompare")
	objective = LinExpr()

	setControlParameters()

	Z, UF, US = defineVariables(firstLayout, secondLayout)
	defineObjectives(firstLayout, secondLayout, Z, UF, US)
	defineConstraints(firstLayout, secondLayout,Z, UF, US)
	
	gurobiModel.optimize()

	if gurobiModel.Status == GRB.Status.OPTIMAL:
		val = objective.getValue()*10000
		print("Solved yielding", val, file=sys.stderr)
		return val
	else:
		print("Solver failed", file=sys.stderr)
		return -1

def setControlParameters():
	gurobiModel.Params.OutputFlag = 0
#	gurobiModel.Params.Method = 4
#	disposeDefaultEnv()
#	gurobiModel.reset(1)

def defineConstraints(firstLayout:Layout, secondLayout:Layout,Z, UF, US):
		#Forward -- First to second
		for countInFirst in range(firstLayout.N):
			assignmentOfThisElement = LinExpr()
			assignmentOfThisElement.addTerms([1],[UF[countInFirst]])
			for countInSecond in range(secondLayout.N):
				assignmentOfThisElement.addTerms([1],[Z[countInFirst,countInSecond]])
			gurobiModel.addConstr(assignmentOfThisElement == 1, "AssignFirstForElement("+str(countInFirst)+")")

		#Reverse -- Second to first
		for countInSecond in range(secondLayout.N):
			assignmentOfThisElement = LinExpr()
			assignmentOfThisElement.addTerms([1],[US[countInSecond]])
			for countInFirst in range(firstLayout.N):
				assignmentOfThisElement.addTerms(1,Z[countInFirst,countInSecond])
			gurobiModel.addConstr(assignmentOfThisElement == 1, "AssignSecondForElement("+str(countInSecond)+")")

def defineObjectives(firstLayout:Layout, secondLayout:Layout,Z, UF, US):
		# THIS is critical to get deterministic results, since `PenaltyAssignment` is a global variable.
		from solver.PrepareParameters import PenaltyAssignment
		#Element Assignment
		for countInFirst in range(firstLayout.N):
			for countInSecond in range(secondLayout.N):
				weightage = PenaltyAssignment[countInFirst][countInSecond]
				variable = Z[countInFirst,countInSecond]
				objective.addTerms(weightage, variable)

		#UnAssigned from first
		for countInFirst in range(firstLayout.N):
			objective.addTerms(firstLayout.elements[countInFirst].PenaltyIfSkipped,UF[countInFirst])
			
		for countInSecond in range(secondLayout.N):
			objective.addTerms(secondLayout.elements[countInSecond].PenaltyIfSkipped,US[countInSecond])
		
		gurobiModel.setObjective(objective, GRB.MINIMIZE)


def defineVariables(firstLayout:Layout, secondLayout:Layout):
	Z = define2DBoolVarArrayArray(gurobiModel, firstLayout.N, secondLayout.N, "ZAssignment")
	UF = define1DBoolVarArray(gurobiModel, firstLayout.N, "UnassignedInFirstLayout")
	US = define1DBoolVarArray(gurobiModel, secondLayout.N, "UnassignedInSecondLayout")
	return Z, UF, US
