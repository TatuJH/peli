import random

import flask
from flask import Flask, render_template, request, session
from flask_cors import CORS
import testi

money = 0
time = 0

app = flask.Flask(__name__)
CORS(app)

@app.route('/intro_text', methods=['GET', 'POST'])
def introduction():

    teksti = testi.intro_text()

    

    answer = {
        "text" : teksti,
        "money" : 0
    }


    return answer


@app.route('/scores', methods=['GET'])
def score():

    scores = testi.scores()

    answer = {
        "scores" : scores
    }

    return answer

# @app.route('/event/<nr>', methods=['GET', 'POST'])
# def event(nr):
#     global money
#     nr = int(nr)
#     if nr == 0:
#         nr = random.randint(1, len(testi.eventit))
#
#
#
#     teksti = testi.events(nr)
#     money += 10
#
#     answer = {
#         "text" : teksti,
#         "money" : money
#     }
#     return answer

@app.route('/getevent', methods=['GET', 'POST'])
def getevent():
    global money
    global time
    nr = random.randint(1, len(testi.eventit))

    response = testi.get_event(nr)

    return response

@app.route('/eventresult/<number>/<choice>', methods=['GET', 'POST'])
def eventresult(number, choice):
    global money
    global time
    nr = int(number)

    response = testi.get_event_result(nr, choice)

    return response

app.run(use_reloader=True, host='127.0.0.1', port=3000)
