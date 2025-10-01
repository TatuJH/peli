import random
import mysql.connector
from event_list import *
from artefacts import *
from trivia_list import *
from geopy import distance
from achievements import *

money = 5000
time = 365
artefacts = list()
cont = ""
conts = []
airport = ""
country = ""
size = ""
remaining_actions = 0
game_over = False
#Ei mitää hajuu mikä on "completed" vastakohta lol
uncompleted_events = []
for ev in events:
    uncompleted_events.append(ev)
total_distance = 0
visited_countries = []
money_earned = 0
artefacts_earned = 0
events_completed = 0
countries_index = 0
money_index = 0
distance_index = 0
artefacts_index = 0
events_index = 0


conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    # minä itken aina kun tämä muuttuu
    database='demokanta',
    user='tatu',
    password='Tietokannat1',
    autocommit=True
)

sql = f'SELECT latitude_deg AS latitude, longitude_deg AS longitude FROM airport WHERE name="{airport}";'
cursor = conn.cursor()
cursor.execute(sql)
latlong = cursor.fetchall()
cursor.close()

class Artefact:
    def __init__(self, nimi, arvo, manner):
        self.name = nimi
        self.value = arvo
        self.continent = manner

def intro():
    global money
    global time
    global artefacts
    global cont
    global conts
    global airport
    global country
    global size
    global remaining_actions
    global game_over
    global uncompleted_events
    global total_distance
    global latlong
    global visited_countries
    global money_earned
    global artefacts_earned
    global events_completed
    global countries_index
    global money_index
    global artefacts_index
    global distance_index
    global events_index

    money = 100000
    time = 365
    artefacts = list()
    cont = "AN"
    conts = ["AF", "AN", "AS", "EU", "NA", "OC", "SA"]
    airport = "Ancient Chamber"
    country = "Antarctica"
    size = "ritual_site"
    remaining_actions = 3
    game_over = False
    uncompleted_events = []
    for eve in events:
        uncompleted_events.append(eve)
    total_distance = 0
    sql = f'SELECT latitude_deg AS latitude, longitude_deg AS longitude FROM airport WHERE name="{airport}";'
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    if row is None:
        raise RuntimeError(f"No coordinates found for airport {airport!r}")
    latlong = (row[0], row[1])
    visited_countries.append(country)
    money_earned = 0
    artefacts_earned = 0
    events_completed = 0
    countries_index = 0
    money_index = 0
    distance_index = 0
    artefacts_index = 0
    events_index = 0

    temp = ""
    print("This game is color-coded. Every time you're presented with a choice, your typeable actions are marked with \033[35mmagenta\033[0m.")
    while temp != "understood":
        temp = input("\033[35mUnderstood\033[0m?\n> ").strip().lower()
    print("----")
    temp = ""
    print("Reading the introduction is recommended for a first-time playthrough.")
    while temp != "read" and temp != "play":
        temp = input("Would you like to \033[35mread\033[0m the introduction or start \033[35mplay\033[0ming?\n> ").strip().lower()
    print("----")
    if temp == "read":
        print(f"You belong in a cult dead-set on waking up an ancient god.\n"
              "After centuries of hard work, the moment is finally at hand.\n"
              "You arrive in an ancient chamber. The chamber smells of sulfur and debris on the ground seems to move on its own.\n"
              "In the middle of the chamber lies a circle made of lit candles. You step in, and start performing a ritual.\n"
              "You feel the air rising as a fading projection of your god appears in front of you. You hear a deep voice.\n"
              "The voice commands you to bring him six artefacts - one from each of the other continents - to finish the ritual.\n"
              "After you have found and collected an artefact from every other continent, you shall return to Antarctica\n"
              f"You are given \033[34m{int(time)}\033[0m days\033[0m to complete your quest - otherwise the ritual fails.\n"
              "In addition, to ensure your obedience, a spirit is sent after you. You feel like you don't want to make contact with it.\n"
              "You leave the chamber as a waning voice behind you asks you to hurry.\n----")
        print("Important things to note:\n"
              "- You only have a limited number of actions on each airport (3), and if you dont depart as your last action, the spirit will catch you.\n"          
              "- Working gives you money, but costs you time.\n"
              "- Exploring consists of randomized events, which can both cost and reward money, time or artefacts.\n"
              "- In the auction house you can either buy or sell artefacts.\n"
              "- Traveling to another continent costs more.\n"
              "- Airport size determines the cost of travel and affects rewards gained from exploring.\n"    
              "----")

