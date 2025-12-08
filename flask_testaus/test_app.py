import random
import json
import flask
from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS
import testi
from testi import achievements

artefacts = list()
cont = "EU"
conts = []
airport = "Helsinki Vantaa Airport"
country = "Finland"
size = ""
money = 1000
time = 365
achieved = []
total_distance = 50000
visited_countries = []
actions_left = 1
reason = "no_time"
money_earned = 1000000
artefacts_earned = 5
events_completed = 0
converted_amount = 0
countries_index = 0
money_index = 0
distance_index = 0
artefacts_index = 0
events_index = 0
convert_index = 0
enemy_amount = 0
fight = {}
money_modifier = 1

app = flask.Flask(__name__)
CORS(app)

def achievement():
    global visited_countries, money_earned, total_distance, artefacts_earned, events_completed
    global countries_index, money_index, artefacts_index, events_index, distance_index, money, achieved
    global converted_amount, convert_index

    new_achievements = []

    if countries_index < len(achievements["countries"]) and len(visited_countries) >= achievements["countries"][countries_index][0]:
        name = achievements["countries"][countries_index][1]
        reward = achievements["countries"][countries_index][3]
        money += reward
        achieved.append(name)
        countries_index += 1
        new_achievements.append({"category": "countries", "name": name, "reward": reward})

    if money_index < len(achievements["money"]) and money_earned >= achievements["money"][money_index][0]:
        name = achievements["money"][money_index][1]
        reward = achievements["money"][money_index][3]
        money += reward
        achieved.append(name)
        money_index += 1
        new_achievements.append({"category": "money", "name": name, "reward": reward})

    if distance_index < len(achievements["distance"]) and total_distance >= achievements["distance"][distance_index][0]:
        name = achievements["distance"][distance_index][1]
        reward = achievements["distance"][distance_index][3]
        money += reward
        achieved.append(name)
        distance_index += 1
        new_achievements.append({"category": "distance", "name": name, "reward": reward})

    if artefacts_index < len(achievements["artefacts"]) and artefacts_earned >= achievements["artefacts"][artefacts_index][0]:
        name = achievements["artefacts"][artefacts_index][1]
        reward = achievements["artefacts"][artefacts_index][3]
        money += reward
        achieved.append(name)
        artefacts_index += 1
        new_achievements.append({"category": "artefacts", "name": name, "reward": reward})

    if events_index < len(achievements["events"]) and events_completed >= achievements["events"][events_index][0]:
        name = achievements["events"][events_index][1]
        reward = achievements["events"][events_index][3]
        money += reward
        achieved.append(name)
        events_index += 1
        new_achievements.append({"category": "events", "name": name, "reward": reward})

    if convert_index < len(achievements["convert"]) and converted_amount >= achievements["convert"][convert_index][0]:
        name = achievements["convert"][convert_index][1]
        reward = achievements["convert"][convert_index][3]
        money += reward
        achieved.append(name)
        convert_index += 1
        new_achievements.append({"category": "convert", "name": name, "reward": reward})

    return new_achievements

def add_game_state(dict):
    response = {}
    response["info"] = dict,
    response["game_state"] = {
        "actions" : actions_left,
        "money" : money,
        "time" : time,
        "total_distance" : total_distance,
        "all_artefacts" : json.dumps([art.__dict__ for art in artefacts]),
        "artefacts" : len(artefacts),
        "visited_countries" : visited_countries,
        "achieved" : achieved,
        "current_aiport" : airport,
        "current_country" : country,
        "current_continent" : cont
    }

    return response

@app.route('/scores', methods=['GET'])
def score():

     scores = testi.scores()

     return {
         "scores" : scores
     }

@app.route('/events/<action>/<int:number>/<choice>', methods=['GET', 'POST'])
def event(action, number, choice):
    global money, time, artefacts, actions_left

    if action == "get":
        actions_left -= 1

        return add_game_state(testi.get_event(money_modifier))

    if action == "result":
        # menetetyt ja maksettavat artefaktit
        removables = list()

        costs = testi.getallevents(money_modifier)[number]['choices'][choice]['cost']
        money -= costs['money']
        time -= costs['time']
        response = testi.get_event_result(number, choice, money_modifier)
        # pelaajan maksama artefakti HINTA
        if costs['artefacts'] > 0:
            removables.extend(testi.remove_artefacts(artefacts, cont, costs['artefacts']))

        money += response['money']
        time += response['time']

        if money < 0:
            money = 0
        if time < 0:
            time = 0

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

        # debug
        # print(response)
        return add_game_state(testi.get_event_result(number, choice, money_modifier))

@app.route('/fight/<action>/<int:enemy>', methods=['GET', 'POST'])
def fight(action, enemy):
    global fight, enemy_amount, actions_left, money, time, money_modifier
    if action == "start":
        actions_left -= 1
        enemy_amount = random.randint(2, 4)
        fight = testi.start_fight(enemy_amount)

        return add_game_state(fight)

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

    if fight["amount"] <= 0:
        fight["money_get"] = 100 * enemy_amount * money_modifier
        money += enemy_amount * 100 * money_modifier

    if fight["player_hp"] <= 0:
        time -= 10

    return add_game_state(fight)

@app.route('/airport/<action>/<atarget>/<ctarget>/<size>/<int:cost>', methods=['GET', 'POST'])
def airports(action, atarget, ctarget, size, cost):
    global airport, country, actions_left, money_modifier, money, time
    if action == "get":
        return add_game_state(testi.get_airport(airport))
    elif action == "depart":
        actions_left -= 1
        airport = atarget
        country = ctarget
        actions_left = 3
        if size == "large_airport":
            money_modifier = 1.5
        elif size == "small_airport":
            money_modifier = 1
        elif size == "medium_airport":
            money_modifier = 1.2
        money -= cost
        time -= 5
        return add_game_state({})

@app.route('/work')
def work():
    global money, time, actions_left, money_modifier

    response = testi.work(money_modifier)
    money += response['money'] * money_modifier
    time -= response['time']
    actions_left -= 1

    return add_game_state(response)

@app.route("/ach", methods=["GET"])
def ach():
    new_achievements = achievement()

    achievements_info = []
    for achievementti in new_achievements:
        category = achievementti["category"]
        name = achievementti["name"]

        description = ""
        for item in achievements[category]:
            if item[1] == name:
                description = item[2]
                break

        achievements_info.append({
            "name": name,
            "description": description
        })

    return add_game_state(achievements_info)

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
