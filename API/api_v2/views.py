from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api, Resource
from __init__ import*

main = Blueprint('main', __name__)

class Home(Resource):
	def get(self):
		return jsonify({"message":"welcome, you can post or answer a question"})
api.add_resource(Home,'/api/v1/')