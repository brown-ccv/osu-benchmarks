
import os, csv, dotenv, subprocess

# Environment Variables
# These come from environment.env file in the work directory.
cwd = os.getcwd()
dotenv.load_dotenv(cwd+'/environment.env')
sinfo = os.getenv('SINFO') # Path to sinfo command
sbatch = os.getenv('SBATCH') # Path to sbatch command
data_dir = os.getenv('OSU_DATA') # Path to data directory
inst_dir = os.getenv('INST_DIR') # Path to installation
module_name = os.getenv('MODULE_NAME') # Name of the module registered on the system
batches = int(os.getenv('N_CRON'))
max_attempt = int(os.getenv('N_ATTEMPTS'))
max_q = int(os.getenv('MAX_Q'))

# Derive necessary variables directly from the environment variables
data_path = data_dir + module_name + '/runHist.csv'
inst_path = inst_dir + module_name + '/osu-benchmarks'
batch_script_path = [inst_path + '/run_osu_latency', inst_path + 'run_osu_bibw']
cur_q = int(subprocess.run(["myq | wc -l"], shell=True, stdout=subprocess.PIPE))

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

# Multiply entries in histArray by 99999/100000
# (99999/100000)^(700^2/2) = 0.0863
# elements in histArray less likely to be rounded off to zero
def mul_nines(two_d_dict):
	for i in two_d_dict:
		for j in two_d_dict[i]:
			two_d_dict[i][j] = two_d_dict[i][j]*99999/100000

# Modify data file
def update_data(data_path, two_d_dict):
	with open(data_path, 'w', newline="") as f:
		csvwriter = csv.writer(f, delimiter=',')
		for i in two_d_dict:
			for j in two_d_dict[i]:
				csvwriter.writerow([i, j, two_d_dict[i][j]])

# Abort run if cur_q > max_q
if (cur_q > max_q):
	sys.exit(0)

# Import data file or create an empty histArray
histArray = Tree()
if (os.path.exists(data_path)):
	# import and parse into histArray
	with open(data_path, 'r', newline="") as f:
		csvreader = csv.reader(f, delimiter=',')
		for row in csvreader:
			histArray[row[0]][row[1]]=float(row[2])
	
# Get list of idle nodes
proc = subprocess.run([sinfo + " --Node | grep batch | grep idle | awk '{print $1}' | sed -z 's/\s/,/g' | sed -z 's/.$//'"], shell=True, stdout=subprocess.PIPE)
idleList = proc.stdout.decode().split(',')

# Choose which node to benchmark in this iteration
nSubmit = 0
nTried = 0

while (nSubmit < batches and nTried < max_attempt):
	(benchNode1, benchNode2) = min_nodes(histArray, idleList)
	if (benchNode1 == -1 or benchNode2 == -1):
		continue
	else:
		slurmError = False
		for j in batch_script_path: # for all osu-benchmark scripts that need to be executed (i.e. bibw, latency)
			x_line = sbatch + " --nodelist=" + benchNode1 + "," + benchNode2 + " " + j
			print(x_line) #DEBUG Line for cmd
			proc = subprocess.run([x_line], shell=True, stderr=subprocess.PIPE)
			if (proc.stderr != b''):
				print(proc.stderr)
				slurmError = True
		if (benchNode1 not in histArray) or (benchNode2 not in histArray[benchNode1]):
			histArray[benchNode1][benchNode2] = 1
		else:
			histArray[benchNode1][benchNode2] += 1
		if (not slurmError):
			nSubmit += 1
	nTried += 1
	mul_nines(histArray)

update_data(data_path, histArray)

