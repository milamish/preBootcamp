from flask import *
import unittest
import json
import re

import os,sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import *

class Test_questions(unittest.TestCase):
	def setUp(self):
		''''mish'''
	

	def test_post_question(self):
		question="how is you"
		question_data=json.dumps({"question":"how is you"})
		header={"content-type":"application/json"}
		question_asked=app.test_client().post('/api/v1/question',data=question_data, headers=header)
		result= json.loads(question_asked.data.decode())
		self.assertEqual(question_asked.status_code, 200)
		self.assertEqual(result['message'],"Token is missing")

	def test_get_question(self):
		get_question=json.dumps({"message":""})
		self.assertEqual(app.test_client().get('/api/v1/question/<int:question_id>',).status_code,404)

	def test_answer_question(self):
		answer="how is you"
		question_data=json.dumps({"answer":"how is you"})
		header={"content-type":"application/json"}
		question_answered=app.test_client().post('/api/v1/question/<int:question_id>/answer',data=question_data, headers=header)
		self.assertEqual(question_answered.status_code,404)
		self.assertTrue(answer=="how is you", True )

	def test_question_entry(self):
		question= ""
		if not question:
			return{"message":"post a question"}
		sign_data=json.dumps({"question":"hey you?"})
		header={"content-type":"application/json"}
		postquestion=app.test_client().post('/api/v1/question',data=sign_data, headers=header)
		result= json.loads(postquestion.data.decode())
		self.assertTrue(result ['message'], "post question")
		
	


if __name__ =='__main__':
    unittest.main()