import random
import json
import flask
from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS
import testi

import data


artefacts = list()
# nykyinen manner
cont = "EU"
# kaikki mantereet
conts = []
# airport
airport = "Helsinki Vantaa Airport"
country = "Finland"
size = ""
money = 1000
time = 365
achieved = ["Digger", "Builder"]
total_distance = 50000
visited_countries = ["Finland, Sweden, Norway, Denmark"]
actions_left = 1
reason = "no_time"


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
    global money, time, artefacts, actions_left

    if action == "get":
        actions_left -= 1
        response = testi.get_event()
        response['money'] = money
        response['time'] = time
        response["artefacts"] = len(artefacts)
        response["actions"] = actions_left

        return response

    if action == "result":
        # menetetyt ja maksettavat artefaktit
        removables = list()

        costs = testi.eventit[number]['choices'][choice]['cost']
        money -= costs['money']
        time -= costs['time']
        response = testi.get_event_result(number, choice)
        # pelaajan maksama artefakti HINTA
        if costs['artefacts'] > 0:
            removables.extend(testi.remove_artefacts(artefacts, cont, costs['artefacts']))

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
            newarts = testi.add_artefacts(artefacts, cont, response["artefact_count"])
            artefacts.extend(newarts)

        # jos negatiivinen arvo niin poistetaan se määrä ja passitetaan tieto eteenpäin
        elif response["artefact_count"] < 0:
            # ainoastaan poista artefakti jos SELLAINEN ON
            if len(artefacts) > 0:
                removables.extend(testi.remove_artefacts(artefacts, cont, abs(response["artefact_count"])))

        # poistetaan kulutetut artefaktit listasta
        for art in artefacts:
            if art in removables:
                artefacts.remove(art)


        # heitetään vaan koko lista js puolelle
        response["all_artefacts"] = json.dumps([art.__dict__ for art in artefacts])

        # debug
        print(response)
        return response



@app.route('/fight/<action>/<int:enemy>', methods=['GET', 'POST'])
def fight(action, enemy):
    global fight, enemy_amount, actions_left
    if action == "start":
        actions_left -= 1
        enemy_amount = random.randint(2, 4)
        fight = testi.start_fight(enemy_amount)
        fight["actions"] = actions_left
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
    fight["actions"] = actions_left
    return fight

@app.route('/airport/<action>/<atarget>/<ctarget>', methods=['GET', 'POST'])
def get_airport(action, atarget, ctarget):
    global airport, country, actions_left
    if action == "get":
        response = {}
        actions_left -= 1
        response["airports"] = testi.get_airport(airport)
        response["actions"] = actions_left
        response["money"] = money
        response["time"] = time
        response["all_artefacts"] = json.dumps([art.__dict__ for art in artefacts])

        return response
    elif action == "depart":
        airport = atarget
        country = ctarget
        actions_left = 3
        return {
            "airport": airport,
            "country": country,
            "actions": actions_left,
            "money": money,
            "time": time,
            "all_artefacts": json.dumps([art.__dict__ for art in artefacts])
        }

@app.route('/work')
def work():
    global money, time, actions_left

    response = testi.work()
    money += response['money']
    time -= response['time']
    actions_left -= 1
    response["actions"] = actions_left
    response["time"] = time
    response["money"] = money
    response["all_artefacts"] = json.dumps([art.__dict__ for art in artefacts])

    return response

@app.route('/win_screen', methods=['GET'])
def win_screen():
    global money, time, total_distance, achieved

    return testi.winning(money, time, total_distance, achieved, visited_countries)

@app.route('/lose_screen', methods=['GET'])
def lose_screen():
    global money, time, total_distance, artefacts, airport, country, cont, visited_countries, reason

    return {
        "money": money,
        "time": time,
        "total_distance": total_distance,
        "artefacts": artefacts,
        "airport": airport,
        "country": country,
        "cont": cont,
        "visited_countries": visited_countries,
        "reason": reason
    }

app.run(use_reloader=True, host='127.0.0.1', port=3000)
