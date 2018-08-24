from flask import Flask, jsonify, request, Blueprint

main = Blueprint('main', __name__)

class Home():
	@main.route('/api/v1/',methods=['POST','GET'])
	def home():
		return jsonify({"message":"welcome, you can post or answer a question"})