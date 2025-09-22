import random
from event_list import *
from artefacts import *
from trivia_list import *
from time import sleep

money = 1000
time = 365
artefacts = list()

# testausta varten
cont = "EU"

class Artefact:
    def __init__(self, nimi, arvo, manner):
        self.name = nimi
        self.value = arvo
        self.continent = manner

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
        print(f"\nYou arrive at the local auctionhouse...\n")
        # has sold
        b = False

        while auctioning:
            i = -1
            # Tee uusi lista jossa on pelkästään artefaktien numerot :p
            for a in artefacts:
                l.append(artefacts.index(a) + 1)

            # looppaa kunnes pelaaja antaa pätevän vastausken tai häipyy
            while i not in l:

                print(f"You currently own the following:")
                print(f"\033[33m----\033[00m")
                list_artefacts()
                print(f"\033[33m----\033[00m")
                print(f"Which\033[33m artefact\033[0m would you like to sell? Leave empty to cancel")

                i = input(f"number of \033[33martefact\033[0m to sell: ").strip()
                if i == "":
                    if b:
                        print(f"You leave the auctionhouse.")
                        return
                    else:
                        print("You awkwardly shuffle back out of the auctionhouse after doing nothing")
                    return

                #muuta numeroksi
                i = int(i)

            # poista indeksistä 1 koska näin ne listit toimii

            # TODO: VAROITA PELAAJAA JOS MYY AINOAN JOSTAKIN MANTEREELTA OLEVAN AARTEEN - ehkä ainoastaan jos hän ei ole kyseisellä mantereella sillä hetkellä :-)

            i -= 1
            money += artefacts[int(i)].value
            b = True
            print(f"Sold the \033[33m{artefacts[int(i)].name}\033[0m for\033[32m ${artefacts[int(i)].value}\033[0m!")
            artefacts.remove(artefacts[i])

            l.clear()

            if len(artefacts) > 0:
                if input("Sell something else? (y/n) ") != "y":
                    auctioning = False
            else:
                auctioning = False
        print("You leave the auctionhouse.")
    else:
        print(f"You have no\033[33m artefacts\033[0m to sell.")


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
    print(f"\nYou arrive at the local auctionhouse...\n")

    while auctioning:

        b = False

        for a in items:
            l.append(items.index(a) + 1)

        for p in items:
            print(f"{items.index(p)}. artifact is {p.name}")

        for e in l:
            print(e)


        i = -1
        # looppaa kunnes pelaaja antaa pätevän vastausken tai häipyy
        while i not in l:

            print(f"The shop has the following onsale:")
            print(f"\033[33m----\033[00m")
            for art in items:
                print(f"\033[35m{items.index(art)+1}\033[0m.\033[33m {art.name}, price:\033[32m ${art.value}")
            print(f"\033[33m----\033[00m")
            print(f"You have\033[32m ${money}\033[0m")
            print(f"Which\033[33m artefact\033[0m would you like to buy? Leave empty to cancel")
            i = input(f"number of\033[33m artefact\033[0m to to purchase: ").strip()


            if i == "":
                if b:
                    print("You exit the auctionhouse, new treasure in tow.")
                    return
                else:
                    print("You awkwardly shuffle back out of the auctionhouse after doing nothing")
                    return

            i = int(i)

            if money < items[i-1].value:
                print(f"You can't afford this item :/")
                sleep(1.5)
                print("----")
                i = -1
        # poista indeksistä 1 koska näin ne listit toimii
        i -= 1
        money -= items[int(i)].value
        print(f"Purchased the \033[33m{items[int(i)].name}\033[0m for\033[32m ${items[int(i)].value}\033[0m!")
        # vähennä kaupan vero
        items[i].value -= 500
        artefacts.append(items[i])
        # poista kaupasta !!!
        items.remove(items[i])
        b = True

        l.clear()

        if len(artefacts) > 0:
            if input("Buy something else? (y/n) ") != "y":
                auctioning = False
        else:
            auctioning = False
    print("You leave the auctionhouse.")




