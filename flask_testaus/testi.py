import mysql.connector
import random
import data
from geopy import distance
from achievement_list import achievements
import event_list

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame',
    user='tatu',
    password='Tietokannat1',
    autocommit=True
)

cursor = conn.cursor()

class Artefact:
    def __init__(self, nimi, arvo, manner):
        self.name = nimi
        self.value = arvo
        self.continent = manner

uncompleted_events = []
# kauppa säilyttää myynnissä olevat aarteet tässä
shop_cache = list()

def start():
    for eve in event_list.getallevents(0):
        uncompleted_events.append(eve)

def scores():
    cursor.execute("SELECT id, score FROM scores;")
    scores = cursor.fetchall()

    if scores:
        return {score[0]: score[1] for score in scores}
    else:
        return {}

# tää returnaa nyt listan uusista artefakteista
# parametreina nykyiset artefaktit, nykyinen manner ja annettava määrä
def add_artefacts(artefacts, cont, count = 1):
    #global artefacts_earned
    #artefacts_earned += count

    # Hanki kaikki mahd. aarteiden nimet mantereen perusteella
    tup = list(data.artefact_names[cont])

    # Sekoita artefaktien lista jotta pelaaja ei saa jokaisella pelikerralla samoja aarteita ekana
    random.shuffle(tup)

    # Luo erikseen lista pelaajan omistamista aarteiden nimistä
    # -> artefacts listaa olioita eikä sanoja joten ei voida verrata sillä
    names = list()
    for nm in artefacts:
        names.append(nm.name)

    new_artefacts = list()

    # Montako artefaktia lisätään?
    for c in range(0,count):
        # Satunnainen rahamäärä
        val = random.randint(600, 1000)

        # Montako mahdollista nimeä on?
        for i in range(0,len(tup)):
            nimi = tup[i]

            # Pelaaja ei voi saada duplikaatteja artifakteista
            if nimi not in names:
                new_artefacts.append(Artefact(nimi, val, cont))
                names.append(nimi)
                # Poistu loopista jos löydettiin käyttämätön nimi
                break
            else:
                if i == len(tup)-1:
                    # Mikäli pelaajalla on jo JOKAINEN aarre mantereelta, valitse satunnaisesti duplikaatti
                    nimi = tup[random.randint(0,len(tup)-1)]
                    new_artefacts.append(Artefact(nimi, val, cont))
                    names.append(nimi)

    return new_artefacts

# tälle annetaan artefaktilista sekä nykyinen manner sekä annettu indeksi (jos myydään artefakti, -1 meinaa ei myydä)
def remove_artefacts(artefacts, cont, count = 1, index = -1):
    # Poista tältä mantereelta kotoisin artefakti ekana
    priority = list()
    removables = list()

    for a in artefacts:
        if a.continent == cont:
            priority.append(a)
    # Tee randomilla jos ei anneta indeksiä (eli jos jokin event ottaa pelaajalta)
    if index == -1:
        for a in range(0,count):
            if len(priority) > 0:
                removables.append(artefacts[random.randint(0, len(priority)-1)])
            else:
                removables.append(artefacts[random.randint(0, len(artefacts)-1)])
    else:
        removables.append(artefacts[index])

    # palautetaan artefakti, joka poistetaan
    return removables

def get_event(modifier):
    global uncompleted_events
    # testausta varten laitetaan lista täyteen taas jos se on tyhjä
    if len(uncompleted_events) == 0:
        for eve in event_list.getallevents(modifier):
            uncompleted_events.append(eve)
    numero = random.choice(uncompleted_events)
    uncompleted_events.remove(numero)

    # TESTI EVENT
    # numero = 14
    choices = []
    mcosts = []
    tcosts = []
    acosts = []

    for choice in event_list.getallevents(modifier)[numero]["choices"]:
        choices.append(choice)
        mcosts.append(event_list.getallevents(modifier)[numero]["choices"][choice]['cost']['money'] * modifier)
        tcosts.append(event_list.getallevents(modifier)[numero]["choices"][choice]['cost']['time'])
        acosts.append(event_list.getallevents(modifier)[numero]["choices"][choice]['cost']['artefacts'])

    return {
        "number": numero,
        "text": event_list.getallevents(modifier)[numero]["event"],
        "question": event_list.getallevents(modifier)[numero]["input"],
        "choices": choices,
        "money_costs": mcosts,
        "time_costs": tcosts,
        "artefacts_costs": acosts
    }


