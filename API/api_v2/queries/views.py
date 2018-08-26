from flask import Flask, Blueprint, jsonify, request
from functools import wraps
from flask_restful import Api, Resource
import psycopg2
import jwt
import datetime


from __init__ import *
from models import *

queries = Blueprint('queries', __name__)


def tokens(k):
    @wraps(k)
    def decorators(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message' : 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'})
        return k(*args, **kwargs)
    return decorators
    
#this class allows a logged in user to post a question
class PostQuestion(Resource):
	@tokens
	def post(self):
		question= request.get_json()['question'].strip()
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']

		if not question:
			return{"message":"post a question"}
				
		try:
			with connection.cursor() as cursor:
				sql_query="INSERT INTO questions(question,user_id) VALUES(%s,%s);"
				cursor.execute(sql_query,(question,user_id))
		except:
			return{"message":"unable to post a question"}, 500
		connection.commit()
		return {"question":question,"user_id":user_id}, 200

api.add_resource(PostQuestion, '/api/v1/question')


#this class allows users to get a single question using the question ID
class GetQuestion(Resource):
	@tokens
	def get(self, question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']

		try:
			with connection.cursor() as cursor:
				sql_get= "SELECT * FROM questions WHERE questions.question_id='"+str(question_id)+"';"
				try:
					cursor.execute(sql_get)
					result=cursor.fetchone()
					if result is None:
						return {"message":"question_id does not exist"}, 404
					else:
						user_id=result[3]
						question=result[1]
						question_date= result[2]
						question_id=result[0]
						return jsonify({"user_id":user_id, "question":question, "question_date":question_date, "question_id":question_id})
				except:
					return{"message": "unable to fetch entry"}, 500
			connection.commit()
		finally:
			pass
api.add_resource(GetQuestion, '/api/v1/question/<int:question_id>')

#this class allows a user to post an answer to a question using the question id then retrieving the question
class PostAnswer(Resource):
	@tokens
	def post(self,question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		question=request.get_json()['question']
		answer=request.get_json()['answer']
		if not answer:
			return {"message":"post an answer"}
		try:
			with connection.cursor() as cursor:
				sql_answer= "INSERT INTO answers(answer,question,user_id,question_id) VALUES(%s,%s,%s,%s);"
				cursor.execute(sql_answer,(answer,question,user_id,question_id))
		except:
			return{"message":"unable to post an answer"}, 500
		connection.commit()
		return {"question":question,"answer":answer, "user_id":user_id}, 200
api.add_resource(PostAnswer,'/api/v1/question/<int:question_id>/answer')

#this class allows a user to retrieve all answers to a secific question using the question ID
class Getanswers(Resource):
	@tokens
	def get(self,question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		
		try:
			with connection.cursor() as cursor:
				sql_one="SELECT * FROM answers WHERE question_id ='"+str(question_id)+"';"
				try:
					cursor.execute(sql_one)
					result=cursor.fetchall()
					questions={}
					if len(result)==0:
						return ({"message":"no answers found"})
					else:
						for row in result:
							answer_id=row[0]
							answer=row[1]
							question=row[2]
							answer_date=row[4]
							questions.update({answer_id:{"question":question, "answer":answer, "answer_date":answer_date}})

						return jsonify(questions)
				except:
					return ({"message":"entry not found"}), 500
			connection.commit()
		finally:
			pass
api.add_resource(Getanswers, '/api/v1/questions/<int:question_id>')

#this class allows users to view all asked questions
class AllQuestions(Resource):
	@tokens
	def get(self):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']

		try:
			with connection.cursor() as cursor:
				sql_get_all= "SELECT * FROM questions;"
				try:
					cursor.execute(sql_get_all)
					result=cursor.fetchall()
					questions={}
					if len(result)==0:
						return jsonify({"message":"no questions found"})
					else:
						for row in result:
							question_id=row[0]
							question=row[1]
							question_date=row[2]
							user_id=row[3]
							questions.update({question_id:{"question":question, "user_id":user_id, "question_date":question_date}})

						return jsonify(questions)
				except:
					return jsonify({"message":"not found"}), 500
			connection.commit()
		finally:
			pass
api.add_resource(AllQuestions, '/api/v1/questions')

#this class allows a user to edit their own answers
class Modify(Resource):
	@tokens
	def put (self,question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		answer=request.get_json()['answer'].strip()
		question=request.get_json()['question'].strip()
		
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM answers WHERE answers.question_id='"+str(question_id)+"' and answers.user_id ='"+str(user_id)+"'")
			result=cursor.fetchone()
			if result is not None:
				sql_update="update answers SET answer ='"+answer+"', question ='"+question+"' WHERE question_id ='"+str(question_id)+"';"
				cursor.execute(sql_update)
			else:
				return jsonify({"message":"entry does not exist"})	
		connection.commit()
		return jsonify({"answer":answer, "question":question})
api.add_resource(Modify, '/api/v1/questions/<int:question_id>/answer')

#this class allows authors of questions to delete their own questions
class Remove(Resource):
	def delete(self,question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		
		try:
			with connection.cursor() as cursor:
				sql_del="DELETE FROM questions WHERE questions.question_id= '"+str(question_id)+"' and questions.user_id='"+str((user_id))+"';"
				cursor.execute("SELECT * FROM questions WHERE questions.question_id = '"+str(question_id)+"' and questions.user_id='"+str((user_id))+"'")
				result=cursor.fetchone()
				if result is None:
					return {"message":"question does not exist"}, 404
				else:
					cursor.execute(sql_del)
		except:
			return {"message": "unable to delete question"}, 500
		connection.commit()
		return {"question": "question succesfully deleted"}
api.add_resource(Remove, '/api/v1/question/<int:question_id>')