def print_all():
    print(money, time, cont, country, size, airport, artefacts, uncompleted_events, latlong, total_distance, visited_countries)

def add_artefact(count):
    global cont
    global artefacts_earned

    artefacts_earned += count

    # Hanki kaikki mahd. aarteiden nimet mantereen perusteella
    tup = list(artefact_names[cont])

    # Sekoita artefaktien lista jotta pelaaja ei saa jokaisella pelikerralla samoja aarteita ekana
    random.shuffle(tup)

    # Luo erikseen lista pelaajan omistamista aarteiden nimistä
    # -> artefacts listaa olioita eikä sanoja joten ei voida verrata sillä
    names = list()
    for nm in artefacts:
        names.append(nm.name)

    if count is None:
        count = 1
    # Montako artefaktia lisätään?
    for c in range(0,count):
        # Satunnainen rahamäärä
        val = random.randint(600, 1000)

        # Montako mahdollista nimeä on?
        for i in range(0,len(tup)):
            nimi = tup[i]

            # Pelaaja ei voi saada duplikaatteja artifakteista
            if nimi not in names:
                artefacts.append(Artefact(nimi, val, cont))
                names.append(nimi)
                # Poistu loopista jos löydettiin käyttämätön nimi
                break
            else:
                if i == len(tup)-1:
                    # Mikäli pelaajalla on jo JOKAINEN aarre mantereelta, valitse satunnaisesti duplikaatti
                    nimi = tup[random.randint(0,len(tup)-1)]
                    artefacts.append(Artefact(nimi, val, cont))
                    names.append(nimi)

