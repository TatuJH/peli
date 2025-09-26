import random
import mysql.connector
from event_list import *
from artefacts import *
from trivia_list import *
from geopy import distance

money = 5000
time = 365
artefacts = list()
cont = "EU"
conts = ["AF", "AN", "AS", "EU", "NA", "OC", "SA"]
airport = "Helsinki Vantaa Airport"
country = "Finland"
size = "large_airport"
remaining_actions = 3
game_over = False
#Ei mitää hajuu mikä on "completed" vastakohta lol
uncompleted_events = []
for i in events:
    uncompleted_events.append(i)
total_distance = 0
visited_countries = []
visited_countries.append(country)

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    # minä itken aina kun tämä muuttuu
    database='demogame',
    user='tatu',
    password='Tietokannat1',
    autocommit=True
)

sql = f'SELECT latitude_deg AS latitude, longitude_deg AS longitude FROM airport WHERE name="{airport}";'
cursor = conn.cursor()
cursor.execute(sql)
latlong = cursor.fetchall()


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

    money = 5000
    time = 365
    artefacts = list()
    cont = "EU"
    conts = ["AF", "AN", "AS", "EU", "NA", "OC", "SA"]
    airport = "Helsinki Vantaa Airport"
    country = "Finland"
    size = "large_airport"
    remaining_actions = 3
    game_over = False
    uncompleted_events = []
    for i in events:
        uncompleted_events.append(i)
    total_distance = 0
    sql = f'SELECT latitude_deg AS latitude, longitude_deg AS longitude FROM airport WHERE name="{airport}";'
    cursor = conn.cursor()
    cursor.execute(sql)
    latlong = cursor.fetchall()

    temp = ""
    print("This game is color-coded. Every time you're presented with a choice, your typeable actions are marked with \033[35mmagenta\033[0m.")
    while temp != "understood":
        temp = input("\033[35mUnderstood\033[0m?\n> ").strip().lower()
    print("----")
    #Tarina tähän????+
    print(f"You arrive in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m. Good luck!\n----")

def print_all():
    print(money, time, cont, country, size, airport, artefacts, uncompleted_events, latlong, total_distance, visited_countries)

def add_artefact(count):
    global cont


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
    if b:
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
        # Tee randomilla jos ei anneta indeksiä (eli jos jokin event ottaa pelaajalta)
        if not index:
                i = random.randint(0, len(artefacts)-1)
                artefacts.remove(i)
        else:
            artefacts.remove(index)

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
    event_id = random.choice(uncompleted_events)
    uncompleted_events.remove(event_id)

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
    while True:
        temp = input(f"After that, would you like to \033[35mcheck\033[0m your statistics or \033[35mclose\033[0m the backpack?\n> ")
        if  temp == "check":
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
            break
        elif temp == "close":
            break
    print("----")

def choose_continent():
    global cont
    cont_temp = ""
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
    while cont_temp != "stay" or cont_temp not in conts:
        cont_temp = input(f"You can either \033[35mstay\033[0m in \033[31m{cont}\033[0m or choose a new continent.\n> ").strip().upper()
        if cont_temp == "STAY" or cont_temp == cont:
            cont = cont
            new_cont = False
            break
        else:
            if cont_temp in conts:
                cont = cont_temp
                new_cont = True
                break
    print("----")
    choose_airport(new_cont)

def choose_airport(new_cont):
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
    sql = f'((SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude FROM airport, country WHERE type="small_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude FROM airport, country WHERE type="medium_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude FROM airport, country WHERE type="large_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1));'
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    airport_results = cursor.fetchall()
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

        sql = f'SELECT latitude_deg AS latitude, longitude_deg AS longitude FROM airport WHERE name="{airport}";'
        cursor = conn.cursor()
        cursor.execute(sql)
        total_distance += int(round(distance.distance(latlong,cursor.fetchall()).km))
        cursor.execute(sql)
        latlong = cursor.fetchall()

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
    else:
        print("You don't have enough money for any airport.")

def trivia(continent):
    global money
    question_number = random.randint(1,5)
    question = kysymykset[continent][question_number]["kysymys"]
    answer = kysymykset[continent][question_number]["vastaus"]
    print(question)
    if input("> ").lower().strip() == answer:
        print("----")
        print("The man's face lights up. You answered correctly. He hands you \033[32m100€\033[0m and tells you to subscribe to his channel, whatever that means.")
        money += 100
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

    quiz(cont)
    # muokattava lista
    all_actions = ["work", "explore", "auction"]
    while remaining_actions > 0:
        check_inventory()
        # Nollaa joka kierroksen alussa
        action = ""
        # Eka vuoro
        if remaining_actions == 3:
            print(
                f"You've just arrived, and thus have {remaining_actions-1} actions remaining on this airport before the spirit catches you.")
        # toka ja kolmas
        else:
            # 1 action :-)
            if remaining_actions == 2:
                print(f"You have {remaining_actions-1} action remaining on this airport before the spirit catches you.")
                all_actions.append("depart")
            # useampi kuin 1 tai 0 o_o
            else:
                print(f"You have {remaining_actions-1} actions remaining on this airport before the spirit catches you.")

        while action not in all_actions:
            if remaining_actions > 2:
                action = input(
                    "Would you like to either \033[35mwork\033[0m, \033[35mexplore\033[0m, or visit the \033[35mauction\033[0m house?\n> ")
            else:
                action = input(
                    "Would you like to either \033[35mwork\033[0m, \033[35mexplore\033[0m, visit the \033[35mauction\033[0m house or \033[35mdepart\033[0m?\n> ")

        print("----")
        if action == "work":
            work = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher",
                    "cucumber quality inspector", "tree doctor", "farmer's assistant",
                    "professional supermarket greeter"]
            print(
                f"You decide to work as a {random.choice(work)}. You earn \033[32m$200\033[0m, but lose \033[34m10 days\033[0m.")
            money += 200
            time -= 10
            print("----")
        elif action == "explore":
            event()
        elif action == "auction":
            shop()

        elif action == "depart":
            choose_continent()
            check_gameover()
            return

        # Onko pelaaja tulhannut kaiken ajan?
        remaining_actions -= 1
        check_gameover()


def check_gameover():
    global time
    global remaining_actions
    global game_over
    global money
    temp = ""

    if remaining_actions <= 0 or time <= 0:
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
                print("----\nGame over.")
                break
            break

def game_loop():
    global game_over
    intro()
    add_artefact(3)
    while not game_over:
        check_gameover()
        airport_actions()

game_loop()

