import psycopg2
from users.views import *
from __init__ import *

connection = psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='questions')

def table():
	connection= psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='questions')
	with connection.cursor() as cursor:
		cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY,\
			name VARCHAR(100) NOT NULL,\
			username VARCHAR(100) NOT NULL,\
			emailaddress VARCHAR(50) NOT NULL,\
			password VARCHAR(100) NOT NULL,\
			reg_date timestamp DEFAULT CURRENT_TIMESTAMP);")
		cursor.execute("CREATE TABLE IF NOT EXISTS questions(question_id serial PRIMARY KEY, \
			question VARCHAR(100) NOT NULL, \
			question_date timestamp DEFAULT CURRENT_TIMESTAMP,\
			user_id INT);")
		cursor.execute("CREATE TABLE IF NOT EXISTS answers(answer_id serial PRIMARY KEY, \
			answer VARCHAR(100) NOT NULL, \
			question VARCHAR(100) NOT NULL,\
			question_id INT REFERENCES questions(question_id) ON DELETE CASCADE ,\
			answer_date timestamp DEFAULT CURRENT_TIMESTAMP,\
			user_id INT);")


		connection.commit()


	

		
			
