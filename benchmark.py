
import os

# Environment Variables
data_path = '/gpfs/data/ccvstaff/osu-benchmarks/runHist.h5f5'
batch_script_path = 'gpfs/data/ccvstaff/osu_benchmarks/run_bench'
batches = 5

# function for easy management of dictionaries / autovivification
# from https://en.wikipedia.org/wiki/Autovivification#Python
class Tree(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

# Return minimum value
def min(two_d_dict):
	index1 = -1
	index2 = -1
	val = 1
	for key1 in two_d_dict:
		for key2 in two_d_dict[key1]:
			if (two_d_dict[key1][key2]) < val:
				index1 = key1
				index2 = key2
				val = two_d_dict[key1][key2]
	return (index1, index2)

# Return pair of nodes to run in this iteration
def min_nodes(two_d_dict, idlenode):
	index1 = -1
	index2 = -1
	val = 1

	# node lists are in alphanumerical order
	for i in range(len(idlenode)):
		for j in range(i+1, len(idlenode)):
			# first check if the entry exists or not
			if ((idlenode[i] not in two_d_dict) or (idlenode[j] not in two_d_dict[idlenode[i]])):
				return (idlenode[i], idlenode[j])
			elif (two_d_dict[idlenode[i]][idlenode[j]] < val):
				index1 = idlenode[i]
				index2 = idlenode[j]
				val = two_d_dict[idlenode[i]][idlenode[j]]
	return (index1, index2)

# Divide entries in histArray by two
def div_two(two_d_dict):
	for i in two_d_dict:
		for j in two_d_dict[i]:
			two_d_dict[i][j] /= 2


# Import data file or create an empty histArray
#if (os.path.exists(data_path)):
	# import and parse into histArray
#	for key1 in histArray:
#		for key2 in histArray[key1]:
#			histArray[key1][key2] /= 2
#else:
#	histArray = Tree()
	
#runHist = h5py.File('/gpfs/data/ccvstaff/osu-benchmarks/runHist.h5f5', 'a')

# Get list of idle nodes
idleList = os.popen("sinfo --Node | grep batch | grep idle | awk '{print $1}' | sed -z 's/\s/,/g' | sed -z 's/.$//'").read().split(',')

# Choose which node to benchmark in this iteration
for i in range(batches):
	(benchNode1, benchNode2) = min_nodes(histArray, idleList)
	if (benchNode1 == -1 or benchNode2 == -1):
		continue # something more sensible?
	else:
		x_line = "sbatch --nodelist=" + benchNode1 + "," + benchNode2 + batch_script_path
		os.popen(x_line)
		if (benchNode1 not in histArray) or (benchNode2 not in histArray[benchNode1]):
			histArray[benchNode1][benchNode2] = 1
		else:
			histArray[benchNode1][benchNode2] += 1
	div_two(histArray)

# TODO: save two dimensional dictionary histArray into h5py for later use