def work(modifier):
    max_money = int(round(200 * modifier))
    min_money = int(round(100 * modifier))
    jobs = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher","cucumber quality inspector", "tree doctor", "farmer's assistant","professional supermarket greeter"]
    moneygain = random.randint(min_money, max_money)

    return {
        "text":f"You decide to work as a {random.choice(jobs)}. You earn <span class='moneytext'>${moneygain}</span>, but lose <span class='timetext'>10 days</span>.",
        "money":moneygain,
        "time":15
    }

def get_event_result(numero, choice, modifier):
    result = random.randint(1, len(event_list.getallevents(modifier)[numero]["choices"][choice]["results"]))

    return {
        "text" : event_list.getallevents(modifier)[numero]["choices"][choice]["results"][result]["text"],
        "money" : event_list.getallevents(modifier)[numero]["choices"][choice]["results"][result]["money"] * modifier,
        "time" : event_list.getallevents(modifier)[numero]["choices"][choice]["results"][result]["time"],
        "artefact_count" : event_list.getallevents(modifier)[numero]["choices"][choice]["results"][result]["artefacts"]
    }


# Katsotaan pelaajan aarteet ja palautetaan muodossa (uniikit artefaktit)/6 +(duplikaatit)
def artefact_displayer(arts):

    # ->0<-/6 +1
    unique_artefacts = 0
    # 0/6 ->+1<-
    duplicate_artefacts = 0

    continent_tally_array_deluxe = []

    for art in arts:
        if art.continent not in continent_tally_array_deluxe:
            unique_artefacts += 1
            # lisätään aarteen manner mannerlistaan
            continent_tally_array_deluxe.append(art.continent)
        else:
            duplicate_artefacts += 1
    if duplicate_artefacts > 0:
        return f"Artefacts: {unique_artefacts}/6 +{duplicate_artefacts}"
    else:
        return f"Artefacts: {unique_artefacts}/6"



# poista listoilta ja palauta ostettu artefakti
def shop_buy(index):
    art = shop_cache[index]
    shop_cache.remove(art)
    return art


def shop_init(arts, cont):
    # Tehdään listä johon laitetaan kaupan esineet
    items = list()
    # otetaan välimuistista veks aiemman kaupan esineet
    shop_cache.clear()

    # kaikki annetun mantereen aarteiden nimet
    possible_names = list(data.artefact_names[cont])
    # Sekoita artefaktien lista jotta pelaaja ei saa jokaisella pelikerralla samoja aarteita ekana
    random.shuffle(possible_names)

    # Löydettyjen artefaktien lista!!
    names = list()



    # pelaajan artefaktit lisätään listaan
    for nm in arts:
        names.append(nm.name)



    # Montako artefaktia kaupassa
    # maksimi on neljä!!
    for i in range(0, random.randint(2,4)):

        # tulevan aarteen arvo
        val = random.randint(600, 1000)
        # kaupan vero
        val += 350

        # Käydään läpi kaikki mahd. nimet
        for n in range(0, len(possible_names) - 1):
            nimi = possible_names[n]

            # Mikäli pelaajan repussa sekä kaupassa ei vielä ole tätä aarretta, laitetaan se kauppaan
            if nimi not in names:
                # lisää kaupan esineisiin aarre nimellä nimi
                items.append(Artefact(nimi, val, cont))
                # lisää löydettyjen aarteiden listaan nimi
                names.append(nimi)
                break

            else:
                # ainoastaan loopin viimeinen toisto
                if n == len(possible_names) - 1:
                    # Heitä kauppaan satunnainen duplikaatti mikäli pelaajalla on 11 aarretta samalta mantereelta
                    nimi = possible_names[random.randint(0, len(possible_names))]
                    items.append(Artefact(nimi, val, cont))
                    break

    # koko paskan lopuksi palautetaan aarreobjektit
    shop_cache.extend(items)
    return items

