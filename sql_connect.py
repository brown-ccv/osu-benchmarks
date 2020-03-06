# Module contains sql-related functions

# Dependencies
import sqlalchemy
import pandas as pd
import dotenv, os
import sys
from datetime import datetime

jobc = sys.argv[1] # Read or Write
if jobc == 'w':
	jobid = sys.argv[2] # Gets jobid
	benchtype = sys.argv[3] # Gets benchmark type

elif jobc == 'r':
	import seaborn as sns # for heatmap generation
	sns.set() # init seaborn
	from matplotlib import pyplot as plt
	from matplotlib import cm

class SQLConnection:
	def __init__(self):
		if os.path.exists('/users/mcho4/osu-benchmarks/config.env'):
			# load dotenv
			dotenv.load_dotenv('/users/mcho4/osu-benchmarks/config.env')
			self.__username = os.getenv('USER')
			self.__password = os.getenv('PASSWORD')
			self.__host = os.getenv('HOST')
			self.__db = os.getenv('DATABASE')
			self.__osu_data= os.getenv('OSU_DATA')
			self.__table = os.getenv('TABLE')
			self.connect_sql()
		else:
			print('config.env does not exist.')
	
	def connect_sql(self):
		url = sqlalchemy.engine.url.URL('mysql+mysqlconnector', username=self.__username, password=self.__password, host=self.__host, database=self.__db, query={'auth_plugin': 'mysql_clear_password'})
		engine = sqlalchemy.create_engine(url)
		self.con = engine.connect()

	def add_dataframe(self, df):
		df.to_sql(self.__table, con=self.con, index=False, if_exists='append')

	def add_osu_data(self):
		readline = os.popen("cat " + self.__osu_data + " | grep " + jobid + " | grep " + benchtype).read()[:-2].split(',')
		parsed = pd.DataFrame({'slurm_id' : [readline[2]], 'node1_id' : [readline[3][0:8]], 'node2_id' : [readline[5][0:8]], 'node1_arch' : [readline[4][0:10]], 'node2_arch' : [readline[6][0:10]], 'bench_type' : [readline[9][0:8]], 'result' : [readline[10]]})
		self.add_dataframe(parsed)
	
	def get_data(self, benchtype):
		return pd.read_sql("select node1_id, node2_id, result from " + self.__table + " where bench_type = '" + benchtype + "';", self.con, index_col = ['node1_id', 'node2_id'])

# Rename axis
def trans_nodeid(nodeid):
	if len(nodeid) < 8:
		return 'node0' + nodeid[4:]
	else:
		return nodeid

# Main body starts here
sql = SQLConnection()
if jobc == 'w':
	sql.add_osu_data()
elif jobc == 'r':
	now = datetime.now()
	bibwData = sql.get_data('bibw').rename(trans_nodeid).fillna(0)['result'].astype(float).groupby(['node1_id', 'node2_id']).mean().unstack().fillna(0)
	bibwHeat = sns.heatmap(bibwData, xticklabels=True, yticklabels=True, square=True, linewidths=.005, cmap=cm.get_cmap('terrain_r'))
	plt.gcf().set_size_inches(100,75)
	plt.title('Bidirectional Bandwidth (MB/s)', fontsize=72)
	plt.savefig('/gpfs/data/ccvstaff/osu-benchmarks/figs/' + now.strftime("%d%m%Y-%H%M%S") + 'bibw.png')

	plt.cla() # clear axis
	plt.clf()
	plt.close()

	latencyData = sql.get_data('latency').rename(trans_nodeid).fillna(0)['result'].astype(float).groupby(['node1_id', 'node2_id']).mean().unstack().fillna(0)
	latencyHeat = sns.heatmap(latencyData, xticklabels=True, yticklabels=True, square=True, linewidths=.005, cmap=cm.get_cmap('terrain_r'))
	plt.gcf().set_size_inches(100,75)
	plt.title('Latency (microsec)', fontsize=72)
	plt.savefig('/gpfs/data/ccvstaff/osu-benchmarks/figs/' + now.strftime("%d%m%Y-%H%M%S") + 'lat.png')


