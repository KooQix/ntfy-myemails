
from db.db import MySQLDatabase
import bcrypt

def has_access(user: str, password: str, topic: str) -> bool:
	"""Check if a user has access to a topic"""
	with MySQLDatabase().get_db() as db:

		user = db.execute("SELECT id, user, pass, role FROM user WHERE user=?", (user,))
		
		if user is None or len(user) == 0: return False

		user_id = user[0][0]
		user_name = user[0][1]
		user_pass = user[0][2]
		user_role = user[0][3]

		# Check password
		if not(bcrypt.checkpw(password.encode(), user_pass)): return False

		# role IN ('anonymous', 'admin', 'user')
		if user_role == "admin": return True
		elif user_role == "anonymous": return False

		# Authentication is good, now check if user has access to topic
		res_access = db.execute("SELECT topic, read, write FROM user_access WHERE user_id=?", (user_id,))
		if res_access is None or len(res_access) == 0: return False

		user_has_access_topic = False
		for topic_access in res_access:
			# If user has access to topic, and can write it, return True
			if topic_access[0] == topic and topic_access[2] == 1:
				user_has_access_topic = True
				break

		return user_has_access_topic



