import random
from event_list import *
from artefacts import *

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
        for i in range(0,len(tup)-1):
            nimi = tup[i]

            # Pelaaja ei voi saada duplikaatteja artifakteista
            if nimi not in names:
                artefacts.append(Artefact(nimi, val, cont))
                names.append(nimi)
                # Poistu loopista jos löydettiin käyttämätön nimi
                break
            else:
                if i == len(tup)-2:
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
                i = int(input(f"number of \033[33martefact\033[0m to sell: ").strip())


                if i == "":
                    print("You awkwardly shuffle back out of the auctionhouse after doing nothing")
                    return
            # poista indeksistä 1 koska näin ne listit toimii

            # TODO: VAROITA PELAAJAA JOS MYY AINOAN JOSTAKIN MANTEREELTA OLEVAN AARTEEN - ehkä ainoastaan jos hän ei ole kyseisellä mantereella sillä hetkellä :-)

            i -= 1
            money += artefacts[int(i)].value
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

add_artefact(1)
while True:
    event()
    if input("Check money, time, artifacts? (y/n) ") == "y":
        print(f"You have \033[32m${money}\033[0m and \033[34m{time} days\033[33m \nCurrent artefacts:\033[0m ")
        list_artefacts()
    print("----")
    if len(artefacts) > 0:
        if input("Would you like to sell\033[33m artefacts\033[0m? (y/n) ") == "y":
            sell_artefacts()
    print("----")