def shop():
    global money
    global remaining_actions
    l = list()
    num = list()
    # onko pelaaja ostanut
    b = False
    # onko pelaaja myynyt (molemmat vaan muuttavat tekstiä hiukan)
    s = False

    # Tee uusi lista jossa on pelkästään artefaktien numerot :p
    items = list()
    tup = list(artefact_names[cont])
    # Sekoita artefaktien lista jotta pelaaja ei saa jokaisella pelikerralla samoja aarteita ekana
    random.shuffle(tup)

    # Tämä tekee listan artefakteja kauppaan.
    names = list()
    for nm in artefacts:
        names.append(nm.name)
    # Montako artefaktia kaupassa
    for i in range(0, random.randint(3, 6)):
        val = random.randint(600, 1000)
        # kaupan vero
        val += 500
        # Montako mahdollista nimeä on?
        for n in range(0, len(tup) - 1):
            nimi = tup[n]

            # Pelaaja ei voi saada duplikaatteja artifakteista
            if nimi not in names:
                items.append(Artefact(nimi, val, cont))
                names.append(nimi)
                # Poistu loopista jos löydettiin käyttämätön nimi
                break
            else:
                if n == len(tup) - 1:
                    # Mikäli pelaajalla on jo JOKAINEN aarre mantereelta, valitse satunnaisesti duplikaatti
                    nimi = tup[random.randint(0, len(tup))]
                    artefacts.append(Artefact(nimi, val, cont))
                    names.append(nimi)

    auctioning = True

    # Looppi, joka toistuu niin kauan kunnes pelaaja lähtee kaupasta
    # Tähän sisältyy while buying ja while selling
    # buying ja selling- looppien loppuun sisältyy kysymys haluaako jatkaa sitä toimintoa tai tehdä jotain muuta
    # koodin lopussa on pelaajan lähtö kaupasta
    while auctioning:
        print("You arrive at the lobby of the auction house.")
        buying = False
        selling = False

        while True:
            inp = input(
                "Would you like to \033[35mbuy\033[0m, \033[35msell\033[0m or\033[35m leave?\033[0m\n> ").strip().lower()
            if inp == "buy":
                buying = True
                break
            if inp == "sell":
                selling = True
                break
            if inp == "leave":
                auctioning = False
                break
        print("----")

        # pelaajan lähtö on koodin lopussa - älä returnaa
        if not auctioning:
            break

        # Pelaaja ostamassa aarteita
        while buying:
            for a in items:
                l.append(str(items.index(a) + 1))
            i = ""
            if len(l) == 0:
                print("You bought out the entire stock!")
                print("----")
                break
            while i not in l:
                print(f"You have\033[32m ${money}\033[0m. The following artefacts are on auction:")
                for art in items:
                    print(f"\033[35m{items.index(art)+1}\033[0m.\033[33m {art.name}\033[0m, \033[32m${art.value}\033[0m")

                i = input(f"Choose which artefact you would like to buy or \033[35mcancel\033[0m the auction.\n> ").strip().lower()
                print("----")

                if i == "cancel":
                    if b:
                        print(f"You decide to not buy anything else.")
                    else:
                        print("You awkwardly shuffle back into the lobby after buying nothing.")
                    print("----")
                    break

            # TÄMÄ pitää tehdä kahdesti, kun on kaksi whileä päällekkäin
            if i == "cancel":
                break
            i = int(i)
            # poista indeksistä 1 koska näin ne listit toimii
            i -= 1

            #lähetä pelaaja takaisin ostosreissun alkuun jos liian köyhä
            if money < items[i].value:
                print(f"You can't afford this artefact.")
                print("----")
                continue

            money -= items[i].value
            print(f"You purchased the \033[33m{items[i].name}\033[0m for\033[32m ${items[i].value}\033[0m.")
            print("----")
            # vähennä kaupan vero
            items[i].value -= 500
            artefacts.append(items[i])
            # poista kaupasta !!!
            items.remove(items[i])
            b = True

            l.clear()

        # MYYMÄSSÄ!!!
        while selling:
            i = -1

            if len(artefacts) == 0:
                if s:
                    print("Having strategically sold every last artefact, you leave satisfied, confident in this masterful gambit.")
                else:
                    print(f"Before heading to cash in, you realize you have nothing to sell.")
                print("----")
                selling = False
                break
            # Tee uusi lista jossa on pelkästään artefaktien numerot :p
            for a in artefacts:
                str(num.append(str(artefacts.index(a) + 1)))

            # looppaa kunnes pelaaja antaa pätevän vastausken tai häipyy
            while i not in num:

                print(f"You own the following artefacts:")
                list_artefacts(True)
                i = input(
                    f"Choose which artefact you would like to sell or \033[35mcancel\033[0m the auction.\n> ").strip().lower()
                print("----")
                if i == "cancel":
                    # onko myynyt jo jotain?
                    # pilkkaa vähän pelaajaa jos ei
                    if s:
                        print("You decide to not sell anything else.")
                        break
                    else:
                        print("After showing your stock to interested buyers you hastily collect them and leave, leaving your customers dumbfounded.")
                        break

            if i == "cancel":
                print("----")
                break
            # muuta numeroksi
            i = int(i)
            # artefaktit samalta mantereelta kuin valittu
            sm = list()
            # valitun artefaktin manner
            ct = artefacts[i - 1].continent

            for ar in artefacts:
                if ar.continent == ct:
                    sm.append(ar)
            coward = False
            # Onko pelaajalla vain 1 valitun mantereen aarre?
            if len(sm) < 2:
                while True:
                    p = input(
                        f"That's your only artefact from \033[31m{ct}\033[0m. Are you sure you want to \033[35msell\033[0m it, or would you rather \033[35mback\033[0m out?\n> ").strip().lower()
                    if p == "sell":
                        break
                    elif p == "back":
                        coward = True
                        break
                print("----")

            # poista indeksistä 1 koska näin ne listit toimii
            i -= 1
            if coward:
                print(f"Recalling the \033[33m{artefacts[i].name}\033[0m's importance, you snatch it from the buyer's hands and run away.")
            else:
                money += artefacts[i].value
                s = True
                print(
                    f"You sold the \033[33m{artefacts[i].name}\033[0m for\033[32m ${artefacts[i].value}\033[0m!")
                artefacts.remove(artefacts[i])
            print("----")

            # poista numerot artefaktilistasta
            num.clear()

    # FUNKTION LOPPU
    # pelaaja on ostanut
    if b and len(artefacts) > 0:
        print("You leave the auction house, new treasure in tow.")
    # pelaaja on myynyt ja ei ostanut
    elif s:
        print(f"You leave the auction house just a tad richer.")
    # ei kumpaakaan
    else:
        print("You hastily retreat back out of the front door mere moments after entering. At least you killed some time.")
        remaining_actions += 1
    print("----")

