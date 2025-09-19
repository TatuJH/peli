import random
from random import shuffle
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


# Poista aarre randomilla
def remove_artefact(count):
    if len(artefacts) > 0:
        i = random.randint(0, len(artefacts)-1)

def list_artefacts():
    for a in artefacts:
        print(f"\033[33m{a.name}, valued at ${a.value}, origin: {a.continent}\033[0m")



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
    money -= events[event_id]["choices"][choice]["cost"]["money"]
    time -= events[event_id]["choices"][choice]["cost"]["time"]

    if events[event_id]["choices"][choice]["cost"]["artefacts"] > 0:
        remove_artefact(events[event_id]["choices"][choice]["cost"]["artefacts"])
    outcome = random.randint(1, len(events[event_id]["choices"][choice]["results"]))
    print(events[event_id]["choices"][choice]["results"][outcome]["text"],f"\n----")
    money += events[event_id]["choices"][choice]["results"][outcome]["money"]
    time += events[event_id]["choices"][choice]["results"][outcome]["time"]
    #artefacts += events[event_id]["choices"][choice]["results"][outcome]["artefacts"]
    if events[event_id]["choices"][choice]["results"][outcome]["artefacts"] > 0:
        add_artefact(events[event_id]["choices"][choice]["results"][outcome]["artefacts"])
event()
add_artefact(4)
print(money)
print(time)


while True:
    event()
    if input("Check money, time, artifacts? y/n") == "y":
        print(f"You have \033[32m${money}\033[0m, \033[34m{time} days\033[33m \nCurrent artefacts: ")
        list_artefacts()
    print("----")



