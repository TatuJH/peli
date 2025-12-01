import random
import json
import flask
from flask import Flask, render_template, request, session
from flask_cors import CORS
import testi
import data


artefacts = list()
# nykyinen manner
cont = "EU"
# kaikki mantereet
conts = []
# airport
airport = ""
country = ""
size = ""
money = 0
time = 365


app = flask.Flask(__name__)
CORS(app)

# @app.route('/intro_text', methods=['GET', 'POST'])
# def introduction():
#
#     teksti = testi.intro_text()
#
#
#
#     answer = {
#         "text" : teksti,
#         "money" : 0
#     }
#
#
#     return answer
#
#
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



@app.route('/events/<action>/<int:number>/<choice>', methods=['GET', 'POST'])
def getevent(action, number, choice):
    global money
    global time

    if action == "get":
        response = testi.get_event()
        response['money'] = money
        response['time'] = time

        return response

    if action == "result":
        money -= testi.eventit[number]['choices'][choice]['cost']['money']
        time -= testi.eventit[number]['choices'][choice]['cost']['time']

        response = testi.get_event_result(number, choice)

        money += response['money']
        time += response['time']

        if money < 0:
            money = 0
        if time < 0:
            time = 0
        response['money'] = money
        response['time'] = time


        if response["artefact_count"] > 0:
            # extend lisää pelkästään annetun listan jäsenet eikä itse listaa
            newarts = testi.add_artefact(artefacts, cont, response["artefact_count"])
            artefacts.extend(newarts)
            jayson = json.dumps([art.__dict__ for art in newarts])
            response["items"] = jayson

            print(jayson)
        print(response)
        return response



@app.route('/fight/<action>/<int:enemy>', methods=['GET', 'POST'])
def fight(action, enemy):
    global fight, enemy_amount
    if action == "start":
        enemy_amount = random.randint(2, 4)
        fight = testi.start_fight(enemy_amount)
        return fight

    if action == "strike":
        if fight["enemies_in_fight"][enemy]["ddg"] >= random.uniform(0, 10):
            fight['text'] = f'You missed {fight["enemies_in_fight"][enemy]["type"]}.'
        else:
            if random.random() <= 0.3:
                dmg = int(round(random.randint(3,6)*1.5))
                fight['text'] = f'You hit {fight["enemies_in_fight"][enemy]["type"]} critically with {dmg} damage.'
            else:
                dmg = int(round(random.randint(3, 6)))
                fight['text'] = f'You hit {fight["enemies_in_fight"][enemy]["type"]} with {dmg} damage.'

            fight['enemies_in_fight'][enemy]['hp'] = fight['enemies_in_fight'][enemy]['hp'] - dmg
            if fight['enemies_in_fight'][enemy]['hp'] <= 0:
                fight['amount'] = fight['amount'] - 1
                fight['text'] = fight['text'] + f' {fight["enemies_in_fight"][enemy]["type"]} converts.'

    if action == "heal":
        heal_amount = 15 - fight['player_hp']
        if heal_amount < 1:
            heal_amount = 1
        fight['text'] = f"You reach for a red potion and drink from it. You gain {heal_amount} HP."
        fight['player_hp'] = fight['player_hp'] + heal_amount
        fight['player_heals'] = fight['player_heals'] - 1

    if action == "guard":
        fight['text'] = "You enter a meditative state and feel your skin harden."
        fight['guarding'] = True

    if action != "start":
        for i in range(enemy_amount):
            if fight["enemies_in_fight"][i]["spd"] == 0 and fight["enemies_in_fight"][i]["hp"] > 0:
                if fight['guarding']:
                    fight['text'] = fight['text'] + f' {fight["enemies_in_fight"][i]["type"]} attacks you with {fight["enemies_in_fight"][i]["dmg"] // 3} damage.'
                    fight['player_hp'] = fight['player_hp'] - fight["enemies_in_fight"][i]["dmg"] // 3
                    fight["enemies_in_fight"][i]["spd"] = fight["enemies_in_fight"][i]["d_spd"]
                else:
                    fight['text'] = fight['text'] + f' {fight["enemies_in_fight"][i]["type"]} attacks you with {fight["enemies_in_fight"][i]["dmg"]} damage.'
                    fight['player_hp'] = fight['player_hp'] - fight["enemies_in_fight"][i]["dmg"]
                    fight["enemies_in_fight"][i]["spd"] = fight["enemies_in_fight"][i]["d_spd"]
            elif fight["enemies_in_fight"][i]["hp"] > 0:
                fight["enemies_in_fight"][i]["spd"] = fight["enemies_in_fight"][i]["spd"] - 1

    fight['guarding'] = False
    return fight

app.run(use_reloader=True, host='127.0.0.1', port=3000)
