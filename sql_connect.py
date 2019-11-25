# Module contains sql-related functions

# Dependencies
import sqlalchemy
import pandas as pd
import dotenv

class SQLConnection:
	def __init__(self):
		if os.path.exists('config.env'):
			# load dotenv
			dotenv.load_dotenv('config.env')
			self.__username = os.getenv('USER')
			self.__password = os.getenv('PASSWORD')
			self.__host = os.getenv('HOST')
			self.__db = os.getenv('DATABASE')
			self.connect_sql()
		else:
			print('config.env does not exist.')
	
	def connect_sql(self):
		url = sqlalchemy.engine.url.URL('mysql+pymysql', username=self.__username, password=self.__password, host=self.__host, database=self.__db, query={'auth_plugin': 'mysql_clear_password'})
		engine = sqlalchemy.create_engine(url)
		self.con = engine.connect()

	def add_dataframe(self, df):
		df.to_sql('snapshots', con=self.con, index=True, if_exists='append')



