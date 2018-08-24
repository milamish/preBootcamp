from flask import *
import unittest
import json

import os,sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import *

class Test_Users(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.questions={'name':'mish'}
		table()

		'''def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Borabora for vacation'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()'''


	def test_Home(self):
		self.assertEqual(app.test_client().get('/api/v1/',).status_code,200)

	def test_login(self):
		m=app.test_client()
		response=(m.get('/api/v1/auth/login',).status_code, 500)
		sign_data=json.dumps({})

	def test_signedup(self):
		sign_data=json.dumps({"username":"mish", "password":"Milamish"})
		header={"content-type":"application/json"}
		signedin=app.test_client().post('/api/v1/auth/login',data=sign_data, headers=header)
		response=signedin

	def test_signup(self):
		response=(app.test_client().get('/api/v1/auth/signUp',).status_code,500)
		respone2=(app.test_client().get('/api/v1/auth/signUp',).status_code,409)

	def tearDown(self):
		"""teardown all initialized variables."""
		with self.app.test_client():
		# drop all tables
			db.session.remove()
			db.drop_all()




if __name__ =='__main__':
    unittest.main()
