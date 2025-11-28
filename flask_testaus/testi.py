import mysql.connector
import random

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demokanta',
    user='tatu',
    password='Tietokannat1',
    autocommit=True
)

money_modifier = 1

def intro_text():
    intro_text1 = ("You belong in a cult dead-set on waking up an ancient god."
                   "After centuries of hard work, the moment is finally at hand."
                   "You arrive in an ancient chamber located in Antarctica. The chamber smells of sulfur and debris on the ground seems to move on its own."
                   "In the middle of the chamber lies a circle made of lit candles. You step in, and start performing a ritual."
                   "You feel the air rising as a fading projection of your god appears in front of you. You hear a deep voice."
                   "The voice commands you to bring him six artefacts - one from each of the other continents - to finish the ritual."
                   "After you have found and collected an artefact from every other continent, you shall return to Antarctica."
                   "You are given limited time to complete your quest - otherwise the ritual fails."
                   "In addition, to ensure your obedience, a spirit is sent after you. You feel as if you don't want to make contact with it."
                   "You leave the chamber as a waning voice behind you asks you to hurry.<br>")

    intro_text2 = ("Important things to note:",
                   "- You only have a limited number of actions on each airport, and if you don't depart as your last action, the spirit will catch you.",
                   "- Working gives you money, but costs you time.",
                   "- Exploring consists of randomized events, which can both cost and reward money, time or artefacts.",
                   "- Converting heretics is a fighting minigame. Winning nets you money. The actions are as follows:",
                   "  STRIKE (#) decreases the selected enemy's stamina, but has a chance to miss.",
                   "  HEAL (#) heals you based on your current stamina, and has limited uses.",
                   "  GUARD decreases the amount of stamina you lose from enemy attacks.",
                   "- In the auction house you can either buy or sell artefacts.",
                   "- Each action consumes days in addition to other costs.",
                   "- Traveling to another continent costs more.",
                   "- Airport size determines the cost of travel and affects some rewards.")

    return intro_text1, intro_text2


def scores():
    sql = "SELECT id, score FROM scores WHERE score IN (SELECT MAX(score) FROM scores);"
    cursor = conn.cursor()
    cursor.execute(sql)
    highest = cursor.fetchall()

    if len(highest) > 0:
        print(f"Your highest score was {highest[0][1]} in game {highest[0][0]}.")
        sql = "SELECT * FROM scores;"
        cursor = conn.cursor()
        cursor.execute(sql)
        scorelist = cursor.fetchall()
        scorelist2 = {}
        for scoretemp in range(len(scorelist)):
            scorelist2[scorelist[scoretemp][0]] = scorelist[scoretemp][1]

        print(scorelist2)
        return scorelist2

scores()