def remove_artefact(index):
    if len(artefacts) > 0:

        # Poista tältä mantereelta kotoisin artefakti ekana
        priority = list()
        for a in artefacts:
            if a.continent == cont:
                priority.append(a)
        # Tee randomilla jos ei anneta indeksiä (eli jos jokin event ottaa pelaajalta)
        if not index:
            if len(priority) > 0:
                artefacts.remove(artefacts[random.randint(0, len(priority))])
            else:
                artefacts.remove(artefacts[random.randint(0, len(artefacts))])
        else:
            artefacts.remove(artefacts[index])
    # todo jotain jos pelaajalla ei ole artefakteja?
    else:
        print("Good thing you had no artefacts to lose!")

def list_artefacts(selling):
    if len(artefacts) > 0:
        for a in artefacts:
            if selling:
                print(f"\033[35m{artefacts.index(a)+1}\033[0m: \033[33m{a.name}\033[0m from \033[31m{a.continent}\033[0m, \033[32m${a.value}\033[0m")
            else:
                print(f"{artefacts.index(a) + 1}: \033[33m{a.name}\033[0m from \033[31m{a.continent}\033[0m, \033[32m${a.value}\033[0m")
    else:
        pass

def event():
    global money
    global time
    global artefacts
    global uncompleted_events
    global money_earned
    global artefacts_earned
    global events_completed
    event_id = random.choice(uncompleted_events)
    #event_id = 12
    uncompleted_events.remove(event_id)

    events_completed += 1
    print(events[event_id]["event"])
    choice = ""
    while choice not in events[event_id]["choices"] or money < events[event_id]["choices"][choice]["cost"][
        "money"] or time < events[event_id]["choices"][choice]["cost"]["time"] or len(artefacts) < events[event_id]["choices"][choice]["cost"]["artefacts"]:
        choice = input(f'{events[event_id]["input"]}\n> ').strip().lower()

        if choice in events[event_id]["choices"]:
            if money < events[event_id]["choices"][choice]["cost"]["money"] and time < events[event_id]["choices"][choice]["cost"]["time"] and len(artefacts) < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough of anything for this option.")
            elif money < events[event_id]["choices"][choice]["cost"]["money"] and time < events[event_id]["choices"][choice]["cost"]["time"]:
                print("Before acting on it, you realize that you don't have enough money nor time for this option.")
            elif money < events[event_id]["choices"][choice]["cost"]["artefacts"] and len(artefacts) < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough money nor artefacts for this option.")
            elif time < events[event_id]["choices"][choice]["cost"]["time"] and len(artefacts) < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough time nor artefacts for this option.")
            elif money < events[event_id]["choices"][choice]["cost"]["money"]:
                print(f"Before acting on it, you realize that you don't have enough money for this option.\n----")
            elif time < events[event_id]["choices"][choice]["cost"]["time"]:
                print("Before acting on it, you realize that you don't have enough time for this option.")
            elif len(artefacts) < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough artefacts for this option.")

    print("----")
    # Tapahtuman hinta
    money -= events[event_id]["choices"][choice]["cost"]["money"]
    time -= events[event_id]["choices"][choice]["cost"]["time"]
    if events[event_id]["choices"][choice]["cost"]["artefacts"] > 0:
        remove_artefact(events[event_id]["choices"][choice]["cost"]["artefacts"])

    outcome = random.randint(1, len(events[event_id]["choices"][choice]["results"]))

    #Tapahtuman lopputulos
    print(events[event_id]["choices"][choice]["results"][outcome]["text"],f"\n----")
    money += events[event_id]["choices"][choice]["results"][outcome]["money"]
    if events[event_id]["choices"][choice]["results"][outcome]["money"] > 0:
        money_earned += events[event_id]["choices"][choice]["results"][outcome]["money"]
    if money < 0:
        money = 0
    time += events[event_id]["choices"][choice]["results"][outcome]["time"]
    if time < 0:
        time = 0
    #artefacts += events[event_id]["choices"][choice]["results"][outcome]["artefacts"]
    if events[event_id]["choices"][choice]["results"][outcome]["artefacts"] > 0:
        add_artefact(events[event_id]["choices"][choice]["results"][outcome]["artefacts"])

