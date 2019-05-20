import sys
from model import Layout

# FIXME: Refactor this program so that the code is reentrant (i.e., thread safe).
# Currently `PenaltyAssignment` is modified globally.
PenaltyAssignment = []

def resolveIndividualLayoutParameters(layout:Layout):
	layout.Xsum = 0
	layout.Ysum = 0
	layout.Wsum = 0
	layout.Hsum = 0
	layout.AreaSum = 0
	for element in layout.elements:
		element.area = element.width * element.height
		layout.Xsum = layout.Xsum + element.X
		layout.Ysum = layout.Ysum + element.Y
		layout.Wsum = layout.Wsum + element.width
		layout.Hsum = layout.Hsum + element.height
		layout.AreaSum = layout.AreaSum + element.area


def buildLayoutParameters(firstLayout:Layout, secondLayout:Layout):
	resolveIndividualLayoutParameters(firstLayout)
	resolveIndividualLayoutParameters(secondLayout)

	for firstElement in firstLayout.elements:
		firstElement.PenaltyIfSkipped = firstElement.area/firstLayout.AreaSum

	for secondElement in secondLayout.elements:
		secondElement.PenaltyIfSkipped = secondElement.area/secondLayout.AreaSum

	for firstElement in firstLayout.elements:
		localPenalty = []
		for secondElement in secondLayout.elements:
			deltaX = abs(firstElement.X - secondElement.X)
			deltaY = abs(firstElement.Y - secondElement.Y)
			deltaW = abs(firstElement.width - secondElement.width)
			deltaH = abs(firstElement.height - secondElement.height)

			try:
				PenaltyToMove = ((deltaX / (firstLayout.Xsum + secondLayout.Xsum)) + (deltaY / (firstLayout.Ysum + secondLayout.Ysum))) * ((firstElement.area + secondElement.area) / (firstLayout.AreaSum + secondLayout.AreaSum))
				PenaltyToResize = ((deltaW / (firstLayout.Wsum + secondLayout.Wsum)) + (deltaH / (firstLayout.Hsum + secondLayout.Hsum))) * ((firstElement.area + secondElement.area) / (firstLayout.AreaSum + secondLayout.AreaSum))
			except:
				PenaltyToMove = 0
				PenaltyToResize = 0

			localPenalty.append(PenaltyToMove + PenaltyToResize)
		PenaltyAssignment.append(localPenalty)


def prepare(firstLayout:Layout, secondLayout:Layout):
	global PenaltyAssignment
	if len(PenaltyAssignment) > 0:
		PenaltyAssignment = []
	buildLayoutParameters(firstLayout, secondLayout)
	print(PenaltyAssignment, file=sys.stderr)
	return PenaltyAssignment
