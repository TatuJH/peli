import random
import json
import flask
from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS
import new_main

app = flask.Flask(__name__)
CORS(app)

@app.route('/scores', methods=['GET'])
def score():

     scores = new_main.scores()

     answer = {
         "scores" : scores
     }

     return answer

@app.route('/endscreen', methods=['GET'])
def winning():

     winning_stats = new_main.winning()

     answer = jsonify(winning_stats)

     return answer

app.run(use_reloader=True, host='127.0.0.1', port=3000)