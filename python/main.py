import random
import mysql.connector
from event_list import *
from artefacts import *
from trivia_list import *

money = 5000
time = 365
artefacts = list()
cont = "EU"
conts = ["AF", "AN", "AS", "EU", "NA", "OC", "SA"]
airport = "Helsinki Vantaa Airport"
country = "Finland"
size = "large_airport"
remaining_actions = 2

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame',
    user='tatu',
    password='Tietokannat1',
    autocommit=True
)

class Artefact:
    def __init__(self, nimi, arvo, manner):
        self.name = nimi
        self.value = arvo
        self.continent = manner

def print_all():
    print(money, time, cont, country, size, airport, artefacts)

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

def sell_artefacts():
    global money
    if len(artefacts) > 0:
        l = list()

        auctioning = True
        print(f"You arrive at the local auction house.")
        print("----")
        # has sold
        b = False

        while auctioning:
            i = -1
            # Tee uusi lista jossa on pelkästään artefaktien numerot :p
            for a in artefacts:
                l.append(artefacts.index(a) + 1)

            # looppaa kunnes pelaaja antaa pätevän vastausken tai häipyy
            while i not in l:

                print(f"You own the following artefacts:")
                list_artefacts(True)
                i = input(f"Choose which artefact you would like to sell or \033[35mcancel\033[0m the auction.\n> ").strip().lower()
                print("----")
                if i == "cancel":
                    if b:
                        print(f"You leave the auction house just a tad richer.")
                        return
                    else:
                        print("You awkwardly shuffle out of the auction house after doing nothing.")
                        print("----")
                    return

                #muuta numeroksi
                i = int(i)

                sm = list()
                ct = artefacts[i-1].continent

                for ar in artefacts:
                    if ar.continent == ct:
                        sm.append(ar)

                if len(sm) < 2:
                    # looppaa kunnes tulee korrekti vastaus y/n
                    while True:
                        p = input(f"That's your only artefact from \033[31m{ct}\033[0m. Are you sure you want to \033[35msell\033[0m it, or would you rather \033[35mback\033[0m out?\n> ").strip().lower()
                        if p == "sell":
                            break
                        elif p == "back":
                            break
                    print("----")
            # poista indeksistä 1 koska näin ne listit toimii
            i -= 1
            money += artefacts[int(i)].value
            b = True
            print(f"You sold the \033[33m{artefacts[int(i)].name}\033[0m for\033[32m ${artefacts[int(i)].value}\033[0m.")
            artefacts.remove(artefacts[i])
            print("----")

            l.clear()

            if len(artefacts) > 0:
                while True:
                    p = input("Would you like to \033[35msell\033[0m something else or \033[35mleave\033[0m the auction house?\n> ").strip().lower()
                    if p == "leave":
                        auctioning = False
                        break
                    elif p == "sell":
                        break
            else:
                auctioning = False
            print("----")
        print("You leave the auction house just a tad richer.")
    else:
        print(f"You have no artefacts to sell.")