def start_fight(amount):
    player_hp = 10 + 5 * amount
    player_heals = 0 + amount // 2

    # hp, dmg, dodge, speed
    types = {
        "Bulwark": [16, 7, 1, 3],
        "Warden": [10, 4, 2.5, 2],
        "Vessel": [7, 2, 4, 0],
        "Zealot": [12, 3, 3, 1]
    }

    enemies_in_fight = {}
    for i in range(amount):
        enemy = random.choice(list(types.keys()))
        stats = types[enemy]

        enemies_in_fight[i] = {
            "type": enemy,
            "hp": stats[0],
            "dmg": stats[1],
            "ddg": stats[2],
            "spd": stats[3],
            "d_spd": stats[3]
        }

    return {
        "text": f"You find a group of {amount} robed men. You prepare to convert them, no matter the cost.",
        "player_hp": player_hp,
        "player_heals": player_heals,
        "enemies_in_fight": enemies_in_fight,
        "amount": amount,
        "guarding": False
    }

def get_airport(current_airport):
    global cursor
    airport_list = []
    data = []
    desc = []
    sql = f'SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE airport.name="{current_airport}" AND country.iso_country = airport.iso_country'
    cursor.execute(sql)
    data.append(cursor.fetchmany(3))

    if current_airport != "Ancient Chamber":
        sql = f'SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE airport.continent="AN" AND country.iso_country = airport.iso_country'
        cursor.execute(sql)
        data.append(cursor.fetchmany(3))

    for cont in ['NA', 'EU', 'AS', 'SA', 'OC', 'AF']:
        sql = f'(SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE type="small_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country AND airport.name NOT LIKE "%/%" ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE type="large_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country AND airport.name NOT LIKE "%/%" ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE type="medium_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country AND airport.name NOT LIKE "%/%" ORDER BY RAND() LIMIT 1)'
        cursor.execute(sql)
        data.append(cursor.fetchmany(3))

    for i in range(len(cursor.description)):
        desc.append(cursor.description[i][0])

    for group in data:
        for row in group:
            airport = {}
            for i in range(len(desc)):
                airport[desc[i]] = row[i]
            airport_list.append(airport)

    for airport in airport_list:
        if airport["continent"] == "EU":
            airport["alt_cont"] = "Europe"
        elif airport["continent"] == "AS":
            airport["alt_cont"] = "Asia"
        elif airport["continent"] == "SA":
            airport["alt_cont"] = "South America"
        elif airport["continent"] == "OC":
            airport["alt_cont"] = "Oceania"
        elif airport["continent"] == "AF":
            airport["alt_cont"] = "Africa"
        elif airport["continent"] == "NA":
            airport["alt_cont"] = "North America"
        elif airport["continent"] == "AN":
            airport["alt_cont"] = "Antarctica"
        if airport["type"] == "small_airport":
            airport["cost"] = 150
        elif airport["type"] == "medium_airport":
            airport["cost"] = 300
        elif airport["type"] == "large_airport":
            airport["cost"] = 450
        latlong = (airport["latitude"], airport["longitude"])
        current_latlong = (airport_list[0]["latitude"], airport_list[0]["longitude"])
        airport["distance"] = int(distance.distance(latlong, current_latlong).km)
        airport["co2"] = int(airport["distance"] // 5)

    return airport_list

def achievement(visited_countries, money_earned, total_distance, artefacts_earned, events_completed, countries_index, money_index, artefacts_index, events_index, distance_index, money, achieved, converted_amount, convert_index):

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

def winning(money, time, total_distance, achieved, visited_countries):
    global cursor

    score = money + total_distance // 60 + time * 10

    #lisää score databaseen, testauksen aikana ei käytössä
    #cursor = conn.cursor()
    #cursor.execute("INSERT INTO scores (score) VALUES (%s)", (score,))
    #conn.commit()

    return {
        "achievements": achieved,
        "visited_countries": visited_countries,
        "total_distance": total_distance,
        "money": money,
        "time": time,
        "score": score,
        "money_score": money,
        "time_score": time * 10,
        "distance_score": total_distance // 60
    }

