from flask import Flask, Blueprint, jsonify, request
import psycopg2
import datetime

from __init__ import *
from models import *

questions = Blueprint('questions', __name__)

class Questions:
	def __init__(self,question):
		self.question = question

	@questions.route('/api/v1/questions', methods=['POST'])
	def question():
		question= request.get_json()['question'].strip()
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		pdb.set_trace()

		if not question:
			return jsonify({"message":"post a question"})
				
		try:
			with connection.cursor() as cursor:
				sql_query="INSERT INTO questions(question,user_id) VALUES(%s,%s);"
				cursor.execute(sql_query,(question,user_id))
		except:
			return jsonify({"message":"unable to post a qusetion"}), 500
		connection.commit()
		return jsonify({"question":question,"question_id":question_id, "question_date":question_date, "user_id":user_id}), 200

	@questions.route('/api/v1/questions/<int:question_id>', methods=['GET'])
	def get_specific_question():
		try:
			
			with connection.cursor() as cursor:
				sql_view="SELECT * FROM questions WHERE questions.question_id ='"+str(question_id)+"';"
				try:
					cursor.execute(sql_view)
					result=cursor.fetchone()
					if result is None:
						
						return jsonify({"message":"question_id does not exist"}), 404
					else:
						user_id=result[3]
						question=result[1]
						question_date= result[2]
						question_id=result[0]
						return jsonify({"user_id":user_id, "question":question, "question_date":question_date, "question_id":question_id})
				except:
					return jsonify({"message": "unable to fetch question"}), 500
					
			connection.commit()
		finally:
			pass