def check_inventory():
    temp = ["your water bottle", "some snacks", "your phone", "a picture of mommy", "an amulet", "a dreamcatcher", "your lucky rock collection"]
    temp1 = random.choice(temp)
    global visited_countries
    print(f"You open your backpack and reach for {temp1}.")
    print("----")
    print(f"You are currently in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m.")
    color_temp = [f"\033[31m{c}\033[0m" for c in visited_countries]
    if len(color_temp) > 1:
        text = ", ".join(color_temp[:-1]) + " and " + color_temp[-1]
    else:
        text = color_temp[0]
    print("You have been to " + text + f", and travelled \033[36m{total_distance} km\033[0m.")
    print(f"You have \033[32m${money}\033[0m and \033[34m{time} days\033[0m.")
    if len(artefacts) > 0:
        print("You own the following artefacts:")
        list_artefacts(False)
    else:
        print("You don't have any artefacts.")
    print("----")

def choose_continent():
    global cont
    cont_temp = ""
    ant_temp = False
    new_cont = False
    print(
        f"You are currently in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m. Other available continents are",
        end=" ")
    for i in range(len(conts)):
        if cont != conts[i]:
            if i < len(conts) - 1:
                print(f"\033[35m{conts[i]}\033[0m", end=", ")
            else:
                print(f"\033[35m{conts[i]}\033[0m.")
    if cont != "AN":
        while cont_temp != "stay" or cont_temp not in conts:
            cont_temp = input(f"You can either \033[35mstay\033[0m in \033[31m{cont}\033[0m or choose a new continent.\n> ").strip().upper()
            if cont_temp == "STAY" or cont_temp == cont:
                cont = cont
                new_cont = False
                break
            else:
                if cont_temp in conts:
                    # JOS etelänapa
                    if cont_temp == "AN":
                    #   # Jos pelaaja ei pääse
                        if not BOOLEAN_player_has_all_artefacts_and_can_go_to_antarctica():
                            continue
                        else:
                            winning()
                            return
                    cont = cont_temp
                    new_cont = True
                    break
    else:
        while cont_temp not in conts:
            cont_temp = input(f"Choose a new continent to travel to.\n> ").strip().upper()
            if cont_temp == "STAY" or cont_temp == cont:
                cont_temp = ""
            else:
                if cont_temp in conts:
                    # JOS etelänapa
                    if cont_temp == "AN":
                    #   # Jos pelaaja ei pääse
                        if not BOOLEAN_player_has_all_artefacts_and_can_go_to_antarctica():
                            continue
                        else:
                            winning()
                            return
                    cont = cont_temp
                    new_cont = True
                    break
    print("----")
    choose_airport(new_cont, ant_temp)

# ei PÄÄSTÄ pelaajaa loppupisteeseen jos hänellä ei ole jokaista artefaktia
def BOOLEAN_player_has_all_artefacts_and_can_go_to_antarctica():
    # kaikki mantereet
    continents = list(conts)
    # poista omistettujen aarteiden mantereet ja AN koska sieltä ei ole artefaktia
    continents.remove("AN")
    for a in artefacts:
        if continents.__contains__(a.continent):
            continents.remove(a.continent)

    # jos on yhtäkään puuttuvaa mannerta, pelimies ei pääse etelänavalle
    if len(continents) > 0:
        print("----")
        print(f"You're missing artefacts from the following continents: ",end="")
        lanka = [f"\033[31m{c}\033[0m" for c in continents]
        if len(lanka) > 1:
            text = ", ".join(lanka[:-1]) + ", " + lanka[-1]
        else:
            text = lanka[0]
        print(text)
        print("----")
        return False
    else:
        print("----")
        print(f"Having collected the necessary artefacts, you prepare to head to the \033[31mAncient Chamber\033[0m.")
        print("----")
        return True

