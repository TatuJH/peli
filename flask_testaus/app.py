import random

import flask
from flask import Flask, render_template, request, session
from flask_cors import CORS
import testi

money = 0

app = flask.Flask(__name__)
CORS(app)

@app.route('/intro_text', methods=['GET', 'POST'])
def introduction():

    teksti = testi.intro_text()

    answer = {
        "text" : teksti,
        "money" : 0
    }

    print(answer)

    return answer


@app.route('/scores', methods=['GET', 'POST'])
def score():

    teksti = ""

    scores = testi.scores()

    for i in range(len(scores)):
        teksti = teksti + f', {scores[i + 1]}'

    answer = {
        "text" : teksti,
        "money" : 0
    }

    return answer

@app.route('/event/<nr>', methods=['GET', 'POST'])
def event(nr):
    global money
    nr = int(nr)
    if nr == 0:
        nr = random.randint(1, len(testi.eventit))



    teksti = testi.events(nr)
    money += 10

    answer = {
        "text" : teksti,
        "money" : money
    }
    return answer

app.run(use_reloader=True, host='127.0.0.1', port=3000)
