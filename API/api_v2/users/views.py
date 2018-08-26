from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api, Resource
from functools import wraps
import psycopg2
import re
import hashlib
import jwt
import datetime

from flask_restful import Api, Resource
from __init__ import *
from models import *

users = Blueprint('users', __name__)
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


def tokens(k):
    @wraps(k)
    def decorators(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'})
        return k(*args, **kwargs)
    return decorators

def pwhash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_pwhash(password, hash):
    if pwhash(password)==hash:
        return True
    
    return False

#this class allows a user to create an account by signing up
class Register(Resource):
	def post(self):
		name = request.get_json()['name'].strip()
		username = request.get_json()['username'].strip()
		emailaddress = request.get_json()['emailaddress'].strip()
		password = request.get_json()['password'].strip()
		repeatpassword = request.get_json()['repeatpassword'].strip()
		phash=pwhash(password)

		if not name:
			return {"message":"you must provide a name"}
		if not username:
			return {"message":"you must provide a username"}
		if len(username) < 5 or len(username) > 22:
			return {"message":"username must be between 5 and 22 characters"}

		if not password:
			return{"message":"you must provide a password"}
			
		if password != repeatpassword:
			return {"message":"password do not match"}

		if len(password) < 9 or len(password) > 20:
			return {"message":"password must be between 9 and 20 characters"}

		if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
			return {"message":"password must contain a capital letter and a number"}

		if not emailaddress:
			return {"message":"you must provide an email"}

		if not re.match("[^@]+@[^@]+\.[^@]+", emailaddress):
			return {"message":"email address not valid"}
		try:
			with connection.cursor() as cursor:
				sql="INSERT INTO users(name,emailaddress,password,username) VALUES\
				('"+name+"','"+emailaddress+"','"+str(phash)+"','"+username+"');"
				cursor.execute("SELECT * FROM  users WHERE username='"+username+"';");
				if cursor.fetchone() is not None:
					return{"message":"username taken"}, 409
				cursor.execute("SELECT * FROM  users WHERE emailaddress='"+emailaddress+"';");
				if cursor.fetchone() is not None:
					return {"message":"emailaddress exists"}
				else:
					cursor.execute(sql)
		except:
			return {"message":"unable to register!"}, 500
		connection.commit()
		return {"name":name, "emailaddress":emailaddress, "username":username}
		
api.add_resource(Register,'/api/v1/auth/signup')

#this class allows a user with an account to login
class Login(Resource):
	def post(self):
		username=request.get_json()['username'].strip()
		password= request.get_json()['password'].strip()
		
		if not username:
			return {"message":"please enter a username"}
		if not password:
			return {"message":"please enter a password"}
		with connection.cursor() as cursor:
			sql_log="SELECT * FROM  users WHERE username = '"+username+"'"
			cursor.execute(sql_log)
			result=cursor.fetchone()
			if result is None :

				return {"message":"your username is wrong"}
			else:
			
				if check_pwhash(password, result[4]):
					token=jwt.encode({'username':username,'user_id':result[0],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
					return {"message":"succesfuly logged in",'token':token.decode ('UTF-8')}
				else:
					return {'message':'invalid password'}
					
		connection.commit()
		return {"message":"check your login details"}
api.add_resource(Login, '/api/v1/auth/login')



		