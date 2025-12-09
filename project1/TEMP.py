# game_refactor_preserve_prints.py
import random
import mysql.connector
from geopy import distance
from typing import List, Tuple, Optional

# keep your original imports (module names used exactly as you had them)
from event_list import *
from artefacts import *
from trivia_list import *
from achievements import *

# ----------------------------
# DB helper
# ----------------------------
class DB:
    def __init__(self, host='localhost', port=3306, database='demogame', user='tatu', password='Tietokannat1'):
        self.conn = mysql.connector.connect(
            host=host, port=port, database=database, user=user, password=password, autocommit=True
        )

    def fetchone_coords_by_name(self, name: str) -> Optional[Tuple[float, float]]:
        sql = 'SELECT latitude_deg AS latitude, longitude_deg AS longitude FROM airport WHERE name = %s;'
        cur = self.conn.cursor()
        try:
            cur.execute(sql, (name,))
            row = cur.fetchone()
            if row:
                return float(row[0]), float(row[1])
            return None
        finally:
            cur.close()

    def fetch_airports_for_continent(self, continent: str, ritual_only: bool = False):
        cur = self.conn.cursor(dictionary=True)
        try:
            if ritual_only:
                sql = ('SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude '
                       'FROM airport JOIN country ON country.iso_country = airport.iso_country '
                       'WHERE type="ritual_site" AND airport.continent=%s ORDER BY RAND() LIMIT 1;')
                cur.execute(sql, (continent,))
                return cur.fetchall()
            sql = ('(SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude '
                   'FROM airport JOIN country ON country.iso_country = airport.iso_country '
                   'WHERE type="small_airport" AND airport.continent=%s ORDER BY RAND() LIMIT 1) '
                   'UNION ALL '
                   '(SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude '
                   'FROM airport JOIN country ON country.iso_country = airport.iso_country '
                   'WHERE type="medium_airport" AND airport.continent=%s ORDER BY RAND() LIMIT 1) '
                   'UNION ALL '
                   '(SELECT airport.name, type, country.name AS country, latitude_deg AS latitude, longitude_deg AS longitude '
                   'FROM airport JOIN country ON country.iso_country = airport.iso_country '
                   'WHERE type="large_airport" AND airport.continent=%s ORDER BY RAND() LIMIT 1);')
            cur.execute(sql, (continent, continent, continent))
            return cur.fetchall()
        finally:
            cur.close()

# ----------------------------
# Model classes
# ----------------------------
class Artefact:
    def __init__(self, nimi, arvo, manner):
        self.name = nimi
        self.value = arvo
        self.continent = manner

