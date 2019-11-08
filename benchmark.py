
import os, csv

# Environment Variables
data_path = '/gpfs/data/ccvstaff/osu-benchmarks/runHist.csv'
batch_script_path = '/users/mcho4/osu-benchmarks/run_osu_latency'
# batch_script_path = '/gpfs/data/ccvstaff/osu_benchmarks/run_osu_latency'
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
			two_d_dict[i][j] = two_d_dict[i][j] / 2

# Modify data file
def update_data(data_path, two_d_dict):
	with open(data_path, 'w', newline="") as f:
		csvwriter = csv.writer(f, delimiter=',')
		for i in two_d_dict:
			for j in two_d_dict[i]:
				csvwriter.writerow([i, j, two_d_dict[i][j]])

# Import data file or create an empty histArray
histArray = Tree()
if (os.path.exists(data_path)):
	# import and parse into histArray
	with open(data_path, 'r', newline="") as f:
		csvreader = csv.reader(f, delimiter=',')
		for row in csvreader:
			histArray[row[0]][row[1]]=float(row[2])
	
# Get list of idle nodes
idleList = os.popen("sinfo --Node | grep batch | grep idle | awk '{print $1}' | sed -z 's/\s/,/g' | sed -z 's/.$//'").read().split(',')

# Choose which node to benchmark in this iteration
for i in range(batches):
	(benchNode1, benchNode2) = min_nodes(histArray, idleList)
	if (benchNode1 == -1 or benchNode2 == -1):
		continue # something more sensible?
	else:
		x_line = "sbatch --nodelist=" + benchNode1 + "," + benchNode2 + batch_script_path
		print(x_line) # debug line
		#os.popen(x_line) # execute benchmark
		if (benchNode1 not in histArray) or (benchNode2 not in histArray[benchNode1]):
			histArray[benchNode1][benchNode2] = 1
		else:
			histArray[benchNode1][benchNode2] += 1
	div_two(histArray)

update_data(data_path, histArray)

