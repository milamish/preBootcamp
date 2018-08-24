from flask import Flask, Blueprint, jsonify, request
import psycopg2
import re
import hashlib
import jwt
import datetime

from __init__ import *
from models import *

users = Blueprint('users', __name__)


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

class Users:
	def __init__(self, name, username, emailadress, password, repeatpassword):
		self.name = name
		self.username = username
		self.emailaddress = emailaddress
		self.password = password
		self.repeatpassword = repeatpassword

	@users.route('/api/v1/auth/signup',methods=['POST'])
	def signup():
		name = request.get_json()['name'].strip()
		username = request.get_json()['username'].strip()
		emailaddress = request.get_json()['emailaddress'].strip()
		password = request.get_json()['password'].strip()
		repeatpassword = request.get_json()['repeatpassword'].strip()
		phash=pwhash(password)

		if not name:
			return jsonify({"message":"you must provide a name"})
		if not username:
			return jsonify({"message":"you must provide a username"})
		if len(username) < 5 or len(username) > 22:
			return jsonify({"message":"username must be between 5 and 22 characters"})

		if not password:
			return jsonify({"message":"you must provide a password"})
			
		if password != repeatpassword:
			return jsonify({"message":"password do not match"})

		if len(password) < 9 or len(password) > 20:
			return jsonify({"message":"password must be between 9 and 20 characters"})

		if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
			return jsonify({"message":"password must contain a capital letter and a number"})

		if not emailaddress:
			return jsonify({"message":"you must provide an email"})

		if not re.match("[^@]+@[^@]+\.[^@]+", emailaddress):
			return jsonify({"message":"email address not valid"})
		try:
			with connection.cursor() as cursor:
				sql="INSERT INTO users(name,emailaddress,password,username) VALUES\
				('"+name+"','"+emailaddress+"','"+str(phash)+"','"+username+"');"
				cursor.execute("SELECT * FROM  users WHERE username='"+username+"';");
				if cursor.fetchone() is not None:
					return jsonify({"message":"username taken"}), 409
				cursor.execute("SELECT * FROM  users WHERE emailaddress='"+emailaddress+"';");
				if cursor.fetchone() is not None:
					return jsonify({"message":"emailaddress exists"})
				else:
					cursor.execute(sql)
		except:
			return jsonify({"message":"unable to register!"}), 500
		connection.commit()
		return jsonify({"name":name, "emailaddress":emailaddress, "username":username})

	@users.route('/api/v1/auth/login',methods=['POST'])
	def login():
		username=request.get_json()['username'].strip()
		password= request.get_json()['password'].strip()
		
		if not username:
			return jsonify({"message":"please enter a username"})
		if not password:
			return jsonify({"message":"please enter a password"})
		with connection.cursor() as cursor:
			sql_log="SELECT * FROM  users WHERE username = '"+username+"'"
			cursor.execute(sql_log)
			result=cursor.fetchone()
			if result is None :
				return jsonify({"message":"your username is wrong"})
			else:
			
				if check_pwhash(password, result[4]):
					token=jwt.encode({'username':username,'user_id':result[0],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
					return jsonify({"message":"succesfuly logged in",'token':token.decode ('UTF-8')})
				else:
					return jsonify({'message':'invalid password'})
		connection.commit()
		return jsonify({"message":"check your login details"})
