import random
import json
import flask
from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS
import game

app = flask.Flask(__name__)
CORS(app)

@app.route('/scores', methods=['GET'])
def score():
     return {
         "scores" : game.scores()
     }

@app.route('/winning', methods=['GET'])
def winning():
     return jsonify(game.winning())

app.run(use_reloader=True, host='127.0.0.1', port=3000)