def shop():
    global money
    l = list()

    # Tee uusi lista jossa on pelkästään artefaktien numerot :p
    items = list()
    tup = list(artefact_names[cont])
    # Sekoita artefaktien lista jotta pelaaja ei saa jokaisella pelikerralla samoja aarteita ekana
    random.shuffle(tup)

    # Lista nykyisistä pelaajan artefakteista
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
    print(f"You arrive at the local auction house.")

    for a in items:
        l.append(items.index(a) + 1)

    print("----")
    while auctioning:

        b = False


        i = -1
        # looppaa kunnes pelaaja antaa pätevän vastausken tai häipyy
        while i not in l:

            print(f"You have\033[32m ${money}\033[0m. The following artefacts are on auction:")
            for art in items:
                print(f"\033[35m{items.index(art)+1}\033[0m.\033[33m {art.name}\033[0m, \033[32m${art.value}\033[0m")
            i = input(f"Choose which artefact you would like to buy or \033[35mcancel\033[0m the auction.\n> ").strip().lower()
            print("----")
            if i == "cancel":
                if b:
                    print("You leave the auction house, new treasure in tow.")
                    return
                else:
                    print("You awkwardly shuffle out of the auction house after doing nothing.")
                    print("----")
                    return

            i = int(i)

            if money < items[i-1].value:
                print(f"You can't afford this artefact.")
                print("----")
                i = -1
        # poista indeksistä 1 koska näin ne listit toimii
        i -= 1
        money -= items[int(i)].value
        print(f"You purchased the \033[33m{items[int(i)].name}\033[0m for\033[32m ${items[int(i)].value}\033[0m.")
        print("----")
        # vähennä kaupan vero
        items[i].value -= 500
        artefacts.append(items[i])
        # poista kaupasta !!!
        items.remove(items[i])
        b = True

        l.clear()

        if len(artefacts) > 0:
            while True:
                p = input("Would you like to \033[35mbuy\033[0m something else or \033[35mleave\033[0m the auction house?\n> ")
                if p == "leave":
                    auctioning = False
                    break
                elif p == "buy":
                    break
            print("----")
    print("You leave the auction house, new treasure in tow.")
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
        print(f"You don't have any artefacts.")

#Hoitaa eventit
def event():
    global money
    global time
    global artefacts
    event_id = random.randint(1,len(events))
    print(events[event_id]["event"])
    choice = ""
    while choice not in events[event_id]["choices"] or money < events[event_id]["choices"][choice]["cost"][
        "money"] or time < events[event_id]["choices"][choice]["cost"]["time"] or len(artefacts) < events[event_id]["choices"][choice]["cost"]["artefacts"]:
        choice = input(events[event_id]["input"]).strip().lower()

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
    while True:
        temp = input(f"You open your backpack and reach for {temp1}. While you're at it, would you like to \033[35mcheck\033[0m your money, time and artefacts or \033[35mclose\033[0m the backpack?\n> ")
        if  temp == "check":
            print("----")
            print(f"You have \033[32m${money}\033[0m and \033[34m{time} days\033[0m.\nYou own the following artefacts:")
            list_artefacts(False)
            break
        elif temp == "close":
            break
    print("----")

def choose_continent():
    global cont
    cont_temp = ""
    new_cont = False
    while cont_temp != "stay" or cont_temp not in conts:
        print(f"You are currently in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m. Other available continents are", end=" ")
        for i in range(len(conts)):
            if cont != conts[i]:
                if i < len(conts)-1:
                    print(f"\033[35m{conts[i]}\033[0m", end=", ")
                else:
                    print(f"\033[35m{conts[i]}\033[0m.")
        cont_temp = input(f"You can either \033[35mstay\033[0m in \033[31m{cont}\033[0m or choose a new continent from the list above.\n> ").strip().upper()
        if cont_temp == "STAY":
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
    airport_names_temp = []
    airport_sizes_temp = []
    airport_country_temp = []
    available_airports_temp = 0
    costs = [100, 200, 300]
    answer_temp = 0
    sql = f'((SELECT airport.name, type, country.name AS country FROM airport, country WHERE type="small_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name, type, country.name AS country FROM airport, country WHERE type="medium_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name, type, country.name AS country FROM airport, country WHERE type="large_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country ORDER BY RAND() LIMIT 1));'
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    airport_results = cursor.fetchall()
    print(f'Available airports in \033[31m{cont}\033[0m:')
    for i in range(len(airport_results)):
        if new_cont:
            if money >= int(costs[i] * 1.5):
                print(f'\033[35m{i+1}\033[0m: \033[31m{airport_results[i]["name"]}\033[0m, a {airport_results[i]["type"].replace("_"," ")} in \033[31m{airport_results[i]["country"]}\033[0m - \033[32m${int(costs[i] * 1.5)}\033[0m, \033[34m10 days\033[0m')
                airport_names_temp.append(airport_results[i]["name"])
                airport_sizes_temp.append(airport_results[i]["type"])
                airport_country_temp.append(airport_results[i]["country"])
                available_airports_temp += 1
        else:
            print(f'\033[35m{i + 1}\033[0m: \033[31m{airport_results[i]["name"]}\033[0m, a {airport_results[i]["type"].replace("_", " ")} in \033[31m{airport_results[i]["country"]}\033[0m - \033[32m${int(costs[i])}\033[0m, \033[34m5 days\033[0m')
            airport_names_temp.append(airport_results[i]["name"])
            airport_sizes_temp.append(airport_results[i]["type"])
            airport_country_temp.append(airport_results[i]["country"])
            available_airports_temp += 1
    if available_airports_temp != 0:
        while answer_temp not in range(1, len(airport_results)+1):
            try:
                answer_temp = int(input("Which airport would you like to travel to?\n> "))
            except ValueError:
                print("Which airport would you like to travel to?")
        airport = airport_names_temp[answer_temp-1]
        size = airport_sizes_temp[answer_temp-1]
        country = airport_country_temp[answer_temp-1]
        if new_cont:
            money -= int(costs[answer_temp-1] * 1.5)
            time -= 10
        else:
            money -= int(costs[answer_temp-1])
            time -= 5
        print("----")
        print(f"You arrive in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m.")
        print("----")
    else:
        print("You don't have enough money for any airport.")