def remove_artefact(index):
    if len(artefacts) > 0:
        # Tee randomilla jos ei anneta indeksiä (eli jos jokin event ottaa pelaajalta)
        if not index:
                i = random.randint(0, len(artefacts)-1)
                artefacts.remove(i)
        else:
            artefacts.remove(index)


def list_artefacts():
    if len(artefacts) > 0:
        for a in artefacts:
            print(f"{artefacts.index(a)+1}. \033[33m{a.name}\033[0m, valued at \033[32m${a.value}\033[0m, origin: \033[31m{a.continent}\033[0m")
    else:
        print(f"None")


#Hoitaa eventit
def event():
    global money
    global time
    global artefacts
    event_id = random.randint(1, len(events))
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

def trivia(continent):
    question_number = random.randint(1, 5)
    question = kysymykset[continent][question_number]["kysymys"]
    answer = kysymykset[continent][question_number]["vastaus"]

    if input(question) == answer:
        print("Right Answer!")
        #lisäätään pelaajalle rahaa
    else:
        print("Wrong Answer!")
        #ei raahaa / pelaaja menettää rahaa


add_artefact(3)

def check_inventory():
    while True:
        event()
        if input("Check money, time, artifacts? (y/n) ") == "y":
            print(f"You have \033[32m${money}\033[0m and \033[34m{time} days\033[33m \nCurrent artefacts:\033[0m ")
            list_artefacts()
        print("----")
        if len(artefacts) > 0:
            inp = input("Would you like to \033[35mbuy \033[0mor \033[35msell\033[33m artefacts\033[0m?")
            if inp.__contains__("sell"):
                sell_artefacts()
            elif inp.__contains__("buy"):
                shop()
        print("----")


def airport_actions():
    first_action = input(
        "Hey there explorer! It seems like you have landed at the (airport).\n"
        "Remember, the Spirit Demon is after you, so your time here is limited.\n"
        "What would you like to do here? (1. Work, 2. Explore, 3. Buy an artefact)\n"
        ">"
    )

    while first_action not in ["1", "2", "3"]:
        first_action = input(
            "Invalid reply. Please answer with '1' for Working, '2' for Exploring or '3' for Buying an artefact.\n"
            ">"
        )
    if first_action == "1":
        print("You have chosen to work here. A safe choice indeed. You will be awarded 100 credits, but lose 20 days.")
    elif first_action == "2":
        print("Explore")
    elif first_action == "3":
        add_artefact(1)

    second_action = input(
        "Well, I sure hope you made the right decision, because the Spirit Demon will be here soon. You only have time for one more action at this airport. \n"
        "Would you like to either 1. Work, 2. Explore or 3. Buy an artifact or 4. Travel to a new airport?\n"
        ">"
    )
    while second_action not in ["1", "2", "3", "4"]:
        second_action = input(
            "Invalid reply. Please answer with '1' for Working, '2' for Exploring or '3' for Buying an artefact.\n"
            ">"
        )
    if second_action == "1":
        print("You have chosen to work here. A safe choice indeed. You will be awarded 100 credits, but lose 20 days.")
    elif second_action == "2":
        print("Explore")
    elif second_action == "3":
        print("Buy an artefact")
    next_move = input("The Spirit Demon is here. To escape from it, you will have to leave as soon as possible. Do you wish to travel to a new continent? (Y/N)")

    while second_action not in ["Y", "N"]:
        second_action = input("Invalid reply. Please answer with either 'Y' to travel to a new continent or with 'N' to travel to a new airport in your current continent.")
    if next_move == "Y":
        next_continent = input("Which continent do you wish to travel to?")
    elif next_move == "N":
        print("1") #TODO maan sisänen lento
    else:
        print("Invalid reply. Please answer with either 'Y' to travel to a new continent or with 'N' to travel to a new airport in your current continent.")

airport_actions()