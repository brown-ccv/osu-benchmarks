
import os

# function for defaultdict autovivification
# from https://en.wikipedia.org/wiki/Autovivification#Python
class Tree(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

# Imports an array that stores which nodes were run recently
#runHist = h5py.File('/gpfs/data/ccvstaff/osu-benchmarks/runHist.h5f5', 'a')
#preexists = "/histArray" in runHist

# TODO: update histArray method (check if it exists before doing so)
# for example
# nodeOne in histArray and nodeTwo in histArray[nodeOne] uses short circuits

# TODO: add something that is basically like a heat map
histArray = Tree()

# Multiply histArray by 1/2
# This uses the fact that sum(1/2^n, n, 1, inf) = 1
histArray /= 2

# Get list of nodes in batch partition
nodeList = os.popen("sinfo --Node | grep batch | awk '{print $1}' | sed -z 's/\s/,/g' | sed -z 's/.$//'").read().split(',')

# Get list of idle nodes
idleList = os.popen("sinfo --Node | grep batch | grep idle | awk '{print $1}' | sed -z 's/\s/,/g' | sed -z 's/.$//'").read().split(','))


# TODO: save two dimensional dictionary histArray into h5py for later use


