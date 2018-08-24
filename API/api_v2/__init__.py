from flask import Flask, request,jsonify,Blueprint
import psycopg2

app = Flask(__name__)
app.config ['SECRET_KEY'] = 'mish'

from users.views import users
#from questions.views import questions
from views import main

app.register_blueprint(users)
#app.register_blueprint(questions)
app.register_blueprint(main)