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
        self.nimi = nimi
        self.arvo = arvo
        self.manner = manner

def add_artefact(count):
    global cont
    # satunnainen raha-arvo
    val = random.randint(600,1000)

    tup = artefact_names[cont]

    # Hanki nimi mantereen perusteella toisesta tiedostosta
    for i in range(0,count):
        nimi = tup[random.randint(0, len(tup) - 1)]
        artefacts.append(Artefact(nimi, val, cont))

def remove_artefact(count):
    i = random.randint(0, len(artefacts)-1)


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
                print("Before acting on it, you realize that you don't have enough money for this option.")
            elif time < events[event_id]["choices"][choice]["cost"]["time"]:
                print("Before acting on it, you realize that you don't have enough time for this option.")
            elif len(artefacts) < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough artefacts for this option.")

    money -= events[event_id]["choices"][choice]["cost"]["money"]
    time -= events[event_id]["choices"][choice]["cost"]["time"]

    if events[event_id]["choices"][choice]["cost"]["artefacts"] > 0:
        remove_artefact(events[event_id]["choices"][choice]["cost"]["artefacts"])
    outcome = random.randint(1, len(events[event_id]["choices"][choice]["results"]))
    print(events[event_id]["choices"][choice]["results"][outcome]["text"])
    money += events[event_id]["choices"][choice]["results"][outcome]["money"]
    time += events[event_id]["choices"][choice]["results"][outcome]["time"]
    #artefacts += events[event_id]["choices"][choice]["results"][outcome]["artefacts"]
    add_artefact(events[event_id]["choices"][choice]["results"][outcome]["artefacts"])

event()
add_artefact(1)
print(money)
print(time)
print(artefacts[0].nimi, artefacts[0].arvo, artefacts[0].manner)