# ----------------------------
# Game class (encapsulates state)
# ----------------------------
class Game:
    def __init__(self, db: DB):
        # initial game-like defaults (these will be set in intro())
        self.db = db

        # mirroring original global variables
        self.money: int = 5000
        self.time: int = 365
        self.artefacts: List[Artefact] = list()
        self.cont: str = ""
        self.conts: List[str] = []
        self.airport: str = ""
        self.country: str = ""
        self.size: str = ""
        self.remaining_actions: int = 0
        self.game_over: bool = False
        self.uncompleted_events: List[int] = []
        self.total_distance: int = 0
        self.visited_countries: List[str] = []
        self.money_earned: int = 0
        self.artefacts_earned: int = 0
        self.events_completed: int = 0
        self.countries_index: int = 0
        self.money_index: int = 0
        self.distance_index: int = 0
        self.artefacts_index: int = 0
        self.events_index: int = 0
        self.latlong: Tuple[float, float] = (0.0, 0.0)

        # attempt to read initial coords for empty airport name to mimic original behaviour
        coords = self.db.fetchone_coords_by_name(self.airport)
        if coords:
            self.latlong = coords

    # ----------------------------
    # preserve original prints exactly
    # ----------------------------
    def intro(self):
        # set state exactly as original intro() did
        self.money = 100000
        self.time = 365
        self.artefacts = list()
        self.cont = "AN"
        self.conts = ["AF", "AN", "AS", "EU", "NA", "OC", "SA"]
        self.airport = "Ancient Chamber"
        self.country = "Antarctica"
        self.size = "ritual_site"
        self.remaining_actions = 3
        self.game_over = False
        self.uncompleted_events = []
        for eve in events:
            self.uncompleted_events.append(eve)
        self.total_distance = 0

        # safe parameterised query
        row = self.db.fetchone_coords_by_name(self.airport)
        if row is None:
            raise RuntimeError(f"No coordinates found for airport {self.airport!r}")
        self.latlong = (row[0], row[1])

        self.visited_countries = [self.country]
        self.money_earned = 0
        self.artefacts_earned = 0
        self.events_completed = 0
        self.countries_index = 0
        self.money_index = 0
        self.distance_index = 0
        self.artefacts_index = 0
        self.events_index = 0

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
                  f"You are given \033[34m{int(self.time)}\033[0m days\033[0m to complete your quest - otherwise the ritual fails.\n"
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

    def print_all(self):
        print(self.money, self.time, self.cont, self.country, self.size, self.airport, self.artefacts, self.uncompleted_events, self.latlong, self.total_distance, self.visited_countries)

    # ----------------------------
    # artefact handling
    # ----------------------------
    def add_artefact(self, count):
        # preserve original behaviour but fix potential None and off-by-one
        if count is None:
            count = 1
        self.artefacts_earned += count

        tup = list(artefact_names[self.cont])
        random.shuffle(tup)

        names = [nm.name for nm in self.artefacts]

        for _ in range(count):
            val = random.randint(600, 1000)
            # iterate through names to find unused one
            found = False
            for i, nimi in enumerate(tup):
                if nimi not in names:
                    self.artefacts.append(Artefact(nimi, val, self.cont))
                    names.append(nimi)
                    found = True
                    break
            if not found:
                # all used -> choose random duplicate safely
                nimi = random.choice(tup)
                self.artefacts.append(Artefact(nimi, val, self.cont))
                names.append(nimi)

    # ----------------------------
    # shop / auction
    # ----------------------------
    def shop(self):
        l = list()
        num = list()
        b = False
        s = False

        items = list()
        tup = list(artefact_names[self.cont])
        random.shuffle(tup)

        names = [nm.name for nm in self.artefacts]

        # number of items in shop
        for _ in range(random.randint(3, 6)):
            val = random.randint(600, 1000)
            val += 500  # tax/markup
            # choose a name not present if possible
            found = False
            for n in range(0, len(tup)):
                nimi = tup[n]
                if nimi not in names:
                    items.append(Artefact(nimi, val, self.cont))
                    names.append(nimi)
                    found = True
                    break
            if not found:
                # pick random (safe index)
                nimi = random.choice(tup)
                # in original code this mistakenly appended to global artefacts,
                # here we append to shop items to mimic intended behaviour
                items.append(Artefact(nimi, val + 0, self.cont))
                names.append(nimi)

        auctioning = True

        while auctioning:
            print("You arrive at the lobby of the auction house.")
            buying = False
            selling = False

            while True:
                inp = input("Would you like to \033[35mbuy\033[0m, \033[35msell\033[0m or\033[35m leave?\033[0m\n> ").strip().lower()
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

            if not auctioning:
                break

            # buying
            while buying:
                l.clear()
                for a in items:
                    l.append(str(items.index(a) + 1))
                i = ""
                if len(l) == 0:
                    print("You bought out the entire stock!")
                    print("----")
                    break
                while i not in l:
                    print(f"You have\033[32m ${self.money}\033[0m. The following artefacts are on auction:")
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

                if i == "cancel":
                    break
                try:
                    i_int = int(i) - 1
                except ValueError:
                    continue
                if not (0 <= i_int < len(items)):
                    continue

                if self.money < items[i_int].value:
                    print(f"You can't afford this artefact.")
                    print("----")
                    continue

                self.money -= items[i_int].value
                print(f"You purchased the \033[33m{items[i_int].name}\033[0m for\033[32m ${items[i_int].value}\033[0m.")
                print("----")
                items[i_int].value -= 500  # reduce value as original did
                self.artefacts.append(items[i_int])
                items.pop(i_int)
                b = True

                l.clear()

            # selling
            while selling:
                if len(self.artefacts) == 0:
                    if s:
                        print("Having strategically sold every last artefact, you leave satisfied, confident in this masterful gambit.")
                    else:
                        print(f"Before heading to cash in, you realize you have nothing to sell.")
                    print("----")
                    selling = False
                    break

                num.clear()
                for a in self.artefacts:
                    num.append(str(self.artefacts.index(a) + 1))

                i = ""
                while i not in num:
                    print(f"You own the following artefacts:")
                    self.list_artefacts(True)
                    i = input(f"Choose which artefact you would like to sell or \033[35mcancel\033[0m the auction.\n> ").strip().lower()
                    print("----")
                    if i == "cancel":
                        if s:
                            print("You decide to not sell anything else.")
                            break
                        else:
                            print("After showing your stock to interested buyers you hastily collect them and leave, leaving your customers dumbfounded.")
                            break

                if i == "cancel":
                    print("----")
                    break

                try:
                    i_int = int(i) - 1
                except ValueError:
                    continue
                if not (0 <= i_int < len(self.artefacts)):
                    continue

                sm = [ar for ar in self.artefacts if ar.continent == self.artefacts[i_int].continent]
                coward = False
                if len(sm) < 2:
                    while True:
                        p = input(f"That's your only artefact from \033[31m{sm[0].continent}\033[0m. Are you sure you want to \033[35msell\033[0m it, or would you rather \033[35mback\033[0m out?\n> ").strip().lower()
                        if p == "sell":
                            break
                        elif p == "back":
                            coward = True
                            break
                    print("----")

                if coward:
                    print(f"Recalling the \033[33m{self.artefacts[i_int].name}\033[0m's importance, you snatch it from the buyer's hands and run away.")
                else:
                    self.money += self.artefacts[i_int].value
                    s = True
                    print(f"You sold the \033[33m{self.artefacts[i_int].name}\033[0m for\033[32m ${self.artefacts[i_int].value}\033[0m!")
                    self.artefacts.pop(i_int)
                print("----")

                num.clear()

        if b and len(self.artefacts) > 0:
            print("You leave the auction house, new treasure in tow.")
        elif s:
            print(f"You leave the auction house just a tad richer.")
        else:
            print("You hastily retreat back out of the front door mere moments after entering. At least you killed some time.")
            self.remaining_actions += 1
        print("----")

    # ----------------------------
    # artefact removal/listing
    # ----------------------------
    def remove_artefact(self, index):
        if len(self.artefacts) > 0:
            priority = [a for a in self.artefacts if a.continent == self.cont]
            if index is None or index is False:
                if len(priority) > 0:
                    # random.choice safe
                    to_remove = random.choice(priority)
                    self.artefacts.remove(to_remove)
                else:
                    to_remove = random.choice(self.artefacts)
                    self.artefacts.remove(to_remove)
            else:
                # index given: validate
                if 0 <= index < len(self.artefacts):
                    self.artefacts.pop(index)
        else:
            print("Good thing you had no artefacts to lose!")

    def list_artefacts(self, selling):
        if len(self.artefacts) > 0:
            for a in self.artefacts:
                if selling:
                    print(f"\033[35m{self.artefacts.index(a)+1}\033[0m: \033[33m{a.name}\033[0m from \033[31m{a.continent}\033[0m, \033[32m${a.value}\033[0m")
                else:
                    print(f"{self.artefacts.index(a) + 1}: \033[33m{a.name}\033[0m from \033[31m{a.continent}\033[0m, \033[32m${a.value}\033[0m")
        else:
            pass

    # ----------------------------
    # events
    # ----------------------------
    def event(self):
        if not self.uncompleted_events:
            for ev in events:
                self.uncompleted_events.append(ev)
        event_id = random.choice(self.uncompleted_events)
        self.uncompleted_events.remove(event_id)

        self.events_completed += 1
        print(events[event_id]["event"])
        choice = ""
        choices_map = events[event_id]["choices"]
        while True:
            choice = input(f'{events[event_id]["input"]}\n> ').strip().lower()
            if choice not in choices_map:
                continue
            cost = choices_map[choice]["cost"]
            if self.money < cost["money"] or self.time < cost["time"] or len(self.artefacts) < cost["artefacts"]:
                # replicate original detailed feedback logic
                if self.money < cost["money"] and self.time < cost["time"] and len(self.artefacts) < cost["artefacts"]:
                    print("Before acting on it, you realize that you don't have enough of anything for this option.")
                elif self.money < cost["money"] and self.time < cost["time"]:
                    print("Before acting on it, you realize that you don't have enough money nor time for this option.")
                elif self.money < cost["money"] and len(self.artefacts) < cost["artefacts"]:
                    print("Before acting on it, you realize that you don't have enough money nor artefacts for this option.")
                elif self.time < cost["time"] and len(self.artefacts) < cost["artefacts"]:
                    print("Before acting on it, you realize that you don't have enough time nor artefacts for this option.")
                elif self.money < cost["money"]:
                    print(f"Before acting on it, you realize that you don't have enough money for this option.\n----")
                elif self.time < cost["time"]:
                    print("Before acting on it, you realize that you don't have enough time for this option.")
                elif len(self.artefacts) < cost["artefacts"]:
                    print("Before acting on it, you realize that you don't have enough artefacts for this option.")
                continue
            break

        print("----")
        self.money -= choices_map[choice]["cost"]["money"]
        self.time -= choices_map[choice]["cost"]["time"]
        if choices_map[choice]["cost"]["artefacts"] > 0:
            # remove that many artefacts randomly (matching previous intent)
            for _ in range(choices_map[choice]["cost"]["artefacts"]):
                self.remove_artefact(None)

        outcome = random.randint(1, len(choices_map[choice]["results"]))
        print(choices_map[choice]["results"][outcome]["text"], f"\n----")
        res = choices_map[choice]["results"][outcome]
        self.money += res["money"]
        if res["money"] > 0:
            self.money_earned += res["money"]
        if self.money < 0:
            self.money = 0
        self.time += res["time"]
        if self.time < 0:
            self.time = 0
        if res["artefacts"] > 0:
            self.add_artefact(res["artefacts"])

    # ----------------------------
    # inventory check
    # ----------------------------
    def check_inventory(self):
        temp = ["your water bottle", "some snacks", "your phone", "a picture of mommy", "an amulet", "a dreamcatcher", "your lucky rock collection"]
        temp1 = random.choice(temp)
        print(f"You open your backpack and reach for {temp1}.")
        print("----")
        print(f"You are currently in \033[31m{self.airport}\033[0m in \033[31m{self.country}\033[0m, \033[31m{self.cont}\033[0m.")
        color_temp = [f"\033[31m{c}\033[0m" for c in self.visited_countries]
        if len(color_temp) > 1:
            text = ", ".join(color_temp[:-1]) + " and " + color_temp[-1]
        else:
            text = color_temp[0] if color_temp else ""
        print("You have been to " + text + f", and travelled \033[36m{self.total_distance} km\033[0m.")
        print(f"You have \033[32m${self.money}\033[0m and \033[34m{self.time} days\033[0m.")
        if len(self.artefacts) > 0:
            print("You own the following artefacts:")
            self.list_artefacts(False)
        else:
            print("You don't have any artefacts.")
        print("----")

    # ----------------------------
    # choose continent / check return
    # ----------------------------
    def choose_continent(self):
        cont_temp = ""
        ant_temp = False
        new_cont = False
        print(f"You are currently in \033[31m{self.airport}\033[0m in \033[31m{self.country}\033[0m, \033[31m{self.cont}\033[0m. Other available continents are", end=" ")
        for i in range(len(self.conts)):
            if self.cont != self.conts[i]:
                if i < len(self.conts) - 1:
                    print(f"\033[35m{self.conts[i]}\033[0m", end=", ")
                else:
                    print(f"\033[35m{self.conts[i]}\033[0m.")
        if self.cont != "AN":
            while True:
                cont_temp = input(f"You can either \033[35mstay\033[0m in \033[31m{self.cont}\033[0m or choose a new continent.\n> ").strip().upper()
                if cont_temp == "STAY" or cont_temp == self.cont:
                    new_cont = False
                    break
                else:
                    if cont_temp in self.conts:
                        if cont_temp == "AN":
                            if not self.BOOLEAN_player_has_all_artefacts_and_can_go_to_antarctica():
                                continue
                            else:
                                self.winning()
                                return
                        self.cont = cont_temp
                        new_cont = True
                        break
        else:
            while True:
                cont_temp = input(f"Choose a new continent to travel to.\n> ").strip().upper()
                if cont_temp == "STAY" or cont_temp == self.cont:
                    cont_temp = ""
                    continue
                else:
                    if cont_temp in self.conts:
                        if cont_temp == "AN":
                            if not self.BOOLEAN_player_has_all_artefacts_and_can_go_to_antarctica():
                                continue
                            else:
                                self.winning()
                                return
                        self.cont = cont_temp
                        new_cont = True
                        break
        print("----")
        self.choose_airport(new_cont, ant_temp)

    def BOOLEAN_player_has_all_artefacts_and_can_go_to_antarctica(self):
        continents = list(self.conts)
        if "AN" in continents:
            continents.remove("AN")
        for a in self.artefacts:
            if a.continent in continents:
                continents.remove(a.continent)
        if len(continents) > 0:
            print("----")
            print(f"You're missing artefacts from the following continents: ", end="")
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

    # ----------------------------
    # winning
    # ----------------------------
    def winning(self):
        color_temp = [f"\033[31m{c}\033[0m" for c in self.visited_countries]
        if len(color_temp) > 1:
            text = ", ".join(color_temp[:-1]) + " and " + color_temp[-1]
        else:
            text = color_temp[0] if color_temp else ""
        print(
            "You have arrived at the Ancient Chamber in Antarctica before your time ran out. Well done!\n"
            "Now, it's finally time to complete the ritual, with the \033[33martefacts\033[0m you have collected.\n"
            "Placing the \033[33martefacts\033[0m on the ground in a circle, everything starts to shake.\n"
            "The chamber fills with fog, and you see something blurry in front of you, could it be? It must be!\n"
            "A figure steps through the fog and you recognize it, it's god himself. You have done it!!!"
        )
        print("----")
        print(
            "Along your jorney you visited " + text + f", and travelled a total of \033[36m{self.total_distance} km\033[0m.\n"
            f"You had \033[32m${self.money}\033[0m and \033[34m{self.time} days\033[0m."
        )
        self.game_over = True

    # ----------------------------
    # choose airport / travel (uses DB helper)
    # ----------------------------
    def choose_airport(self, new_cont, an):
        airport_names_temp = []
        airport_sizes_temp = []
        airport_country_temp = []
        available_airports_temp = 0
        costs = [100, 200, 300]
        answer_temp = 0
        if an:
            airport_results = self.db.fetch_airports_for_continent(self.cont, ritual_only=True)
        else:
            airport_results = self.db.fetch_airports_for_continent(self.cont, ritual_only=False)

        print(f'Available airports in \033[31m{self.cont}\033[0m:')

        for i in range(len(airport_results)):
            row = airport_results[i]
            if new_cont:
                if self.money >= int(costs[i] * 1.5):
                    latlong_temp = (row["latitude"], row["longitude"])
                    print(f'\033[35m{i+1}\033[0m: \033[31m{row["name"]}\033[0m, a {row["type"].replace("_"," ")} in \033[31m{row["country"]}\033[0m - \033[36m{int(round(distance.distance(self.latlong,latlong_temp).km))} km\033[0m - \033[32m${int(costs[i] * 1.5)}\033[0m, \033[34m10 days\033[0m')
                    airport_names_temp.append(row["name"])
                    airport_sizes_temp.append(row["type"])
                    airport_country_temp.append(row["country"])
                    available_airports_temp += 1
            else:
                if self.money >= int(costs[i]):
                    latlong_temp = (row["latitude"], row["longitude"])
                    print(f'\033[35m{i + 1}\033[0m: \033[31m{row["name"]}\033[0m, a {row["type"].replace("_", " ")} in \033[31m{row["country"]}\033[0m - \033[36m{int(round(distance.distance(self.latlong,latlong_temp).km))} km\033[0m - \033[32m${int(costs[i])}\033[0m, \033[34m5 days\033[0m')
                    airport_names_temp.append(row["name"])
                    airport_sizes_temp.append(row["type"])
                    airport_country_temp.append(row["country"])
                    available_airports_temp += 1
        if available_airports_temp != 0:
            while True:
                try:
                    answer_temp = int(input("Which airport would you like to travel to?\n> "))
                except ValueError:
                    continue
                if 1 <= answer_temp <= len(airport_names_temp):
                    break
            idx = answer_temp - 1
            self.airport = airport_names_temp[idx]
            self.size = airport_sizes_temp[idx]
            self.country = airport_country_temp[idx]

            row_coords = self.db.fetchone_coords_by_name(self.airport)
            if row_coords is None:
                print(f"Warning: coordinates for {self.airport!r} not found; distance not updated.")
            else:
                dest = (row_coords[0], row_coords[1])
                self.total_distance += int(round(distance.distance(self.latlong, dest).km))
                self.latlong = dest

            if new_cont:
                self.money -= int(costs[idx] * 1.5)
                self.time -= 10
            else:
                self.money -= int(costs[idx])
                self.time -= 5
            print("----")
            print(f"You arrive in \033[31m{self.airport}\033[0m in \033[31m{self.country}\033[0m, \033[31m{self.cont}\033[0m.")
            self.uncompleted_events = []
            for i in events:
                self.uncompleted_events.append(i)
            if self.country not in self.visited_countries:
                self.visited_countries.append(self.country)
            print("----")
            self.remaining_actions = 3

    # ----------------------------
    # trivia / quiz
    # ----------------------------
    def trivia(self, continent):
        question_number = random.randint(1,5)
        question = kysymykset[continent][question_number]["kysymys"]
        answer = kysymykset[continent][question_number]["vastaus"]
        print(question)
        if input("> ").lower().strip() == answer:
            print("----")
            print("The man's face lights up. You answered correctly. He hands you \033[32m100€\033[0m and tells you to subscribe to his channel, whatever that means.")
            self.money += 100
            self.money_earned += 100
        else:
            print("----")
            print("The man frowns slightly. It doesn't seem like your answer was correct. He thanks you for your time and starts looking for a new contestant. You think the game was rigged.")
        print("----")

    def quiz(self, continent):
        print("Upon your arrival, a young man approaches you. He informs you that he hosts a game show. By answering a question correctly, you win \033[32m100€\033[0m.")
        while True:
            a = input(
                "Do you want to \033[35mplay\033[0m or \033[35mwalk\033[0m away?\n"
                "> "
            )
            if a == "play":
                print("----")
                self.trivia(continent)
                break
            elif a == "walk":
                print("----")
                print("You can't be bothered to partake in stupid trends and decline the offer.")
                print("----")
                break

    # ----------------------------
    # airport action loop
    # ----------------------------
    def airport_actions(self):
        self.achievement()
        if self.cont != "AN":
            self.quiz(self.cont)

        all_actions = ["work", "explore", "auction", "check", "depart"]
        self.achievement()
        while self.remaining_actions > 0:
            action = ""
            if self.remaining_actions == 3:
                print(f"You've just arrived, and thus have {self.remaining_actions} actions remaining on this airport before the spirit catches you.")
            else:
                print(f"You have {self.remaining_actions} actions remaining on this airport before the spirit catches you.")

            while action not in all_actions:
                action = input(
                    "Would you like to either \033[35mcheck\033[0m your stats, \033[35mwork\033[0m, \033[35mexplore\033[0m, visit the \033[35mauction\033[0m house or \033[35mdepart\033[0m?\n> ").strip().lower()

            print("----")
            if action == "work":
                work = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher",
                        "cucumber quality inspector", "tree doctor", "farmer's assistant",
                        "professional supermarket greeter"]
                print(
                    f"You decide to work as a {random.choice(work)}. You earn \033[32m$200\033[0m, but lose \033[34m10 days\033[0m.")
                self.money += 200
                self.money_earned += 200
                self.time -= 10
                print("----")
                self.achievement()
            elif action == "explore":
                self.event()
                self.achievement()
            elif action == "auction":
                self.shop()
                self.achievement()
            elif action == "check":
                self.check_inventory()
                self.remaining_actions += 1
                self.achievement()

            elif action == "depart":
                if self.money < 100:
                    if self.remaining_actions <= 1:
                        if len(self.artefacts) > 0:
                            a = random.choice(self.artefacts)
                            print(
                                f"Realizing you have no time or money, you desperately peddle off one of your treasures for travel money.\n----\n"
                                f"You sell off your \033[33m{a.name}\033[0m for \033[32m${random.randint(140, 240)}\033[0m!")
                            # remove the chosen artefact
                            try:
                                self.artefacts.remove(a)
                            except ValueError:
                                pass
                            print("----")
                        else:
                            print(f"Backed into a corner, you find yourself with no way to escape the spirit.")
                            print("----")
                            self.check_gameover(True)
                    else:
                        print(
                            f"Realizing you have no money for a ticket, you sprint out of the airport and reconsider your course of action.")
                        print("----")
                        continue
                self.choose_continent()
                self.check_gameover(False)
                self.achievement()
                return

            self.remaining_actions -= 1
            self.check_gameover(False)

    # ----------------------------
    # game over / check
    # ----------------------------
    def check_gameover(self, nomoneyforairport):
        temp = ""

        if self.remaining_actions <= 0 or self.time <= 0 or nomoneyforairport:
            self.game_over = True
            if self.remaining_actions <= 0:
                print(
                    "The spirit catches you. You have failed to fulfill your god's wishes and are banished from this realm.")
            elif self.time <= 0:
                print("You ran out of time. You have failed to fulfill your god's wishes and are banished from this realm.")
            elif self.money < 100:
                print("Lacking money to escape the spirit, you have failed to fulfill your god's wishes and are banished from this realm.")
            print("----")
            while True:
                print("You are given the chance to begin anew.")
                temp = input("Do you \033[35maccept\033[0m or \033[35mdecline\033[0m the offer?\n> ")
                if temp == "accept":
                    print("----")
                    self.game_over = False
                    # restart game by re-running main loop
                    self.game_loop()
                    break
                elif temp == "decline":
                    print(f"----\nGame over.\n----")
                    print(
                        f"Your journey ended in \033[31m{self.airport}\033[0m in \033[31m{self.country}\033[0m, \033[31m{self.cont}\033[0m.")
                    color_temp = [f"\033[31m{c}\033[0m" for c in self.visited_countries]
                    if len(color_temp) > 1:
                        text = ", ".join(color_temp[:-1]) + " and " + color_temp[-1]
                    else:
                        text = color_temp[0] if color_temp else ""
                    print("You visited " + text + f", and travelled a total of \033[36m{self.total_distance} km\033[0m.")
                    print(f"You had \033[32m${self.money}\033[0m and \033[34m{self.time} days\033[0m.")
                    if len(self.artefacts) > 0:
                        print("You owned the following artefacts:")
                        self.list_artefacts(False)
                    else:
                        print("You didn't have any artefacts.")
                    break
                break

    # ----------------------------
    # achievements
    # ----------------------------
    def achievement(self):
        if self.countries_index < len(achievements["countries"]) and len(self.visited_countries) >= achievements["countries"][self.countries_index][0]:
            print("You've achieved",achievements["countries"][self.countries_index][1])
            print("----")
            self.countries_index += 1
        if self.money_index < len(achievements["money"]) and self.money_earned >= achievements["money"][self.money_index][0]:
            print("You've achieved",achievements["money"][self.money_index][1])
            print("----")
            self.money_index += 1
        if self.distance_index < len(achievements["distance"]) and self.total_distance >= achievements["distance"][self.distance_index][0]:
            print("You've achieved",achievements["distance"][self.distance_index][1])
            print("----")
            self.distance_index += 1
        if self.artefacts_index < len(achievements["artefacts"]) and self.artefacts_earned >= achievements["artefacts"][self.artefacts_index][0]:
            print("You've achieved",achievements["artefacts"][self.artefacts_index][1])
            print("----")
            self.artefacts_index += 1
        if self.events_index < len(achievements["events"]) and self.events_completed >= achievements["events"][self.events_index][0]:
            print("You've achieved",achievements["events"][self.events_index][1])
            print("----")
            self.events_index += 1

    # ----------------------------
    # all_artefacts_test (kept)
    # ----------------------------
    def all_artefacts_test(self):
        self.cont = "OC"
        self.add_artefact(1)
        self.cont = "NA"
        self.add_artefact(1)
        self.cont = "AF"
        self.add_artefact(1)
        self.cont = "SA"
        self.add_artefact(1)
        self.cont = "AS"
        self.add_artefact(1)
        self.cont = "EU"
        self.add_artefact(1)
        self.cont = "AN"

    # ----------------------------
    # main loop
    # ----------------------------
    def game_loop(self):
        self.intro()
        #self.all_artefacts_test()
        self.choose_continent()
        while not self.game_over:
            self.check_gameover(False)
            if self.game_over:
                break
            self.airport_actions()

# ----------------------------
# bootstrap
# ----------------------------
def main():
    db = DB()
    game = Game(db)
    game.game_loop()

if __name__ == "__main__":
    main()