def trivia(continent):
    global money
    question_number = random.randint(1,5)
    question = kysymykset[continent][question_number]["kysymys"]
    answer = kysymykset[continent][question_number]["vastaus"]
    print(question)
    print("(Psst. Remember capital letters!)")
    if input("> ") == answer:
        print("Yes! You got it right. The man hands you the \033[32m100€\033[0m and tells you to subscribe to his YouTube-channel.")
        money += 100

def quiz(continent):
    i = random.randint(1,9)
    if i >= 2:
        while True:
            a = input(
                "Quick! A man approaches you at the airport, informing you that he's an YouTube-influencer.\n"
                "The man tells you that if you answer his question correctly, you will win \033[32m100€\033[0m. Do you want to \033[35mplay\033[0m or \033[35mwalk\033[0m away?\n"
                "> "
            )
            if a == "play":
                trivia(continent)
                break
            elif a == "walk":
                print("Well then, no one is forcing you to play.")
                break

def airport_actions():
    global time
    global money
    global remaining_actions
    check_inventory()
    first_action = ""
    second_action = ""

    print(f"You just arrived, and thus have {remaining_actions} actions remaining on this airport before the spirit catches you.")
    quiz(cont)
    while first_action not in ["work", "explore", "auction"]:
        first_action = input("Would you like to either \033[35mwork\033[0m, \033[35mexplore\033[0m, or visit the \033[35mauction\033[0m house?\n> ")
    print("----")
    if first_action == "work":
        work = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher", "cucumber quality inspector", "tree doctor", "farmer's assistant", "professional supermarket greeter"]
        print(f"You decide to work as a {random.choice(work)}. You earn \033[32m$200\033[0m, but lose \033[34m10 days\033[0m.")
        money += 200
        time -= 10
        print("----")
    elif first_action == "explore":
        event()
    elif first_action == "auction":
        shop()
    remaining_actions -= 1

    check_inventory()
    print(f"You have {remaining_actions} action remaining on this airport before the spirit catches you.")
    while second_action not in ["work", "explore", "auction", "leave"]:
        second_action = input("Would you like to either \033[35mwork\033[0m, \033[35mexplore\033[0m, visit the \033[35mauction\033[0m house or \033[35mleave\033[0m this airport?\n> ")
    print("----")
    if second_action == "work":
        work = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher",
                "cucumber quality inspector", "tree doctor", "farmer's assistant", "professional supermarket greeter"]
        print(
            f"You decide to work as a {random.choice(work)}. You earn \033[32m$200\033[0m, but lose \033[34m10 days\033[0m.")
        money += 200
        time -= 10
        print("----")
    elif second_action == "explore":
        event()
    elif second_action == "auction":
        shop()
    elif second_action == "leave":
        choose_continent()

add_artefact(2)
airport_actions()
shop()
check_inventory()