eventit = {
        1:{
            "event":f"You are given an investment opportunity on the street by a man in a trench coat. He says that by giving him ${int(round(100*money_modifier))} you could make ${int(round(300*money_modifier))}." ,
            "input":"Do you want to invest or decline the opportunity?",
            "choices":{
                "invest":{
                    f"cost":{"money":int(round(100*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{f"money":int(round(300*money_modifier)),"time":0,"artefacts":0,"text":f"The opportunity actually paid out. You earned ${int(round(300*money_modifier))}."},
                        2:{"money":0,"time":0,"artefacts":0,"text":f"The opportunity was real... But you lost your ${int(round(100*money_modifier))}."},
                        3:{"money":int(round(200*money_modifier)),"time":-10,"artefacts":0,"text":f"The man takes off running! You chase him and get your ${int(round(100*money_modifier))} back. You also manage to snatch ${int(round(100*money_modifier))} extra from him, but lose 10 days in the process."}
                    }
                },
                "decline":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"You decline the man's offer. It was probably a scam anyway."}
                    }
                }
            }
        },
        2:{
            "event":f"You meet a witch, who says she can buy you time. Literally. She offers you 10 days in exchange for $200.",
            "input":"Do you accept or decline the offer?",
            "choices":{
                "accept":{
                    "cost":{f"money":200,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":15,"artefacts":0,"text":"You bought yourself some time. 10 days to be exact."}
                    }
                },
                "decline":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-10,"artefacts":0,"text":"The witch gets mad at you declining her offer. She curses you, draining you of 10 days."}
                    }
                }
            }
        },
        3:{
            "event":"You get lost, somehow.",
            "input":"Would you like to turn left, right or continue straight?",
            "choices":{
                "left":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-10,"artefacts":0,"text":"You get even more lost, losing 10 days in the process. Eventually, you find your way back."}
                    }
                },
                "right":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"As you turn right, you notice that the airport is literally just there. Talk about luck."}
                    }
                },
                "straight":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":50,"time":-10,"artefacts":0,"text":f"That wasn't the right way and you lose 10 days. On a positive note, you find ${int(round(50*money_modifier))} on the ground."},
                        2:{"money":100,"time":-10,"artefacts":0,"text":f"That wasn't the right way and you lose 10 days. On a positive note, you find ${int(round(100*money_modifier))} on the ground."},
                        3:{"money":200,"time":-10,"artefacts":0,"text":f"That wasn't the right way and you lose 10 days. On a positive note, you find ${int(round(150*money_modifier))} on the ground."}
                    }
                }
            }
        },
        4:{
            "event":"You stumble upon some sort of monument. There is a sign asking you to pray.",
            "input":"Do you pray on your knees, standing up or do you leave?",
            "choices":{
                "knees":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"Something rumbles. A hatch opens underneath the monument, revealing an artefact. The gods must be pleased."},
                        2:{"money":0,"time":-15,"artefacts":1,"text":"The monument shakes and reveals something under it. You take a peek and lose consciousness. You wake up 15 days later and find an artefact next to you."},
                        3:{"money":int(round(-100*money_modifier)),"time":-10,"artefacts":0,"text": f"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of ${int(round(100*money_modifier))} and 10 days."}

                    }
                },
                "standing":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(-100*money_modifier)),"time":-10,"artefacts":0,"text":f"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of ${int(round(100*money_modifier))} and 10 days."},
                        2:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"You feel a pleasant sensation. The gods must've been pleased with your praying. You notice you're carrying ${int(round(100*money_modifier))} more than before."}
                    }
                },
                "leave":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"You decide to not accidentally disrespect the gods."},
                        2:{"money":0,"time":-5,"artefacts":0,"text":"Gearing to leave, you feel the earth starting to tremble. The gods weren't happy about you not honoring them. You black out and lose 5 days."}
                    }
                }
            }
        },
        5:{
            "event":"You see a man in a suit strolling on the street. He seems to be giving money to some people he meets.",
            "input":'Do you greet him with a "hello", a "good evening sir" or do you do nothing?',
            "choices":{
                "hello":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"The man replies and hands you ${int(round(100*money_modifier))}."}
                    }
                },
                "good evening":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(200*money_modifier)),"time":0,"artefacts":0,"text":f"The man seems happy and hands you ${int(round(200*money_modifier))}."},
                        2:{"money":int(round(300*money_modifier)),"time":0,"artefacts":0,"text":f"The man says how refreshing good manners are and hands you ${int(round(300*money_modifier))}."}
                    }
                },
                "nothing":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"You pass him by. You don't need his pity money."}
                    }
                }
            }
        },
        6:{
            "event":f'You accidentally bump into a towering man on the street. You try to apologize, but the man seeks {int(round(200*money_modifier))} for "physical pain". Like he felt anything.',
            "input":f"Do you pay him the ${int(round(200*money_modifier))} he asks for, try to settle for ${int(round(100*money_modifier))} or refuse to pay?",
            "choices":{
                f"{int(round(200*money_modifier))}":{
                    "cost":{"money":int(round(200*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":f"The man scoffs, relieving you of your ${int(round(200*money_modifier))}. He gives you one last angry look and leaves."}
                    }
                },
                f"{int(round(100*money_modifier))}":{
                    "cost":{"money":int(round(100*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-5,"artefacts":0,"text":f"The man seems unimpressed. He looks you up and down, takes your ${int(round(100*money_modifier))} and pushes you to the ground. You lose  5 days."}
                    }
                },
                "refuse":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(-200*money_modifier)),"time":0,"artefacts":0,"text":f"The man seems outright outraged. He quickly reaches into your pocket and takes ${int(round(200*money_modifier))}."},
                        2:{"money":int(round(-150*money_modifier)),"time":0,"artefacts":0,"text":f"The man seems outright outraged. He quickly reaches into your pocket and takes ${int(round(150*money_modifier))}."}
                    }
                }
            }
        },
        7:{
            "event":f'You notice a small well. A woman stands next to it, holding a cardboard sign. On it, she has written: "One coin = ${int(round(300*money_modifier))}." Must be a wishing well.',
            "input":f"Do you want to buy a coin for ${int(round(300*money_modifier))} or pass on the opportunity?",
            "choices":{
                "buy":{
                    "cost":{"money":int(round(300*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(300*money_modifier)),"time":0,"artefacts":0,"text":f"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find ${int(round(300*money_modifier))}."},
                        2:{"money":int(round(450*money_modifier)),"time":0,"artefacts":0,"text":f"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find ${int(round(450*money_modifier))}."},
                        3:{"money":int(round(600*money_modifier)),"time":0,"artefacts":0,"text":f"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find ${int(round(600*money_modifier))}."},
                        4:{"money":0,"time":20,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive 20 days."},
                        5:{"money":0,"time":30,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive 30 days."},
                        6:{"money":0,"time":40,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive 40 days."}
                    }
                },
                "pass":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"You? Superstitious? Like any normal person, you decide to save your money."}
                    }
                }
            }
        },
        8:{
            "event":"You hear sounds of metal hitting rock. Upon further inspection, you find a dig site, where a dozen men are swinging their pickaxes. \nOne of the men offers you their position for 20 days.",
            "input":f"Do you accept it, pay the man ${int(round(200*money_modifier))} to dig for you or refuse?",
            "choices":{
                "accept":{
                    "cost":{"money":0,"time":20,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"You dig and dig. Finally, your pickaxe strikes something softer. You frantically wipe away some dirt, revealing a slightly battered artefact."},
                        2:{"money":int(round(50*money_modifier)),"time":0,"artefacts":0,"text":f"You dig and dig. Finally, your pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around ${int(round(50*money_modifier))}."}
                    }
                },
                "pay":{
                    "cost":{"money":int(round(200*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"The man digs and digs. Finally, his pickaxe strikes something softer. You rush to the scene, frantically wipe away some dirt and reveal a slightly battered artefact."},
                        2:{"money":int(round(50*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around ${int(round(50*money_modifier))}."},
                        3:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around ${int(round(100*money_modifier))}."},
                        4:{"money":int(round(150*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around ${int(round(150*money_modifier))}."}
                    }
                },
                "refuse":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"You don't have the energy nor the money for this. What were they even digging for, stones?"}
                    }
                }
            }
        },
        9:{
            "event":"You hear a thunderstorm starting to build up. This wasn't in the weather forecasts. The only building you see nearby is some sort of motel.",
            "input":f"Do you rent a room for the night for ${int(round(50*money_modifier))} or try finding some makeshift shelter?",
            "choices":{
                "rent":{
                    "cost":{"money":int(round(50*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-10,"artefacts":0,"text":"You wait out the storm, losing 10 days. At least you leave the motel unscathed."}
                    }
                },
                "shelter":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(-100*money_modifier)),"time":-15,"artefacts":0,"text":f"You find a small crevice and hole up inside. You're left unharmed by the storm, but lose 15 days and ${int(round(100*money_modifier))} for the arthritis you develop."},
                        2:{"money":0,"time":-20,"artefacts":0,"text":"You wander for a while and find an old, run-down cabin and hide there. Unfortunately, lightning strikes the unprotected shack, shocking you of 20 days."},
                        3:{"money":0,"time":-15,"artefacts":0,"text":"You decide to lay low in an open area, covering yourself with leaves to keep the rain out. You wake up unscathed but freezing and lose 15 days."}
                    }
                }
            }
        },
        10: {
            "event": "You see an old building in the distance. Walking closer to it, you become pretty sure it's abandoned.",
            "input": "Do you go inside the building, check its surroundings it, or walk away?",
            "choices": {
                "inside": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 1,
                            "text": "The inside of building is very dark and you decide to use your phone's flashlight. On the ground, you spot an artefact buried in rubble."},
                        2: {"money": 0, "time": -10, "artefacts": 1,
                            "text": "As you walk in, a trapdoor opens under your feet. The fall is harsh, and you wake up after 10 days to the glimmering of an artefact."},
                        3: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You walk around the house, but find nothing inside. It seems the building was abandoned for a reason."}
                    }
                },
                "surroundings": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 1,
                            "text": "You walk around the building, and see a pile of dirt with a shovel beside it. You decide to dig and after 5 days, your shovel hits an artefact."},
                        2: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You don't really see anything after a walk around the building. You decide to just leave it be."}
                    }
                },
                "away": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You walk away. There was probably nothing in that place anyway, besides rotting floorboards."}
                    }
                }
            }
        },
        11: {
            "event": "You explore the nearby wildlife sanctuary. Halfway through your trail, you notice a campsite full of people in indigenous clothing. \nPerhaps they have an artefact you could take?",
            "input": "Do you continue your relaxing walk or greet the tribesmen.. Or try stealing from them?",
            "choices": {
                "walk": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 20, "artefacts": 0,
                            "text": "You walk the rest of the trail and feel completely at peace. As if you have no rush at all.\n"
                                    "The sense of calmness extends your time by \033{10 days."},
                        2: {"money": 0, "time": -5, "artefacts": 0,
                            "text": "You forgot to read the length of the trail and walk a ridiculous distance.\nYou spend 5 days in various lodges along the trail until you finally get to the end."},
                        3: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You find the quickest way out of the trail and get back on your journey."},
                    }
                },
                "greet": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 1,
                            "text": "You spend 5 days living with the tribesmen, who tell you that they're living like their ancestors once did in this area.\nHappy with your stay, they send you off with a souvenir."},
                        2: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You greet the tribesmen and are treated to seemingly endless tales about the people who used to live in these lands.\nYou fall asleep out of boredom and get kicked out of the campsite for this."},
                        3: {"money": 0, "time": 15, "artefacts": 0,
                            "text": "You find the tribesmen worshipping a false idol and hastily do right by attacking their totem."
                                    "\nThe police are called on you but your righteous actions earn you the favour of your god. You get away and are granted 15 days time."
                            }
                    }
                },
                "steal": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You put on a friendly facade and when the moment is right, you sneakily take something without anyone seeing it.\nAfter leaving you realize it was just a worthless plastic replica."},
                        2: {"money": 0, "time": -10, "artefacts": 0,
                            "text": "You greet the campers and immediately are caught trying to steal a historic artefact. You explain your righteous mission, but to no avail.\n"
                                    "You spend 10 days in jail for attempted thievery."
                            },
                        3: {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": "You put on a friendly facade and when the moment is right, you sneakily take something without anyone seeing it."
                                    f"\nYou find the item to be too paltry of an offering and pawn it off for ${int(round(200 * money_modifier))}."},
                        4: {"money": 0, "time": 0, "artefacts": -1,
                            "text": "You put on a friendly facade and when the moment is right, you attempt to steal something from the campers but get caught. \n"
                                    "They end up taking one of your artefacts as punishment and exile you."},
                    }
                }
            }
        },
        12: {
            "event": "You come across a cockfighting ring. The host is beckoning passersby to come and bet on one of the roosters.\n"
                     "'C'mon up and bet on one of these fightin' birds! Paying 2:1 on winning bets!'",
            "input": f"Do you leave, bet ${int(round(200 * money_modifier))}, ${int(round(400 * money_modifier))} or try betting an artefact?",
            "choices": {
                f"{int(round(200 * money_modifier))}": {
                    "cost": {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(200 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(200 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    f"\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained ${int(round(400 * money_modifier))}!!"},
                        3: {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(200 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!"
                                    f"\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded ${int(round(200 * money_modifier))}."}
                    }
                },
                f"{int(round(400 * money_modifier))}": {
                    "cost": {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(400 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": int(round(800 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(400 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    f"\nThe birds are placed into the ring and the bell rings!!\n"
                                    f"\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    f"\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained ${int(round(800 * money_modifier))}!!"},
                        3: {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(400 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    f"\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded ${int(round(400 * money_modifier))}."}
                    }
                },
                "artefact": {
                    "cost": {"money": 0, "time": 0, "artefacts": 1},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You try to convince the referee to accept an artefact as a bet.\n"
                                    "'Tell you what, I'll take this and give you two treasures from my collection if you win!"
                                    "\nThe birds are placed into the ring and the bell rings!!"
                                    "\n\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": 0, "time": 0, "artefacts": 2,
                            "text": "You try to convince the referee to accept an artefact as a bet.\n"
                                    "'Tell you what, I'll take this and give you two treasures from my collection if you win!"
                                    "\nThe birds are placed into the ring and the bell rings!!"
                                    "\n\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    "\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation."
                                    "\nThe referee concedes and gives you 2 artefacts from his collection!!"},
                        3: {"money": 0, "time": 0, "artefacts": 1,
                            "text": "You try to convince the referee to accept an artefact as a bet."
                                    "\n'Tell you what, I'll take this and give you two treasures from my collection if you win!"
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw.\n"
                                    "You're given an artefact from his collection."}
                    }
                },
                "leave": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You decide to not gamble on chickens fighting."
                            }
                    }
                },
            }
        },
        13: {
            "event": "You trek around for a while and decide to set up camp. You fall asleep, but suddenly hear ungodly noises outside your tent.",
            "input": "Do you check on the noises, try sleeping through them or hide?",
            "choices": {
                "check": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You crawl out of your tent, and see a faint figure of a bear rushing away. You notice you've only lost a trail mix bag."},
                        2: {"money": 0, "time": 0, "artefacts": -1,
                            "text": "You crawl out of your tent, and see strangers looting your backpack. Before you manage to react, you see them running off with an artefact."},
                        3: {"money": -int(round(100 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You crawl out of your tent, and see strangers looting your backpack. Before you manage to react, you see them running off with ${int(round(100 * money_modifier))}."}
                    }
                },
                "sleep": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You come to the conclusion that it's just the wind. When you wake up, you notice that nothing has changed."},
                        2: {"money": 0, "time": 0, "artefacts": -1,
                            "text": "As you go back to sleep, a humanoid figure rushes into your tent and knocks you unconscious. When you wake up, you notice that an artefact has been stolen from you."},
                        3: {"money": 0, "time": 10, "artefacts": 0,
                            "text": "You go back to sleep and see a vision of your god. He praises your faith and rewards you with 10 days' extra time."}
                    }
                },
                "hide": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 0,
                            "text": "You get into a fetal position under a blanket and wait out the entire night. Morning comes and you feel exhausted. Your sleep debt costs you 5 days."},
                        2: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You quickly grab your belongings and hide under a pile of clothes. You hear someone stepping in and looking around. Thankfully, they don't notice you."}
                    }
                }
            }
        }
    }

def get_event(numero):
    choices = []
    mcosts = []
    tcosts = []
    acosts = []
    for choice in eventit[numero]["choices"]:
        choices.append(choice)
        mcosts.append(eventit[numero]["choices"][choice]['cost']['money'])
        tcosts.append(eventit[numero]["choices"][choice]['cost']['time'])
        acosts.append(eventit[numero]["choices"][choice]['cost']['artefacts'])

    return {
        "number" : numero,
        "text" : eventit[numero]["event"],
        "question" : eventit[numero]["input"],
        "choices" : choices,
        "money_costs" : mcosts,
        "time_costs" : tcosts,
        "artefacts_costs" : acosts
    }

def get_event_result(numero, choice):
    result = random.randint(1, len(eventit[numero]["choices"][choice]["results"]))

    return {
        "text" : eventit[numero]["choices"][choice]["results"][result]["text"],
        "money" : eventit[numero]["choices"][choice]["results"][result]["money"],
        "time" : eventit[numero]["choices"][choice]["results"][result]["time"],
        "artefacts" : eventit[numero]["choices"][choice]["results"][result]["artefacts"]
    }

