
import os

# Environment Variables
data_path = '/gpfs/data/ccvstaff/osu-benchmarks/runHist.h5f5'

# function for easy management of dictionaries / autovivification
# from https://en.wikipedia.org/wiki/Autovivification#Python
class Tree(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

# Import data file or create it
if (os.path.exists(data_path)):
	# import and parse into histArray
	for key1 in histArray:
		for key2 in histArray:
			histArray[key1][key2] /= 2
else:
	histArray = Tree()
	
#runHist = h5py.File('/gpfs/data/ccvstaff/osu-benchmarks/runHist.h5f5', 'a')

# TODO: update histArray method (check if it exists before doing so)
# for example
# nodeOne in histArray and nodeTwo in histArray[nodeOne] uses short circuits

# Get list of nodes in batch partition
# nodeList = os.popen("sinfo --Node | grep batch | awk '{print $1}' | sed -z 's/\s/,/g' | sed -z 's/.$//'").read().split(',')

# Get list of idle nodes
idleList = os.popen("sinfo --Node | grep batch | grep idle | awk '{print $1}' | sed -z 's/\s/,/g' | sed -z 's/.$//'").read().split(','))

# Choose which node to benchmark in this iteration
benchNode = min(histArray.items()) # not correct, need to change

# TODO: save two dimensional dictionary histArray into h5py for later use


