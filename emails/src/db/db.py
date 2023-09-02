
from contextlib import contextmanager
import os

import sqlite3
from dotenv import load_dotenv
load_dotenv()


class MySQLDatabase():
	DATABASE_URL = os.environ.get('DATABASE_URL')
	assert DATABASE_URL is not None, 'DATABASE_URL is not set in .env file'
	DATABASE_URL: str

	def __init__(self, keep_open=False):
		self.db = None
		self.cursor = None
		self.keep_open = keep_open

		if keep_open: self.open()

	def open(self):
		if self.db is not None and self.cursor is not None: return

		self.db = sqlite3.connect(self.DATABASE_URL)
		self.cursor = self.db.cursor()


	def close(self):
		if self.keep_open: return

		self.force_close()

	def force_close(self):
		try:
			self.db.close()
			self.db = None
			self.cursor = None
		except: pass


	def execute(self, query: str, args=[], commit=False) -> int | list:
		"""Execute query

		Args:
			query (str): Query to execute
			args (list, optional): Arguments of the query. Defaults to [].
			commit (bool, optional): Whether to commit or not. If not commit, return last row id Defaults to True.

		Returns:
			int | list: Last row id if commit or list of rows
		"""
		if self.db is None or self.cursor is None: self.open()

		self.cursor.execute(query, args)
		if commit: 
			self.db.commit()
			res = self.cursor.lastrowid
		else:
			res = self.cursor.fetchall()

		if not(self.keep_open): self.close()
			
		return res
	

	@staticmethod
	@contextmanager
	def get_db(keep_open=False):
		db = MySQLDatabase(keep_open)
		try:
			yield db
		finally:
			db.force_close()
	
