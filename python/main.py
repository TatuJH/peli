import random
from event_list import *

money = 1000
time = 365
artefacts = 0

class Auto:
    def __init__(self, nimi, arvo, manner):
        self.nimi = nimi
        self.arvo = arvo
        self.manner = manner


def event():
    global money
    global time
    global artefacts
    event_id = random.randint(1, len(events))
    print(events[event_id]["event"])

    choice = ""
    while choice not in events[event_id]["choices"] or money < events[event_id]["choices"][choice]["cost"][
        "money"] or time < events[event_id]["choices"][choice]["cost"]["time"] or artefacts < events[event_id]["choices"][choice]["cost"]["artefacts"]:
        choice = input(events[event_id]["input"]).strip().lower()

        if choice in events[event_id]["choices"]:
            if money < events[event_id]["choices"][choice]["cost"]["money"] and time < events[event_id]["choices"][choice]["cost"]["time"] and artefacts < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough of anything for this option.")
            elif money < events[event_id]["choices"][choice]["cost"]["money"] and time < events[event_id]["choices"][choice]["cost"]["time"]:
                print("Before acting on it, you realize that you don't have enough money nor time for this option.")
            elif money < events[event_id]["choices"][choice]["cost"]["artefacts"] and artefacts < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough money nor artefacts for this option.")
            elif time < events[event_id]["choices"][choice]["cost"]["time"] and artefacts < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough time nor artefacts for this option.")
            elif money < events[event_id]["choices"][choice]["cost"]["money"]:
                print("Before acting on it, you realize that you don't have enough money for this option.")
            elif time < events[event_id]["choices"][choice]["cost"]["time"]:
                print("Before acting on it, you realize that you don't have enough time for this option.")
            elif artefacts < events[event_id]["choices"][choice]["cost"]["artefacts"]:
                print("Before acting on it, you realize that you don't have enough artefacts for this option.")

    money -= events[event_id]["choices"][choice]["cost"]["money"]
    time -= events[event_id]["choices"][choice]["cost"]["time"]
    artefacts -= events[event_id]["choices"][choice]["cost"]["artefacts"]
    outcome = random.randint(1, len(events[event_id]["choices"][choice]["results"]))
    print(events[event_id]["choices"][choice]["results"][outcome]["text"])
    money += events[event_id]["choices"][choice]["results"][outcome]["money"]
    time += events[event_id]["choices"][choice]["results"][outcome]["time"]
    artefacts += events[event_id]["choices"][choice]["results"][outcome]["artefacts"]

event()
print(money)
print(time)
print(artefacts)



