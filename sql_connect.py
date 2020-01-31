# Module contains sql-related functions

# Dependencies
import sqlalchemy
import pandas as pd
import dotenv, os

class SQLConnection:
	def __init__(self):
		if os.path.exists('config.env'):
			# load dotenv
			dotenv.load_dotenv('config.env')
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
		readline = os.popen("tail -n 1 " + self.__osu_data).read()[:-2].split(',')
		parsed = pd.DataFrame({'slurm_id' : [readline[2]], 'node1_id' : [readline[3][0:8]], 'node2_id' : [readline[5][0:8]], 'node1_arch' : [readline[4][0:10]], 'node2_arch' : [readline[6][0:10]], 'bench_type' : [readline[9][0:8]], 'result' : [readline[10]]})
		self.add_dataframe(parsed)

# Main body starts here
sql = SQLConnection()
sql.add_osu_data()