def winning():
    global game_over
    color_temp = [f"\033[31m{c}\033[0m" for c in visited_countries]
    text = ", ".join(color_temp[:-1]) + " and " + color_temp[-1]
    print(
        "You have arrived at the Ancient Chamber in Antarctica before your time ran out. Well done!\n"
        "Now, it's finally time to complete the ritual, with the \033[33martefacts\033[0m you have collected.\n"
        "Placing the \033[33martefacts\033[0m on the ground in a circle, everything starts to shake.\n"
        "The chamber fills with fog, and you see something blurry in front of you, could it be? It must be!\n"
        "A figure steps through the fog and you recognize it, it's god himself. You have done it!!!"
    )
    print("----")
    print(
        "Along your jorney you visited " + text + f", and travelled a total of \033[36m{total_distance} km\033[0m.\n"
        f"You had \033[32m${money}\033[0m and \033[34m{time} days\033[0m."
    )
    game_over = True

def choose_airport(new_cont, an):
    global airport
    global size
    global country
    global money
    global time
    global remaining_actions
    global uncompleted_events
    global latlong
    global visited_countries
    global total_distance
    airport_names_temp = []
    airport_sizes_temp = []
    airport_country_temp = []
    available_airports_temp = 0
    costs = [100, 200, 300]
    answer_temp = 0
    if an:
        sql = f'SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude FROM airport, country WHERE type="ritual_site" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1;'
    else:
        sql = f'((SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude FROM airport, country WHERE type="small_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude FROM airport, country WHERE type="medium_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude FROM airport, country WHERE type="large_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1));'
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    airport_results = cursor.fetchall()
    cursor.close()

    print(f'Available airports in \033[31m{cont}\033[0m:')

    for i in range(len(airport_results)):
        if new_cont:
            if money >= int(costs[i] * 1.5):
                latlong_temp = (airport_results[i]["latitude"], airport_results[i]["longitude"])
                print(f'\033[35m{i+1}\033[0m: \033[31m{airport_results[i]["name"]}\033[0m, a {airport_results[i]["type"].replace("_"," ")} in \033[31m{airport_results[i]["country"]}\033[0m - \033[36m{int(round(distance.distance(latlong,latlong_temp).km))} km\033[0m - \033[32m${int(costs[i] * 1.5)}\033[0m, \033[34m10 days\033[0m')
                airport_names_temp.append(airport_results[i]["name"])
                airport_sizes_temp.append(airport_results[i]["type"])
                airport_country_temp.append(airport_results[i]["country"])
                available_airports_temp += 1
        else:
            if money >= int(costs[i]):
                latlong_temp = (airport_results[i]["latitude"], airport_results[i]["longitude"])
                print(f'\033[35m{i + 1}\033[0m: \033[31m{airport_results[i]["name"]}\033[0m, a {airport_results[i]["type"].replace("_", " ")} in \033[31m{airport_results[i]["country"]}\033[0m - \033[36m{int(round(distance.distance(latlong,latlong_temp).km))} km\033[0m - \033[32m${int(costs[i])}\033[0m, \033[34m5 days\033[0m')
                airport_names_temp.append(airport_results[i]["name"])
                airport_sizes_temp.append(airport_results[i]["type"])
                airport_country_temp.append(airport_results[i]["country"])
                available_airports_temp += 1
    if available_airports_temp != 0:
        while answer_temp not in range(1, len(airport_results)+1):
            try:
                answer_temp = int(input("Which airport would you like to travel to?\n> "))
            except ValueError:
                pass
        airport = airport_names_temp[answer_temp-1]
        size = airport_sizes_temp[answer_temp-1]
        country = airport_country_temp[answer_temp-1]

        sql = f'SELECT latitude_deg AS latitude, longitude_deg AS longitude FROM airport WHERE name=%s;'
        cursor = conn.cursor()
        cursor.execute(sql, (airport,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            print(f"Warning: coordinates for {airport!r} not found; distance not updated.")
        else:
            dest = (row[0], row[1])  # (lat, lon)
            total_distance += int(round(distance.distance(latlong, dest).km))
            latlong = dest

        if new_cont:
            money -= int(costs[answer_temp-1] * 1.5)
            time -= 10
        else:
            money -= int(costs[answer_temp-1])
            time -= 5
        print("----")
        print(f"You arrive in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m.")
        uncompleted_events = []
        for i in events:
            uncompleted_events.append(i)
        if country not in visited_countries:
            visited_countries.append(country)
        print("----")
        remaining_actions = 3

def trivia(continent):
    global money
    global money_earned
    question_number = random.randint(1,5)
    question = kysymykset[continent][question_number]["kysymys"]
    answer = kysymykset[continent][question_number]["vastaus"]
    print(question)
    if input("> ").lower().strip() == answer:
        print("----")
        print("The man's face lights up. You answered correctly. He hands you \033[32m100€\033[0m and tells you to subscribe to his channel, whatever that means.")
        money += 100
        money_earned += 100
    else:
        print("----")
        print("The man frowns slightly. It doesn't seem like your answer was correct. He thanks you for your time and starts looking for a new contestant. You think the game was rigged.")
    print("----")

def quiz(continent):
    print("Upon your arrival, a young man approaches you. He informs you that he hosts a game show. By answering a question correctly, you win \033[32m100€\033[0m.")
    while True:
        a = input(
            "Do you want to \033[35mplay\033[0m or \033[35mwalk\033[0m away?\n"
            "> "
        )
        if a == "play":
            print("----")
            trivia(continent)
            break
        elif a == "walk":
            print("----")
            print("You can't be bothered to partake in stupid trends and decline the offer.")
            print("----")
            break

def airport_actions():
    global time
    global money
    global remaining_actions
    global money_earned

    achievement()
    if cont != "AN":
        quiz(cont)

    # muokattava lista
    all_actions = ["work", "explore", "auction", "check", "depart"]
    achievement()
    while remaining_actions > 0:
        # Nollaa joka kierroksen alussa
        action = ""
        # Eka vuoro
        if remaining_actions == 3:
            print(
                f"You've just arrived, and thus have {remaining_actions} actions remaining on this airport before the spirit catches you.")
        # toka ja kolmas
        else:
            print(f"You have {remaining_actions} actions remaining on this airport before the spirit catches you.")

        while action not in all_actions:
            action = input(
                "Would you like to either \033[35mcheck\033[0m your stats, \033[35mwork\033[0m, \033[35mexplore\033[0m, visit the \033[35mauction\033[0m house or \033[35mdepart\033[0m?\n> ")

        print("----")
        if action == "work":
            work = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher",
                    "cucumber quality inspector", "tree doctor", "farmer's assistant",
                    "professional supermarket greeter"]
            print(
                f"You decide to work as a {random.choice(work)}. You earn \033[32m$200\033[0m, but lose \033[34m10 days\033[0m.")
            money += 200
            money_earned += 200
            time -= 10
            print("----")
            achievement()
        elif action == "explore":
            event()
            achievement()
        elif action == "auction":
            shop()
            achievement()
        elif action == "check":
            check_inventory()
            # reppuun katsominen ei vie paljon aikaa
            remaining_actions += 1
            achievement()

        elif action == "depart":
            # ei rahea jolla lentöö
            if money < 100:
                # ei rahaa eikä aikaa tehdä duunia
                if remaining_actions <= 1:
                    # pelaajalla artefakti
                    if len(artefacts) > 0:
                        a = artefacts[random.randint(0, len(artefacts))]
                        # todo ehkä vaihtoehtoa pelaajalle tähän - nyt vaan myy aarteen suoraan ilman inputtia
                        print(
                            f"Realizing you have no time or money, you desperately peddle off one of your treasures for travel money.\n----\n"
                            f"You sell off your \033[33m{a.name}\033[0m for \033[32m${random.randint(140, 240)}\033[0m!")
                        print("----")
                    # ei rahaa ei aikaa ei artefaktia - GG
                    else:
                        print(f"Backed into a corner, you find yourself with no way to escape the spirit.")
                        print("----")
                        check_gameover(True)
                # on aikaa - lähde lentokentältä
                else:
                    print(
                        f"Realizing you have no money for a ticket, you sprint out of the airport and reconsider your course of action.")
                    print("----")
                    # takas loopin alkuun
                    continue
            choose_continent()
            check_gameover(False)
            achievement()
            return

        # Onko pelaaja tulhannut kaiken ajan?
        remaining_actions -= 1
        check_gameover(False)

def check_gameover(nomoneyforairport):
    global time
    global remaining_actions
    global game_over
    global money
    temp = ""

    if remaining_actions <= 0 or time <= 0 or nomoneyforairport:
        game_over = True
        if remaining_actions <= 0:
            print(
                "The spirit catches you. You have failed to fulfill your god's wishes and are banished from this realm.")
        elif time <= 0:
            print("You ran out of time. You have failed to fulfill your god's wishes and are banished from this realm.")
        elif money < 100:
            print("Lacking money to escape the spirit, you have failed to fulfill your god's wishes and are banished from this realm.")
        print("----")
        while temp != "accept" or "decline":
            print("You are given the chance to begin anew.")
            temp = input("Do you \033[35maccept\033[0m or \033[35mdecline\033[0m the offer?\n> ")
            if temp == "accept":
                print("----")
                game_over = False
                game_loop()
            elif temp == "decline":
                print(f"----\nGame over.\n----")
                print(
                    f"Your journey ended in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m.")
                color_temp = [f"\033[31m{c}\033[0m" for c in visited_countries]
                if len(color_temp) > 1:
                    text = ", ".join(color_temp[:-1]) + " and " + color_temp[-1]
                else:
                    text = color_temp[0]
                print("You visited " + text + f", and travelled a total of \033[36m{total_distance} km\033[0m.")
                print(f"You had \033[32m${money}\033[0m and \033[34m{time} days\033[0m.")
                if len(artefacts) > 0:
                    print("You owned the following artefacts:")
                    list_artefacts(False)
                else:
                    print("You didn't have any artefacts.")
                break
            break

def achievement():
    global visited_countries
    global money_earned
    global total_distance
    global artefacts_earned
    global events_completed
    global countries_index
    global money_index
    global artefacts_index
    global events_index
    global distance_index

    if len(visited_countries) >= achievements["countries"][countries_index][0]:
        print("You've achieved",achievements["countries"][countries_index][1])
        print("----")
        countries_index += 1
    if money_earned >= achievements["money"][money_index][0]:
        print("You've achieved",achievements["money"][money_index][1])
        print("----")
        money_index += 1
    if total_distance >= achievements["distance"][distance_index][0]:
        print("You've achieved",achievements["distance"][distance_index][1])
        print("----")
        distance_index += 1
    if artefacts_earned >= achievements["artefacts"][artefacts_index][0]:
        print("You've achieved ",achievements["artefacts"][artefacts_index][1])
        print("----")
        artefacts_index += 1
    if events_completed >= achievements["events"][events_index][0]:
        print("You've achieved ",achievements["events"][events_index][1])
        print("----")
        events_index += 1

def all_artefacts_test():
    global cont
    cont = "OC"
    add_artefact(1)
    cont = "NA"
    add_artefact(1)
    cont = "AF"
    add_artefact(1)
    cont = "SA"
    add_artefact(1)
    cont = "AS"
    add_artefact(1)
    cont = "EU"
    add_artefact(1)
    cont = "AN"

def game_loop():
    global game_over
    intro()
    #all_artefacts_test()
    #jos haluu testaa kaikkien artefaktien kanssa, esim voittoa varten
    choose_continent()
    while not game_over:
        check_gameover(False)
        airport_actions()

game_loop()