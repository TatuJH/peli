import random
import json
import flask
from flask import Flask, render_template, request, session, jsonify
from flask_cors import CORS
import testi
from geopy import distance
from achievement_list import achievements
import event_list

artefacts = list()
cont = "AN"
conts = []
airport = "Ancient Chamber"
country = "Antarctica"
size = ""
money = 1000
time = 365
achieved = []
total_distance = 0
visited_countries = []
actions_left = 3
reason = "no_time"
money_earned = 0
artefacts_earned = 0
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
current_airport_list = {}
co2 = 0

# Tämä on merkkijono joka näytetään sellaisenaan ruudun yläosassa
# Jos artefakteja on kaksi samalta mantereelta, merkitään 1/6 +1
artefact_display = "0/6"

app = flask.Flask(__name__)
CORS(app)

#Adds game state to the JSON response (all requests return game_state and info)
def add_game_state(dict):
    response = {}
    thing = testi.artefact_displayer(artefacts)
    response["info"] = dict,
    response["game_state"] = {
        "actions" : actions_left,
        "money" : int(money),
        "time" : time,
        "total_distance" : total_distance,
        "all_artefacts" : json.dumps([art.__dict__ for art in artefacts]),
        "artefacts" : len(artefacts),
        "visited_countries" : visited_countries,
        "achieved" : achieved,
        "current_airport" : airport,
        "current_country" : country,
        "current_continent" : cont,
        "distance" : total_distance,
        "artefact_display" : thing,
        "co2" : co2
    }

    return response

@app.route('/scores', methods=['GET'])
def score():

     scores = testi.scores()

     return {
         "scores" : scores
     }

@app.route("/shop/<action>/<int:index>", methods=["GET", "POST"])
# shop init
def shop(action, index):
    global money, money_earned, actions_left, cont, artefacts_earned

    # kauppaan ilmestyy artefaktit
    if action == "get":
        # annetaan pelille nykyiset artefaktit sekä manner jotta kauppaan ei tuu duplikaatteja tai ulkomaisia aarteita
        actions_left += 1
        arts = testi.shop_init(artefacts, cont)

        return add_game_state(json.dumps([art.__dict__ for art in arts]))


    # Pelaaja ostaa artefaktin indeksillä index
    if action == "buy":
        # hankitaan haluttu artefakti kauppalistasta
        art = testi.shop_buy(index)
        if money < art.value:
            DIC = {
                "text": f"Sinun rahat eivät riitä tähän !!",
                "success" : False
            }
        else:
            money -= art.value

            # annetaan se pelaajlle :-)
            artefacts.append(art)
            DIC = {
                    "text" : f"Ostettu {art.name} hintaan ${art.value}!!",
                    "success" : True
                }
            artefacts_earned += 1

        return add_game_state(DIC)


    # pelaaja myy artefaktin indeksillä index
    if action == "sell":
        for arrrr in artefacts:
            print (arrrr.name)

        #TODO TÄRKEÄ: ETSI KEINO, JOLLA LISTA EI PÄIVITY HETI KUN PELAAJA POISTAA ARTEFAKTIN
        #TODO           PELAAJAN REPPU MUUTTUU VASTA KUN LÄHTEE VETÄÄN KAUPASTA!!
        #TODO           NAPIT JS PUOLELLA ON KERTAKÄYTTÖISIÄ
        #TODO           MUUTA SE AARREKOUNTTERI SAMALLA!!!!!
        art = artefacts[int(index)]
        artefacts.pop(index)

        # pakko olla parempi tapa tehdä tämä
        money_earned += art.value
        money += art.value
        DIC = {
                "text" : f"Myyty {art.name} hintaan {art.value}!!",
               }

        return add_game_state(DIC)



