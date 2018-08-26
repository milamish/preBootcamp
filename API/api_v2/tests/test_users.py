from flask import *
import unittest
import json
import re

import os,sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import *

class Test_Users(unittest.TestCase):
	def setUp(self):
		'''
		self.app = app.test_client()
		self.questions={'name':'mish'}
		table() '''

		
	def test_Home(self):
		home=json.dumps({"message":"you can post your question"})
		self.assertEqual(app.test_client().get('/api/v1/',).status_code,200)

	def test_login(self):
		m=app.test_client()
		response=(m.post('/api/v1/auth/login',).status_code, 500)
		sign_data=json.dumps({})

	def test_unregistered_user_login(self):
		noneuser=json.dumps({"username":"militree","password":"Milamish8"})
		header={"content-type":"application/json"}
		res=app.test_client().post( '/api/v1/auth/login',data=noneuser, headers=header )
		result = json.loads(res.data.decode())
		self.assertEqual(res.status_code, 200)
		self.assertEqual(result['message'], "your username is wrong")

	def test_signedup(self):
		sign_data=json.dumps({"username":"sharlyne2454", "password":"Milamish8", "emailaddress":"shal5@yahoo.com",
		 "repeatpassword":"Milamish8", "name":"Mildred"})
		header={"content-type":"application/json"}
		signedup=app.test_client().post('/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(signedup.data.decode())
		self.assertEqual(signedup.status_code, 409)
		self.assertEqual(result['message'], "username taken")

	def test_password_match(self):
		password = "Milamish8"
		repeatpassword = "Milamish8"
		sign_data=json.dumps({"password":"Milamish8","repeatpassword":"Milamish8",})
		header={"content-type":"application/json"}
		passwordmatch=app.test_client().post('/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(passwordmatch.data.decode())
		self.assertTrue(password==repeatpassword, True)
		
	def test_password_characters(self):
		password = "Milamish8"
		length = len(password) < 9 or len(password) > 20
		match= re.match('\d.*[A-Z]|[A-Z].*\d',password)
		if len(password) < 9 or len(password) > 20:
			return {"message":"password must be between 9 and 20 characters"}
		if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
			return {"message":"password must contain a capital letter and a number"}

		sign_data=json.dumps({"password":"Milamish9"})
		header={"content-type":"application/json"}
		passwordcharacter=app.test_client().post('/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(passwordcharacter.data.decode())
		self.assertEqual(password==length, length)
		self.assertEqual(password==match, False)

		






	'''def tearDown(self):
		"""teardown all initialized variables."""
		with self.app.test_client():
		# drop all tables
			db.session.remove()
			db.drop_all()'''




if __name__ =='__main__':
    unittest.main()
