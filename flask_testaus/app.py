import flask
from flask import Flask, render_template, request, session
from flask_cors import CORS
import testi

money = 0

app = flask.Flask(__name__)
CORS(app)
@app.route('/event/<nr>', methods=['GET', 'POST'])
def event(nr):
    global money
    teksti = testi.events(int(nr))

    money += 10

    answer = {
        "text" : teksti,
        "money" : money
    }
    return answer

app.run(use_reloader=True, host='127.0.0.1', port=3000)