@app.route('/events/<action>/<int:number>/<choice>', methods=['GET', 'POST'])
def event(action, number, choice):
    global money, time, artefacts, actions_left, money_earned, artefacts_earned, events_completed

    if action == "get":
        actions_left -= 1
        time -= 5
        events_completed += 1

        return add_game_state(testi.get_event(money_modifier))

    if action == "result":
        # menetetyt ja maksettavat artefaktit
        removables = list()

        costs = event_list.getallevents(money_modifier)[number]['choices'][choice]['cost']
        money -= costs['money']
        time -= costs['time']
        response = testi.get_event_result(number, choice, money_modifier)
        # pelaajan maksama artefakti HINTA
        if costs['artefacts'] > 0:
            removables.extend(testi.remove_artefacts(artefacts, cont, costs['artefacts']))

        money += response['money']
        money_earned += response['money']
        time += response['time']

        if money < 0:
            money = 0
        if time < 0:
            time = 0

        if response["artefact_count"] > 0:
            # extend lisää pelkästään annetun listan jäsenet eikä itse listaa
            newarts = testi.add_artefacts(artefacts, cont, response["artefact_count"])
            artefacts.extend(newarts)
            artefacts_earned += response['artefact_count']

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
    global fight, enemy_amount, actions_left, money, time, money_modifier, money_earned
    if action == "start":
        actions_left -= 1
        time -= 5
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
        money_earned += 100 * enemy_amount * money_modifier
        money += enemy_amount * 100 * money_modifier

    if fight["player_hp"] <= 0:
        time -= 10

    return add_game_state(fight)

@app.route('/airport/<action>/<atarget>/<ctarget>/<size>/<int:cost>/<continent>/<int:index>', methods=['GET', 'POST'])
def airports(action, atarget, ctarget, size, cost, continent, index):
    global airport, country, actions_left, money_modifier, money, time, cont, total_distance, current_airport_list, visited_countries, co2
    visited_countries.append(ctarget)

    if action == "get":
        current_airport_list = testi.get_airport(airport)
        return add_game_state(current_airport_list)
    elif action == "depart":
        latlong = (current_airport_list[index]["latitude"], current_airport_list[index]["longitude"])
        current_latlong = (current_airport_list[0]["latitude"], current_airport_list[0]["longitude"])
        total_distance += int(distance.distance(latlong, current_latlong).km)
        co2 += int(distance.distance(latlong, current_latlong).km) // 5
        actions_left -= 1
        airport = atarget
        country = ctarget
        cont = continent
        actions_left = 3
        if size == "large_airport":
            money_modifier = 1.5
        elif size == "small_airport":
            money_modifier = 1
        elif size == "medium_airport":
            money_modifier = 1.2
        money -= cost
        time -= 10

        return add_game_state({})

@app.route('/work')
def work():
    global money, time, actions_left, money_modifier, money_earned

    response = testi.work(money_modifier)
    money += response['money'] * money_modifier
    money_earned += response['money']
    time -= response['time']
    actions_left -= 1
    time -= 5

    return add_game_state(response)

@app.route("/ach", methods=["GET"])
def ach():
    global visited_countries, money_earned, total_distance, artefacts_earned, events_completed
    global countries_index, money_index, artefacts_index, events_index, distance_index, money, achieved
    global converted_amount, convert_index

    new_achievements = testi.achievement(visited_countries, money_earned, total_distance, artefacts_earned, events_completed, countries_index, money_index, artefacts_index, events_index, distance_index, money, achieved, converted_amount, convert_index)

    achievements_info = []
    for achievementti in new_achievements:
        category = achievementti["category"]
        name = achievementti["name"]

        reward = achievementti.get("reward", 0)
        if reward > 0:
            money += reward
            money_earned += reward
        else:
            money += reward
            if money < 0:
                money = 0


        description = ""
        for item in achievements[category]:
            if item[1] == name:
                description = item[2]
                break

        achievements_info.append({
            "name": name,
            "description": description,
            "category": category,
            "reward": reward
        })

    print(money_earned)
    print(money)
    print(total_distance)

    print(achievements_info)

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

@app.route('/reset', methods=['POST'])
def reset_game():
    global actions_left, money, time, total_distance, artefacts, countries_index, money_index
    global visited_countries, achieved, airport, country, cont, distance_index, co2
    global conts, size, money_earned, artefacts_earned, events_completed, converted_amount
    global artefacts_index, events_index, convert_index, enemy_amount, fight, money_modifier

    artefacts = list()
    cont = "AN"
    # tarviiko tätä resetoida?
    conts = []
    airport = "Ancient Chamber"
    country = "Antarctica"
    size = ""
    money = 1000
    time = 365
    achieved = []
    total_distance = 0
    visited_countries = []
    actions_left = 3
    money_earned = 0
    artefacts_earned = 0
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
    co2 = 0

    return add_game_state({"success": True})

app.run(use_reloader=True, host='127.0.0.1', port=3000)
