import random
import mysql.connector
from geopy import distance

money_modifier = 1.0

events = dict()

def get_all_events():
    global money_modifier
    global events
    events.clear()
    events = {
        1:{
            "event":f"You are given an investment opportunity on the street by a man in a trench coat. He says that by giving him \033[32m${int(round(100*money_modifier))}\033[0m you could make \033[32m${int(round(300*money_modifier))}\033[0m." ,
            "input":"Do you want to \033[35minvest\033[0m or \033[35mdecline\033[0m the opportunity?",
            "choices":{
                "invest":{
                    f"cost":{"money":int(round(100*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{f"money":int(round(300*money_modifier)),"time":0,"artefacts":0,"text":f"The opportunity actually paid out. You earned \033[32m${int(round(300*money_modifier))}.\033[0m"},
                        2:{"money":0,"time":0,"artefacts":0,"text":f"The opportunity was real... But you lost your \033[32m${int(round(100*money_modifier))}\033[0m."},
                        3:{"money":int(round(200*money_modifier)),"time":-10,"artefacts":0,"text":f"The man takes off running! You chase him and get your \033[32m${int(round(100*money_modifier))}\033[0m back. You also manage to snatch \033[32m${int(round(100*money_modifier))}\033[0m extra from him, but lose \033[34m10 days\033[0m in the process."}
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
            "event":f"You meet a witch, who says she can buy you time. Literally. She offers you \033[34m10 days\033[0m in exchange for \033[32m$200\033[0m.",
            "input":"Do you \033[35maccept\033[0m or \033[35mdecline\033[0m the offer?",
            "choices":{
                "accept":{
                    "cost":{f"money":200,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":15,"artefacts":0,"text":"You bought yourself some time. \033[34m10 days\033[0m to be exact."}
                    }
                },
                "decline":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-10,"artefacts":0,"text":"The witch gets mad at you declining her offer. She curses you, draining you of \033[34m10 days\033[0m."}
                    }
                }
            }
        },
        3:{
            "event":"You get lost, somehow.",
            "input":"Would you like to turn \033[35mleft\033[0m, \033[35mright\033[0m or continue \033[35mstraight\033[0m?",
            "choices":{
                "left":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-10,"artefacts":0,"text":"You get even more lost, losing \033[34m10 days\033[0m in the process. Eventually, you find your way back."}
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
                        1:{"money":50,"time":-10,"artefacts":0,"text":f"That wasn't the right way and you lose \033[34m10 days\033[0m. On a positive note, you find \033[32m${int(round(50*money_modifier))}\033[0m on the ground."},
                        2:{"money":100,"time":-10,"artefacts":0,"text":f"That wasn't the right way and you lose \033[34m10 days\033[0m. On a positive note, you find \033[32m${int(round(100*money_modifier))}\033[0m on the ground."},
                        3:{"money":200,"time":-10,"artefacts":0,"text":f"That wasn't the right way and you lose \033[34m10 days\033[0m. On a positive note, you find \033[32m${int(round(150*money_modifier))}\033[0m on the ground."}
                    }
                }
            }
        },
        4:{
            "event":"You stumble upon some sort of monument. There is a sign asking you to pray.",
            "input":"Do you pray on your \033[35mknees\033[0m, \033[35mstanding\033[0m up or do you \033[35mleave\033[0m?",
            "choices":{
                "knees":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"Something rumbles. A hatch opens underneath the monument, revealing an \033[33martefact\033[0m. The gods must be pleased."},
                        2:{"money":0,"time":-15,"artefacts":1,"text":"The monument shakes and reveals something under it. You take a peek and lose consciousness. You wake up \033[34m15 days\033[0m later and find an \033[33martefact\033[0m next to you."},
                        3:{"money":int(round(-100*money_modifier)),"time":-10,"artefacts":0,"text": f"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of \033[32m${int(round(100*money_modifier))}\033[0m and \033[34m10 days\033[0m."}

                    }
                },
                "standing":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(-100*money_modifier)),"time":-10,"artefacts":0,"text":f"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of \033[32m${int(round(100*money_modifier))}\033[0m and \033[34m10 days\033[0m."},
                        2:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"You feel a pleasant sensation. The gods must've been pleased with your praying. You notice you're carrying \033[32m${int(round(100*money_modifier))}\033[0m more than before."}
                    }
                },
                "leave":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"You decide to not accidentally disrespect the gods."},
                        2:{"money":0,"time":-5,"artefacts":0,"text":"Gearing to leave, you feel the earth starting to tremble. The gods weren't happy about you not honoring them. You black out and lose \033[34m5 days\033[0m."}
                    }
                }
            }
        },
        5:{
            "event":"You see a man in a suit strolling on the street. He seems to be giving money to some people he meets.",
            "input":'Do you greet him with a "\033[35mhello\033[0m", a "\033[35mgood evening\033[0m sir" or do you do \033[35mnothing\033[0m?',
            "choices":{
                "hello":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"The man replies and hands you \033[32m${int(round(100*money_modifier))}\033[0m."}
                    }
                },
                "good evening":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(200*money_modifier)),"time":0,"artefacts":0,"text":f"The man seems happy and hands you \033[32m${int(round(200*money_modifier))}\033[0m."},
                        2:{"money":int(round(300*money_modifier)),"time":0,"artefacts":0,"text":f"The man says how refreshing good manners are and hands you \033[32m${int(round(300*money_modifier))}\033[0m."}
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
            "event":f'You accidentally bump into a towering man on the street. You try to apologize, but the man seeks \033[32m{int(round(200*money_modifier))}\033[0m for "physical pain". Like he felt anything.',
            "input":f"Do you pay him the \033[32m$\033[0m\033[35m{int(round(200*money_modifier))}\033[0m he asks for, try to settle for \033[32m$\033[0m\033[35m{int(round(100*money_modifier))}\033[0m or \033[35mrefuse\033[0m to pay?",
            "choices":{
                f"{int(round(200*money_modifier))}":{
                    "cost":{"money":int(round(200*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":f"The man scoffs, relieving you of your \033[32m${int(round(200*money_modifier))}\033[0m. He gives you one last angry look and leaves."}
                    }
                },
                f"{int(round(100*money_modifier))}":{
                    "cost":{"money":int(round(100*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-5,"artefacts":0,"text":f"The man seems unimpressed. He looks you up and down, takes your \033[32m${int(round(100*money_modifier))}\033[0m and pushes you to the ground. You lose \033[34m 5 days\033[0m."}
                    }
                },
                "refuse":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(-200*money_modifier)),"time":0,"artefacts":0,"text":f"The man seems outright outraged. He quickly reaches into your pocket and takes \033[32m${int(round(200*money_modifier))}\033[0m."},
                        2:{"money":int(round(-150*money_modifier)),"time":0,"artefacts":0,"text":f"The man seems outright outraged. He quickly reaches into your pocket and takes \033[32m${int(round(150*money_modifier))}\033[0m."}
                    }
                }
            }
        },
        7:{
            "event":f'You notice a small well. A woman stands next to it, holding a cardboard sign. On it, she has written: "One coin = \033[32m${int(round(300*money_modifier))}\033[0m." Must be a wishing well.',
            "input":f"Do you want to \033[35mbuy\033[0m a coin for \033[32m${int(round(300*money_modifier))}\033[0m or \033[35mpass\033[0m on the opportunity?",
            "choices":{
                "buy":{
                    "cost":{"money":int(round(300*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(300*money_modifier)),"time":0,"artefacts":0,"text":f"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find \033[32m${int(round(300*money_modifier))}\033[0m."},
                        2:{"money":int(round(450*money_modifier)),"time":0,"artefacts":0,"text":f"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find \033[32m${int(round(450*money_modifier))}\033[0m."},
                        3:{"money":int(round(600*money_modifier)),"time":0,"artefacts":0,"text":f"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find \033[32m${int(round(600*money_modifier))}\033[0m."},
                        4:{"money":0,"time":20,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive \033[34m20 days\033[0m."},
                        5:{"money":0,"time":30,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive \033[34m30 days\033[0m."},
                        6:{"money":0,"time":40,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive \033[34m40 days\033[0m."}
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
            "event":"You hear sounds of metal hitting rock. Upon further inspection, you find a dig site, where a dozen men are swinging their pickaxes. \nOne of the men offers you their position for \033[34m20 days\033[0m.",
            "input":f"Do you \033[35maccept\033[0m it, \033[35mpay\033[0m the man \033[32m${int(round(200*money_modifier))}\033[0m to dig for you or \033[35mrefuse\033[0m?",
            "choices":{
                "accept":{
                    "cost":{"money":0,"time":20,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"You dig and dig. Finally, your pickaxe strikes something softer. You frantically wipe away some dirt, revealing a slightly battered \033[33martefact\033[0m."},
                        2:{"money":int(round(50*money_modifier)),"time":0,"artefacts":0,"text":f"You dig and dig. Finally, your pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around \033[32m${int(round(50*money_modifier))}\033[0m."}
                    }
                },
                "pay":{
                    "cost":{"money":int(round(200*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"The man digs and digs. Finally, his pickaxe strikes something softer. You rush to the scene, frantically wipe away some dirt and reveal a slightly battered \033[33martefact\033[0m."},
                        2:{"money":int(round(50*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around \033[32m${int(round(50*money_modifier))}\033[0m."},
                        3:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around \033[32m${int(round(100*money_modifier))}\033[0m."},
                        4:{"money":int(round(150*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around \033[32m${int(round(150*money_modifier))}\033[0m."}
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
            "input":f"Do you \033[35mrent\033[0m a room for the night for \033[32m${int(round(50*money_modifier))}\033[0m or try finding some makeshift \033[35mshelter\033[0m?",
            "choices":{
                "rent":{
                    "cost":{"money":int(round(50*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-10,"artefacts":0,"text":"You wait out the storm, losing \033[34m10 days\033[0m. At least you leave the motel unscathed."}
                    }
                },
                "shelter":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(-100*money_modifier)),"time":-15,"artefacts":0,"text":f"You find a small crevice and hole up inside. You're left unharmed by the storm, but lose \033[34m15 days\033[0m and \033[32m${int(round(100*money_modifier))}\033[0m for the arthritis you develop."},
                        2:{"money":0,"time":-20,"artefacts":0,"text":"You wander for a while and find an old, run-down cabin and hide there. Unfortunately, lightning strikes the unprotected shack, shocking you of \033[34m20 days\033[0m."},
                        3:{"money":0,"time":-15,"artefacts":0,"text":"You decide to lay low in an open area, covering yourself with leaves to keep the rain out. You wake up unscathed but freezing and lose \033[34m15 days\033[0m."}
                    }
                }
            }
        },
        10: {
            "event": "You see an old building in the distance. Walking closer to it, you become pretty sure it's abandoned.",
            "input": "Do you go \033[35minside\033[0m the building, check its \033[35msurroundings\033[0m it, or walk \033[35maway\033[0m?",
            "choices": {
                "inside": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 1,
                            "text": "The inside of building is very dark and you decide to use your phone's flashlight. On the ground, you spot an \033[33martefact\033[0m buried in rubble."},
                        2: {"money": 0, "time": -10, "artefacts": 1,
                            "text": "As you walk in, a trapdoor opens under your feet. The fall is harsh, and you wake up after \033[34m10 days\033[0m to the glimmering of an \033[33martefact\033[0m."},
                        3: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You walk around the house, but find nothing inside. It seems the building was abandoned for a reason."}
                    }
                },
                "surroundings": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 1,
                            "text": "You walk around the building, and see a pile of dirt with a shovel beside it. You decide to dig and after \033[34m5 days\033[0m, your shovel hits an \033[33martefact\033[0m."},
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
            "event": "You explore the nearby wildlife sanctuary. Halfway through your trail, you notice a campsite full of people in indigenous clothing. \nPerhaps they have an \033[33martefact\033[0m you could take?",
            "input": "Do you continue your relaxing \033[35mwalk\033[0m or \033[35mgreet\033[0m the tribesmen.. Or try \033[35msteal\033[0ming from them?",
            "choices": {
                "walk": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 20, "artefacts": 0,
                            "text": "You walk the rest of the trail and feel completely at peace. As if you have no rush at all.\n"
                                    "The sense of calmness extends your time by \033{34m10 days\033[0m."},
                        2: {"money": 0, "time": -5, "artefacts": 0,
                            "text": "You forgot to read the length of the trail and walk a ridiculous distance.\nYou spend \033[34m5\033[0m days in various lodges along the trail until you finally get to the end."},
                        3: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You find the quickest way out of the trail and get back on your journey."},
                    }
                },
                "greet": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 1,
                            "text": "You spend \033[34m5 days\033[0m living with the tribesmen, who tell you that they're living like their ancestors once did in this area.\nHappy with your stay, they send you off with a \033[33msouvenir\033[0m."},
                        2: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You greet the tribesmen and are treated to seemingly endless tales about the people who used to live in these lands.\nYou fall asleep out of boredom and get kicked out of the campsite for this."},
                        3: {"money": 0, "time": 15, "artefacts": 0,
                            "text": "You find the tribesmen worshipping a false idol and hastily do right by attacking their totem."
                                    "\nThe police are called on you but your righteous actions earn you the favour of your god. You get away and are granted \033[34m15 days\033[0m time."
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
                                    "You spend \033[34m10 days\033[0m in jail for attempted thievery."
                            },
                        3: {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": "You put on a friendly facade and when the moment is right, you sneakily take something without anyone seeing it."
                                    f"\nYou find the item to be too paltry of an offering and pawn it off for \033[32m${int(round(200 * money_modifier))}\033[0m."},
                        4: {"money": 0, "time": 0, "artefacts": -1,
                            "text": "You put on a friendly facade and when the moment is right, you attempt to steal something from the campers but get caught. \n"
                                    "They end up taking one of your \033[33martefacts\033[0m as punishment and exile you."},
                    }
                }
            }
        },
        12: {
            "event": "You come across a cockfighting ring. The host is beckoning passersby to come and bet on one of the roosters.\n"
                     "\033[36m'C'mon up and bet on one of these fightin' birds! Paying 2:1 on winning bets!'\033[0m",
            "input": f"Do you \033[35mleave\033[0m, bet $\033[35m{int(round(200 * money_modifier))}\033[0m, $\033[35m{int(round(400 * money_modifier))}\033[0m or try betting an \033[35martefact\033[0m?",
            "choices": {
                f"{int(round(200 * money_modifier))}": {
                    "cost": {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(200 * money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(200 * money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    f"\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained \033[32m${int(round(400 * money_modifier))}\033[0m!!"},
                        3: {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(200 * money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!"
                                    f"\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded \033[32m${int(round(200 * money_modifier))}\033[0m."}
                    }
                },
                f"{int(round(400 * money_modifier))}": {
                    "cost": {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(400 * money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": int(round(800 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(400 * money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    f"\nThe birds are placed into the ring and the bell rings!!\n"
                                    f"\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    f"\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained \033[32m${int(round(800 * money_modifier))}\033[0m!!"},
                        3: {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(400 * money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    f"\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded \033[32m${int(round(400 * money_modifier))}\033[0m."}
                    }
                },
                "artefact": {
                    "cost": {"money": 0, "time": 0, "artefacts": 1},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet.\n"
                                    "\033[36m'Tell you what, I'll take this and give you \033[33mtwo treasures\033[36m from my collection if you win!\033[0m"
                                    "\nThe birds are placed into the ring and the bell rings!!"
                                    "\n\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": 0, "time": 0, "artefacts": 2,
                            "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet.\n"
                                    "\033[36m'Tell you what, I'll take this and give you \033[33mtwo treasures\033[36m from my collection if you win!\033[0m"
                                    "\nThe birds are placed into the ring and the bell rings!!"
                                    "\n\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    "\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation."
                                    "\nThe referee concedes and gives you \033[33m2 artefacts\033[0m from his collection!!"},
                        3: {"money": 0, "time": 0, "artefacts": 1,
                            "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet."
                                    "\n\033[36m'Tell you what, I'll take this and give you \033[33mtwo treasures\033[36m from my collection if you win!\033[0m"
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw.\n"
                                    "You're given \033[33man artefact\033[0m from his collection."}
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
            "input": "Do you \033[35mcheck\033[0m on the noises, try \033[35msleep\033[0ming through them or \033[35mhide\033[0m?",
            "choices": {
                "check": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You crawl out of your tent, and see a faint figure of a bear rushing away. You notice you've only lost a trail mix bag."},
                        2: {"money": 0, "time": 0, "artefacts": -1,
                            "text": "You crawl out of your tent, and see strangers looting your backpack. Before you manage to react, you see them running off with an \033[33martefact\033[0m."},
                        3: {"money": -int(round(100 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You crawl out of your tent, and see strangers looting your backpack. Before you manage to react, you see them running off with \033[32m${int(round(100 * money_modifier))}\033[0m."}
                    }
                },
                "sleep": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You come to the conclusion that it's just the wind. When you wake up, you notice that nothing has changed."},
                        2: {"money": 0, "time": 0, "artefacts": -1,
                            "text": "As you go back to sleep, a humanoid figure rushes into your tent and knocks you unconscious. When you wake up, you notice that an \033[33martefact\033[0m has been stolen from you."},
                        3: {"money": 0, "time": 10, "artefacts": 0,
                            "text": "You go back to sleep and see a vision of your god. He praises your faith and rewards you with \033[34m10 days\033[0m' extra time."}
                    }
                },
                "hide": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 0,
                            "text": "You get into a fetal position under a blanket and wait out the entire night. Morning comes and you feel exhausted. Your sleep debt costs you \33[34m5 days\033[0m."},
                        2: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You quickly grab your belongings and hide under a pile of clothes. You hear someone stepping in and looking around. Thankfully, they don't notice you."}
                    }
                }
            }
        }
    }


    # todo !!!Kun pelaajalle lisätään rahaa, käytä \033[32m${int(round(100*money_modifier))}\033[0m TEKSTIN SISÄLLÄ -> CHOICES, TEKSTISSÄ, TEE F STRINGEJÄ !!
    # todo KÄYTÄ int(round(100*money_modifier)) (EI HAKASULKUJA, TULEE SETTI) TEKSTIN ULKOPUOLELLA -> RESULTS KOHDASSA RAHAN LISÄYS

    # Eventin lisäys pohja:
    # JÄRJESTYSLUKY:{
    #        "event":, !!!EVENTIN TEKSTI
    #        "input":, !!!MITÄ EVENTTI KYSYY (ESIM ACCEPT (A) OR DECLINE (D)
    #        "choices":{
    #            "VAIHTOEHTO (ESIM A TAI D)":{
    #                "cost":{"money":,"time":,"artefacts":}, !!!MITÄ VAIHTOEHTO MAKSAA (AINA POSITIIVINEN)
    #                "results":{
    #                    JÄRJESTYSLUKU, ALKAA AINA 1:{"money":,"time":,"artefacts":,"text":}, !!!EKAT KOLME ANTAA PELAAJALLE RESURSSIA (NEG/POS), "TEXT" ON MITÄ PRINTATAAN
    #               }
    #            },
    #        }
    #    },

    # HUOM! VÄRIKOODIT:
    # Raha (vihreä): \033[32m$X\033[0m
    # Aika (sininen): \033[34mX DAYS\033[0m
    # Artefaktit (keltainen): \033[33mX ARTEFACT(S)\033[0m
    # Vaihtoehdot (magenta): \033[35mTEKSTI\033[0m
    # Paikat (punainen): \033[31mTEKSTI\033[0m
    # Matka (syaani) \033[36mTEKSTI\033[0m

get_all_events()
money = 3000
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
achieved = []
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
converted_amount = 0
convert_index = 0
achievements = {
    "distance":[
        (10000,"\033[1mFirst Steps\033[0m for travelling \033[36m10000 km\033[0m",50),
        (30000,"\033[1mBeginner Traveler\033[0m for travelling \033[36m30000 km\033[0m",75),
        (60000,"\033[1mIntermediate Traveler\033[0m for travelling \033[36m60000 km\033[0m",100),
        (80000,"\033[1mAdvanced Traveler\033[0m for travelling \033[36m80000 km\033[0m",150),
        (125000,"\033[1mMaster Traveler\033[0m for travelling \033[36m125000 km\033[0m",300),
        (175000,"\033[1mBusiness Class\033[0m for travelling \033[175000 km\033[0m",400),
        (200000,"\033[1mFirst Class\033[0m for travelling \033[36m200000 km\033[0m",500),
        (250000,"\033[1mApostle\033[0m for travelling \033[36m250000 km\033[0m",500),
        (9999999999999999999999,"error",999999999999)
    ],
    "countries":[
        (3,"\033[1mSightseer\033[0m for visiting 4 countries",75),
        (6,"\033[1mTourist\033[0m for visiting 6 countries",100),
        (10,"\033[1mRegular\033[0m for visiting 10 countries",150),
        (13,"\033[1mDual Citizenship\033[0m for visiting 13 countries",200),
        (18, "\033[1mMissionary\033[0m for visiting 18 countries", 350),
        (9999999999999999999999,"error",9999999999)
    ],
    "money":[
        (300,"\033[1mIntern\033[0m for earning \033[32m$300\033[0m",50),
        (600,"\033[1mHard Worker\033[0m for earning \033[32m$600\033[0m",100),
        (1200,"\033[1mBusinessman\033[0m for earning \033[32m$1200\033[0m",150),
        (2000,"\033[1mCEO\033[0m for earning \033[32m$2000\033[0m",200),
        (3000, "\033[1mTithe\033[0m for earning \033[32m$3000\033[0m", 300),
        (4000, "\033[1mPeter's Pence\033[0m for earning \033[32m$4000\033[0m", 300),
        (99999999999999999999999999,"error",9999999999999999)
    ],
    "artefacts":[
        (1,"\033[1mExplorer\033[0m for finding your first artefact",50),
        (3,"\033[1mTreasure Hunter\033[0m for finding 3 artefacts",100),
        (8,"\033[1mCulture Preserver\033[0m for finding 8 artefacts",150),
        (12,"\033[1mIndiana Jones\033[0m for finding 12 artefacts",200),
        (9999999999999999999999,"error",9999999999999)
    ],
    "events":[
        (3,"\033[1mRisk-taker\033[0m for completing 2 events",75),
        (6,"\033[1mLucky Guy\033[0m for completing 6 events",125),
        (10,"\033[1mTrue Adventurer\033[0m for completing 10 events",150),
        (16,"\033[1mFortuna\033[0m for completing 16 events",300),
        (999999999999999999999,"error",9999999999999)
    ],
    "convert":[
        (1,"\033[1mBeliever\033[0m for converting heretics once",100),
        (2,"\033[1mFaithful\033[0m for converting heretics 2 times",150),
        (4,"\033[1mDevotee\033[0m for converting heretics 4 times",200),
        (7,"\033[1mChosen One\033[0m for converting heretics 7 times",300),
        (10,"\033[1mMandate from Heaven\033[0m for converting heretics 10 times",400),
        (999999999999999999999,"error",99999999)
    ]
}

kysymykset = {
    "NA": {
        1:{"kysymys":"What is the highest mountain in North America? \033[35m_____  ________\033[0m",
           "vastaus":"mount mckinley"},
        2:{"kysymys":"Who was the first president of the United States? \033[35m______  __________\033[0m",
           "vastaus":"george washington"},
        3:{"kysymys":"Which country colonized Canada before it became independent? The \033[35m______  _______\033[0m",
           "vastaus":"united kingdom"},
        4:{"kysymys":"How many states are there in the United States of America? \033[35m__\033[0m",
           "vastaus":"50"},
        5:{"kysymys":"What is the largest city in North America by population? \033[35m______  ____\033[0m",
           "vastaus":"mexico city"}
    },
    "SA": {
        1:{"kysymys":"What is the largest country in South America by area? \033[35m_______\033[0m",
           "vastaus":"brazil"},
        2:{"kysymys":"The tango dance originated in which South American country? \033[35m_________\033[0m",
           "vastaus":"argentina"},
        3:{"kysymys":"Which South American country has coastlines on both the Pacific Ocean and the Caribbean Sea? \033[35m________\033[0m",
           "vastaus":"colombia"},
        4:{"kysymys":"In which city is the famous statue 'Christ the Redeemer' located? \033[35m___  __  ______\033[0m",
           "vastaus":"rio de janeiro"},
        5:{"kysymys":"What is the longest river in South America? The \033[35m______  _____\033[0m",
           "vastaus":"amazon river"}
    },
    "EU": {
        1:{"kysymys":"Which European country is famous for inventing pizza and pasta? \033[35m_____\033[0m",
           "vastaus":"italy"},
        2:{"kysymys":"What is the smallest country in Europe, by both population and area? \033[35m_______  ____\033[0m",
           "vastaus":"vatican city"},
        3:{"kysymys":"What is the longest river in Europe? The \033[35m_____  _____\033[0m",
           "vastaus":"volga river"},
        4:{"kysymys":"What mountain range separates Europe and Asia? The \033[35m____  ________\033[0m",
           "vastaus":"ural mountains"},
        5:{"kysymys":"Which year did the Soviet Union collapse? \033[35m____\033[0m",
           "vastaus":"1991"}
    },
    "AS": {
        1:{"kysymys":"What is the highest mountain in Asia? \033[35m_____  _______\033[0m",
           "vastaus":"mount everest"},
        2:{"kysymys":"In which country is the longest river in Asia located? \033[35m_____\033[0m",
           "vastaus":"china"},
        3:{"kysymys":"Who was the founder of the Mongol Empire? \033[35m_______  ____\033[0m",
           "vastaus":"genghis khan"},
        4:{"kysymys":"Which city is the most populous in Asia? \033[35m_____\033[0m",
           "vastaus":"tokyo"},
        5:{"kysymys":"In which country can you ride the world’s fastest train, the Maglev? \033[35m_____\033[0m",
           "vastaus":"china"}
    },
    "OC": {
        1:{"kysymys":"What is the largest city in Australia by population? \033[35m______\033[0m",
           "vastaus":"sydney"},
        2:{"kysymys":"Which reef system, visible from space, lies off the coast of Queensland? The \033[35m_____  _______  ____\033[0m",
           "vastaus":"great barrier reef"},
        3:{"kysymys":"What is the national animal of Australia? The \033[35m________\033[0m",
           "vastaus":"kangaroo"},
        4:{"kysymys":"How many states are there in Australia? \033[35m_\033[0m",
           "vastaus":"6"},
        5:{"kysymys":"What is the capital city of Australia? \033[35m_______\033[0m",
           "vastaus":"canberra"}
    },
    "AF": {
        1:{"kysymys":"What is the longest river in Africa? The \033[35m____  _____\033[0m",
           "vastaus":"nile river"},
        2:{"kysymys":"What is the largest desert in Africa? The \033[35m______  ______\033[0m",
           "vastaus":"sahara desert"},
        3:{"kysymys":"What is the only African country that was never colonized? \033[35m_______\033[0m",
           "vastaus":"ethiopia"},
        4:{"kysymys":"What is the most populous country in Africa? \033[35m_______\033[0m",
           "vastaus":"nigeria"},
        5:{"kysymys":"What is the highest mountain in Africa? \033[35m_____  __________\033[0m",
           "vastaus":"mount kilimanjaro"}
    },
    "AN": {
        1:{"kysymys":"Which continent is larger: Antarctica or Europe? \033[35m__________\033[0m",
           "vastaus":"antarctica"},
        2:{"kysymys":"Which ocean surrounds Antarctica? The \033[35m________  ______\033[0m",
           "vastaus":"southern ocean"},
        3:{"kysymys":"In which century was Antarctica discovered? The \033[35m__th  _______\033[0m",
           "vastaus":"19th century"},
        4:{"kysymys":"How many cities are there in Antarctica? \033[35m_\033[0m",
           "vastaus":"0"},
        5:{"kysymys":"Which type of whale, the largest animal on Earth, can be found in Antarctic waters? \033[35m____  _____\033[0m",
           "vastaus":"blue whale"}
    }
}
# Sanakirja, jossa jokainen mantereen lyhennys vastaa useaa artifaktin nimeä
artefact_names = \
    {
# Europe
"EU" : ("Ivory Figurine", "Celtic Sword", "Gold Bracelet", "Ceramic Pot", "Iron Axehead", "Roman Gold Coin", "Ceramic Figurine", "Jade Pendant", "Golden Chalice", "Book of Hours", "Pewter Silverware"),

# Oceania
"OC" : ("Aboriginal Boomerang", "Didgeridoo", "Hielaman Shield", "Sea Snail Rattle", "Message Stick", "Quartzite Grinding Stone", "Tasmanian Devil Necklace", "Decorated Pearl Shell"),

# Africa
"AF" : ("Ancient Spearhead", "Egyptian Adze", "Rosetta Stone", "Nok Terracotta", "Ivory Statue", "Chair of Power", "Songye Mask", "Ooni Brass Head"),

# South America
"SA" : ("Tobacco Pipe", "Aztec Sword", "Olmec Celt", "Gold Poporo Vessel", "Gold Figure", "Ceramic Incense Burner", "Ceramic Sherd", "Death Whistle"),

# North America
"NA" : ("Flint Arrowhead", "Feathered Headdress", "Sacred Wooden Mask", "Clovis Point Spearhead", "Hammerstone", "Rhyolite Arrowhead", "Gold Pendant"),

# Asia
"AS" : ("Jade Sculpture", "Bronze Vessel", "Gold Mask", "Bronze Bird", "Zhang Jade Blade", "Pottery Pig", "Bronze Spearhead", "Ivory Chest", "Decorated Plate", "Ming Dynasty Painting", "Wooden Figures"),

#
"AN" : ("Carved Bone", "Rusted Anchor")

}
for eve in events:
    uncompleted_events.append(eve)
conn = mysql.connector.connect(
    host='localhost',
    port=3306,
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
    global converted_amount
    global convert_index

    money = 3000
    time = 365
    artefacts = list()
    cont = "AN"
    conts = ["AF", "AN", "AS", "EU", "NA", "OC", "SA"]
    airport = "Ancient Chamber"
    country = "Antarctica"
    size = "ritual_site"
    achieved = []
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
    converted_amount = 0
    convert_index = 0

    temp = ""
    print("This game is color-coded. Every time you're presented with a choice, your typeable actions are marked with \033[35mmagenta\033[0m.")
    while temp != "understood":
        temp = input("\033[35mUnderstood\033[0m?\n> ").strip().lower()
    print("----")
    temp = ""
    print("Reading the introduction is recommended for a first-time playthrough.")
    while temp != "read" and temp != "play" and temp != "scores":
        temp = input("Would you like to \033[35mread\033[0m the introduction, check past \033[35mscores\033[0m or start \033[35mplay\033[0ming?\n> ").strip().lower()
    print("----")
    if temp == "read":
        print(f"You belong in a cult dead-set on waking up an ancient god.\n"
              "After centuries of hard work, the moment is finally at hand.\n"
              "You arrive in an ancient chamber located in Antarctica. The chamber smells of sulfur and debris on the ground seems to move on its own.\n"
              "In the middle of the chamber lies a circle made of lit candles. You step in, and start performing a ritual.\n"
              "You feel the air rising as a fading projection of your god appears in front of you. You hear a deep voice.\n"
              "The voice commands you to bring him six artefacts - one from each of the other continents - to finish the ritual.\n"
              "After you have found and collected an artefact from every other continent, you shall return to Antarctica.\n"
              f"You are given limited time to complete your quest - otherwise the ritual fails.\n"
              "In addition, to ensure your obedience, a spirit is sent after you. You feel as if you don't want to make contact with it.\n"
              "You leave the chamber as a waning voice behind you asks you to hurry.\n----")
        print("Important things to note:\n"
              "- You only have a limited number of actions on each airport, and if you don't depart as your last action, the spirit will catch you.\n"          
              "- Working gives you money, but costs you time.\n"
              "- Exploring consists of randomized events, which can both cost and reward money, time or artefacts.\n"
              "- Converting heretics is a fighting minigame. Winning nets you money. The actions are as follows:\n"
              "  STRIKE (#) decreases the selected enemy's stamina, but has a chance to miss.\n"
              "  HEAL (#) heals you based on your current stamina, and has limited uses.\n"
              "  GUARD decreases the amount of stamina you lose from enemy attacks.\n"
              "- In the auction house you can either buy or sell artefacts.\n"
              "- Each action consumes \033[34m5 days\033[0m in addition to other costs.\n"
              "- Traveling to another continent costs more.\n"
              "- Airport size determines the cost of travel and affects some rewards.\n"    
              "----")
    elif temp == "scores":
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
            for scoretemp in range(len(scorelist)):
                print(f"Game {scorelist[scoretemp][0]}: {scorelist[scoretemp][1]}")
        else:
            print(f"No games played in the past.")
        print("----")

def print_all():
    print(money, time, cont, country, size, airport, artefacts, uncompleted_events, latlong, total_distance, visited_countries)

def add_artefact(count):
    global cont
    global artefacts_earned
    if count is None:
        count = 1

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
            ctemp=""
            if ct == "SA":
                ctemp = "South America"
            elif ct == "EU":
                ctemp = "Europe"
            elif ct == "NA":
                ctemp = "North America"
            elif ct == "OC":
                ctemp = "Oceania"
            elif ct == "AS":
                ctemp = "Asia"
            elif ct == "AN":
                ctemp = "Antarctica"
            elif ct == "AF":
                ctemp = "Africa"
            # Onko pelaajalla vain 1 valitun mantereen aarre?
            if len(sm) < 2:
                while True:
                    p = input(
                        f"That's your only artefact from \033[31m{ctemp}\033[0m. Are you sure you want to \033[35msell\033[0m it, or would you rather \033[35mback\033[0m out?\n> ").strip().lower()
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
        pass

def list_artefacts(selling):
    if len(artefacts) > 0:
        ctemp=""
        for a in artefacts:
            if a.continent == "SA":
                ctemp = "South America"
            elif a.continent == "EU":
                ctemp = "Europe"
            elif a.continent == "NA":
                ctemp = "North America"
            elif a.continent == "OC":
                ctemp = "Oceania"
            elif a.continent == "AS":
                ctemp = "Asia"
            elif a.continent == "AN":
                ctemp = "Antarctica"
            elif a.continent == "AF":
                ctemp = "Africa"
            if selling:
                print(f"\033[35m{artefacts.index(a)+1}\033[0m: \033[33m{a.name}\033[0m from \033[31m{ctemp}\033[0m, \033[32m${a.value}\033[0m")
            else:
                print(f"{artefacts.index(a) + 1}: \033[33m{a.name}\033[0m from \033[31m{ctemp}\033[0m, \033[32m${a.value}\033[0m")
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
    # chicken
    #event_id = 12
    # tribe
    #event_id = 11

    # vvvv kommentoi testatessa vvvv
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

    # ota eventin mahdolliset lopputulokset
    results = list()
    for i in range(1, len(events[event_id]["choices"][choice]["results"])+1):
        results.append(events[event_id]["choices"][choice]["results"][i])

    # sekoita niiden lista
    random.shuffle(results)
    # ei warningia
    outcome = results[0]
    # mene kaikkien läpi
    for i in range(0,len(results)):
        outcome = results[i]
        # ota ensimmäinen, joka ei vie pelaajalta liikaa artefakteja!!
        if not len(artefacts) + outcome["artefacts"] < 0:
            break


    #Tapahtuman lopputulos
    print(outcome["text"],f"\n----")
    money += outcome["money"]
    if outcome["money"] > 0:
        money_earned += outcome["money"]
    if money < 0:
        money = 0
    time += outcome["time"]
    if time < 0:
        time = 0


    # lisää / poista aarre
    if outcome["artefacts"] > 0:
        add_artefact(outcome["artefacts"])
    elif outcome["artefacts"] < 0:
        for i in range(0, outcome["artefacts"]):
            remove_artefact()

def fight(amount):
    hp = 10
    if amount > 1:
        hp += amount * 5
    heals = amount // 2
    guarding = False
    fight_over = False
    global money, converted_amount, time
    # hp, dmg, dodge, speed
    types = {
    "Bulwark":[16, 7, 1, 3],
    "Warden":[10, 4, 2.5, 2],
    "Vessel":[7, 2, 4, 0],
    "Zealot":[12, 3, 3, 1]
    }
    enemies = []

    enemies_in_fight = {}
    for i in range(amount):
        enemies_in_fight[i] = {
            "hp":0,
            "dmg":0,
            "ddg":0,
            "spd":0
        }

    if amount == 1:
        print(f"You find a singular robed man and prepare to convert him, no matter the cost.")
    else:
        print(f"You find a group of {amount} robed men and prepare to convert them, no matter the cost.")

    print("----")

    for enemy in range(amount):
        enemies.append(random.choice(["Bulwark", "Vessel", "Warden", "Zealot"]))
        enemies_in_fight[enemy]["hp"] = types[enemies[enemy]][0]
        enemies_in_fight[enemy]["dmg"] = types[enemies[enemy]][1]
        enemies_in_fight[enemy]["ddg"] = types[enemies[enemy]][2]
        enemies_in_fight[enemy]["spd"] = types[enemies[enemy]][3]

    changing_amount = amount
    enemylist = []
    for i in range(amount):
        enemylist.append(i)

    while not fight_over:
        for enemy in range(amount):
            if enemies_in_fight[enemy]["hp"] == 0:
                temp = 'unconscious'
            elif enemies_in_fight[enemy]["spd"] == 0:
                temp = 'attacking'
            else:
                temp = f'charging for {enemies_in_fight[enemy]["spd"]} turns'
            if enemy < enemylist[len(enemylist) - 1]:
                if enemies_in_fight[enemy]["hp"] != 0:
                    print(f"Enemy \033[35m{enemy+1}\033[0m: "+f"\033[1m{enemies[enemy]}\033[0m"+f' \033[33m{enemies_in_fight[enemy]["hp"]}\033[0m'+ f' (\033[36m{temp}\33[0m)',end=" | ")
            else:
                if enemies_in_fight[enemy]["hp"] != 0:
                    print(f"Enemy \033[35m{enemy + 1}\033[0m: " + f"\033[1m{enemies[enemy]}\033[0m"+ f' \033[33m{enemies_in_fight[enemy]["hp"]}\033[0m'+ f' (\033[36m{temp}\33[0m)\n----')

        print(f"\033[33m{hp}\033[0m | \033[35mSTRIKE\033[0m (\033[35m#\033[0m)\033[0m | \033[35mHEAL\033[0m ({heals}) | \33[35mGUARD\033[0m | \033[35mESCAPE\033[0m")
        action = ""
        tempactionlist = ["guard", "escape"]
        for i in range(amount):
            if enemies_in_fight[i]["hp"] != 0:
                tempactionlist.append(f"strike {i+1}")
        if heals > 0:
            tempactionlist.append("heal")
        while action not in tempactionlist:
            action = input("> ").strip().lower()
        print("----")
        if action == "escape":
            if random.random() <= 0.3:
                if hp == 20:
                    print("You manage to escape the quarrel unscathed.")
                    print("----")
                else:
                    print("You manage to escape the beating.")
                    print("----")
            else:
                print("You try scrambling your way out but fail.")
                print("----")
        elif "strike" in action:
            enemynumber = int(action[7])-1
            print(f"You try striking the \033[1m{enemies[enemynumber]}\033[0m in his {random.choice(['head','chest','right arm','left arm','stomach'])}.",end=" ")
            if enemies_in_fight[enemynumber]["ddg"] >= random.uniform(0, 10):
                print(f"The \033[1m{enemies[enemynumber]}\033[0m dodges the blow and you miss.")
            else:
                if random.random() <= 0.3:
                    dmg = int(round(random.randint(3,6)*1.5))
                    print(f"The blow lands critically, dealing \033[31m{dmg}\033[0m damage.")
                    enemies_in_fight[enemynumber]["hp"] = enemies_in_fight[enemynumber]["hp"] - dmg
                    if enemies_in_fight[enemynumber]["hp"] <= 0:
                        print("----")
                        enemies_in_fight[enemynumber]["hp"] = 0
                        print(f"The \033[1m{enemies[enemynumber]}\033[0m loses all his stamina and decides to convert.")
                        changing_amount -= 1
                        enemylist.remove(enemynumber)
                else:
                    dmg = int(round(random.randint(3,6)))
                    print(f"The blow lands, dealing \033[31m{dmg}\033[0m damage.")
                    enemies_in_fight[enemynumber]["hp"] = enemies_in_fight[enemynumber]["hp"] - dmg
                    if enemies_in_fight[enemynumber]["hp"] <= 0:
                        print("----")
                        enemies_in_fight[enemynumber]["hp"] = 0
                        print(f"The \033[1m{enemies[enemynumber]}\033[0m loses all his stamina and decides to convert.")
                        changing_amount -= 1
                        enemylist.remove(enemynumber)
            print("----")
            if changing_amount == 0:
                print(f"Having converted all the heretics, your god blesses you with \033[32m${amount*150}\033[0m.")
                money += amount*150
                converted_amount += 1
                print("----")
                fight_over = True
        elif action == "heal":
            heal_amount = random.randint(8,13) - hp
            if heal_amount < 1:
                heal_amount = 1
            print(f"You reach for a red potion and drink from it. You gain \033[33m{heal_amount} stamina\033[0m.")
            hp += heal_amount
            heals -= 1
            print("----")
        elif action == "guard":
            print("You enter a meditative state and feel your skin harden.")
            print("----")
            guarding = True

        for enemy in range(amount):
            if enemies_in_fight[enemy]["hp"] != 0:
                if enemies_in_fight[enemy]["spd"] == 0:
                    if guarding:
                        print(f"The \033[1m{enemies[enemy]}\033[0m {random.choice(['smacks', 'hits', 'strikes', 'punches', 'kicks'])} you in your {random.choice(['head', 'chest', 'right arm', 'left arm', 'stomach'])}, dealing \033[31m{enemies_in_fight[enemy]['dmg'] // 3}\033[0m damage.")
                        hp -= enemies_in_fight[enemy]['dmg'] // 3
                    else:
                        print(f"The \033[1m{enemies[enemy]}\033[0m {random.choice(['smacks', 'hits', 'strikes', 'punches', 'kicks'])} you in your {random.choice(['head','chest','right arm','left arm','stomach'])}, dealing \033[31m{enemies_in_fight[enemy]['dmg']}\033[0m damage.")
                        hp -= enemies_in_fight[enemy]['dmg']
                    print("----")
                    enemies_in_fight[enemy]["spd"] = types[enemies[enemy]][3]
                else:
                    enemies_in_fight[enemy]["spd"] = enemies_in_fight[enemy]["spd"] - 1

        if hp <= 0:
            print("You lose all your stamina and pass out for \033[34m10 days\033[0m. The heretics win and leave the scene.")
            time -= 10
            fight_over = True
        guarding = False

def check_inventory():
    temp = ["your water bottle", "some snacks", "your phone", "a picture of mommy", "an amulet", "a dreamcatcher", "your lucky rock collection"]
    temp1 = random.choice(temp)
    global visited_countries
    print(f"You open your backpack and reach for {temp1}.")
    print("----")
    ctemp=""
    if cont == "SA":
        ctemp = "South America"
    elif cont == "EU":
        ctemp = "Europe"
    elif cont == "NA":
        ctemp = "North America"
    elif cont == "OC":
        ctemp = "Oceania"
    elif cont == "AS":
        ctemp = "Asia"
    elif cont == "AN":
        ctemp = "Antarctica"
    elif cont == "AF":
        ctemp = "Africa"
    print(f"You are currently in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{ctemp}\033[0m.")
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
    ctemp=""
    if cont == "SA":
        ctemp = "South America"
    elif cont == "EU":
        ctemp = "Europe"
    elif cont == "NA":
        ctemp = "North America"
    elif cont == "OC":
        ctemp = "Oceania"
    elif cont == "AS":
        ctemp = "Asia"
    elif cont == "AN":
        ctemp = "Antarctica"
    elif cont == "AF":
        ctemp = "Africa"
    print(
        f"You are currently in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{ctemp}\033[0m. Other available continents are",
        end=" ")

    other_continents = list()
    for c in conts:
        other_continents.append(c)

    other_continents.remove(cont)

    for i in range(len(other_continents)):
        ctemp=""
        if other_continents[i] == "SA":
            ctemp = "\033[35mS\033[0m\033[31mouth\033[0m \033[35mA\033[0m\033[31mmerica\033[0m"
        elif other_continents[i] == "EU":
            ctemp = "\033[35mEu\033[0m\033[31mrope\033[0m"
        elif other_continents[i] == "NA":
            ctemp = "\033[35mN\033[0m\033[31morth\033[0m \033[35mA\033[0m\033[31mmerica\033[0m"
        elif other_continents[i] == "OC":
            ctemp = "\033[35mOc\033[0m\033[31meania\033[0m"
        elif other_continents[i] == "AS":
            ctemp = "\033[35mAs\033[0m\033[31mia\033[0m"
        elif other_continents[i] == "AN":
            ctemp = "\033[35mAn\033[0m\033[31mtarctica\033[0m"
        elif other_continents[i] == "AF":
            ctemp = "\033[35mAf\033[0m\033[31mrica\033[0m"
        if i < len(other_continents) - 2:
            print(f"{ctemp}", end=", ")
        elif i < len(other_continents) - 1:
            print(f"{ctemp}", end=" and ")
        else:
            print(f"{ctemp}.")
    if cont != "AN":
        ctemp = ""
        if cont == "SA":
            ctemp = "South America"
        elif cont == "EU":
            ctemp = "Europe"
        elif cont == "NA":
            ctemp = "North America"
        elif cont == "OC":
            ctemp = "Oceania"
        elif cont == "AS":
            ctemp = "Asia"
        elif cont == "AN":
            ctemp = "Antarctica"
        elif cont == "AF":
            ctemp = "Africa"
        while cont_temp != "stay" or cont_temp not in other_continents:
            cont_temp = input(f"You can either \033[35mstay\033[0m in \033[31m{ctemp}\033[0m or choose a new continent.\n> ").strip().upper()
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
        mapping = {
            "SA": "South America",
            "EU": "Europe",
            "NA": "North America",
            "OC": "Oceania",
            "AS": "Asia",
            "AN": "Antarctica",
            "AF": "Africa"
        }

        lanka = [f"\033[31m{mapping.get(c, 'Unknown')}\033[0m" for c in continents]

        if len(lanka) > 1:
            text = ", ".join(lanka[:-1]) + " and " + lanka[-1] + "."
        else:
            text = lanka[0] + "."

        print(text)
        return False
    else:
        print("----")
        print(f"Having collected the necessary artefacts, you prepare to head to the \033[31mAncient Chamber\033[0m.")
        print("----")
        return True

def winning():
    global game_over
    global money
    global time
    global total_distance
    global achieved

    score = 0

    score += money
    score += total_distance // 60
    score += time * 10

    color_temp = [f"\033[31m{c}\033[0m" for c in visited_countries]
    text = ", ".join(color_temp[:-1]) + " and " + color_temp[-1]
    print(
        "You arrive at the \033[31mAncient Chamber\033[0m well in time.\n"
        "It's finally time to complete the ritual. You reach for your backpack and pull out the artefacts you have collected.\n"
        "Beside each candle in the circle, there is a small slot. You place the artefacts in the slots, one by one, and feel everything start to gradually shake.\n"
        "The chamber fills with fog, and you see something blurry in front of you. Or rather, someone.\n"
        "A figure steps through the fog, the chamber echoing with his footsteps. Your god stands before you, fully materialized.\n"
        '"Congratulations", the voice says, "you have done me proud." The divine being touches you, and you ascend to a higher state of being.'
    )
    print("----")
    print("You got the following achievements:")
    for ach in achieved:
        print(ach)
    print("----")
    print(
        "Along your journey you visited " + text + f", and travelled a total of \033[36m{total_distance} km\033[0m, rewarding you", (total_distance // 60), "points.\n"
        f"You had \033[32m${money}\033[0m rewarding you", money, f"points and \033[34m{time} days\033[0m rewarding you", (time * 10), "points.\n"
        f"Your total score was {score}."
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (score) VALUES (%s)", (score,))
    conn.commit()
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
    global money_modifier

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
    ctemp = ""
    if cont == "SA":
        ctemp = "South America"
    elif cont == "EU":
        ctemp = "Europe"
    elif cont == "NA":
        ctemp = "North America"
    elif cont == "OC":
        ctemp = "Oceania"
    elif cont == "AS":
        ctemp = "Asia"
    elif cont == "AN":
        ctemp = "Antarctica"
    elif cont == "AF":
        ctemp = "Africa"
    print(f'Available airports in \033[31m{ctemp}\033[0m:')

    for i in range(len(airport_results)):
        if new_cont:
            if money >= int(costs[i] + 200):
                latlong_temp = (airport_results[i]["latitude"], airport_results[i]["longitude"])
                print(f'\033[35m{i+1}\033[0m: \033[31m{airport_results[i]["name"]}\033[0m, a {airport_results[i]["type"].replace("_"," ")} in \033[31m{airport_results[i]["country"]}\033[0m - \033[36m{int(round(distance.distance(latlong,latlong_temp).km))} km\033[0m - \033[32m${int(costs[i] + 200)}\033[0m, \033[34m10 days\033[0m')
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
        _ = cursor.fetchall()
        cursor.close()
        if row is None:
            print(f"Warning: coordinates for {airport!r} not found; distance not updated.")
        else:
            dest = (row[0], row[1])  # (lat, lon)
            total_distance += int(round(distance.distance(latlong, dest).km))
            latlong = dest

        if new_cont:
            money -= int(costs[answer_temp-1] + 200)
            time -= 10
        else:
            money -= int(costs[answer_temp-1])
            time -= 5
        print("----")

        # Tässä rahat säädetään
        # Money modifier on event_list skriptissä
        if size == "large_airport":
            money_modifier = 1.5
        elif size == "medium_airport":
            money_modifier = 1.2
        else:
            money_modifier = 1
        # RIP suorituskyky
        get_all_events()
        ctemp = ""
        if cont == "SA":
            ctemp = "South America"
        elif cont == "EU":
            ctemp = "Europe"
        elif cont == "NA":
            ctemp = "North America"
        elif cont == "OC":
            ctemp = "Oceania"
        elif cont == "AS":
            ctemp = "Asia"
        elif cont == "AN":
            ctemp = "Antarctica"
        elif cont == "AF":
            ctemp = "Africa"
        print(f"You arrive in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{ctemp}\033[0m.")
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
        print(f"The man's face lights up. You answered correctly. He hands you \033[32m${int(round(100 * money_modifier))}\033[0m and tells you to subscribe to his channel, whatever that means.")
        money += int(round(100 * money_modifier))
        money_earned += int(round(100 * money_modifier))
    else:
        print("----")
        print("The man frowns slightly. It doesn't seem like your answer was correct. He thanks you for your time and starts looking for a new contestant. You think the game was rigged.")
    print("----")

def quiz(continent):
    print(f"Upon your arrival, a young man approaches you. He informs you that he hosts a game show. By answering a question correctly, you win \033[32m${int(round(100 * money_modifier))}\033[0m.")
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

    i = random.randint(1,10)
    if cont != "AN":
        if i <= 4:
            quiz(cont)

    # muokattava lista
    all_actions = ["work", "explore", "auction", "check", "depart", "convert"]
    achievement()
    while remaining_actions > 0:
        # Nollaa joka kierroksen alussa
        action = ""

        # Tässä työrahan randomisaatio
        max_money = int(round(200 * money_modifier))
        min_money = int(round(100 * money_modifier))

        # Eka vuoro
        if remaining_actions == 3:
            print(
                f"You've just arrived, and thus have {remaining_actions} actions remaining on this airport before the spirit catches you.")
        # toka ja kolmas
        else:
            print(f"You have {remaining_actions} actions remaining on this airport before the spirit catches you.")

        while action not in all_actions:
            action = input(
                "Would you like to either \033[35mcheck\033[0m your standing, \033[35mwork\033[0m, \033[35mexplore\033[0m, \033[35mconvert\033[0m heretics, visit the \033[35mauction\033[0m house or \033[35mdepart\033[0m?\n> ")

        print("----")
        if action == "work":
            work = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher",
                    "cucumber quality inspector", "tree doctor", "farmer's assistant",
                    "professional supermarket greeter"]
            moneygain = random.randint(min_money, max_money)
            print(
                f"You decide to work as a {random.choice(work)}. You earn \033[32m${moneygain}\033[0m, but lose \033[34m10 days\033[0m.")
            money += moneygain
            money_earned += moneygain
            time -= 15
            print("----")
            achievement()
        elif action == "explore":
            time -= 5
            event()
            achievement()
        elif action == "auction":
            time -= 5
            shop()
            achievement()
        elif action == "check":
            check_inventory()
            # reppuun katsominen ei vie paljon aikaa
            remaining_actions += 1
            achievement()
        elif action == "convert":
            fight(random.randint(1,4))
            achievement()
            time -= 5

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
                ctemp = ""
                if cont == "SA":
                    ctemp = "South America"
                elif cont == "EU":
                    ctemp = "Europe"
                elif cont == "NA":
                    ctemp = "North America"
                elif cont == "OC":
                    ctemp = "Oceania"
                elif cont == "AS":
                    ctemp = "Asia"
                elif cont == "AN":
                    ctemp = "Antarctica"
                elif cont == "AF":
                    ctemp = "Africa"
                print(
                    f"Your journey ended in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{ctemp}\033[0m.")
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
    global money
    global achieved
    global converted_amount
    global convert_index

    if len(visited_countries) >= achievements["countries"][countries_index][0]:
        print("You've achieved",achievements["countries"][countries_index][1],f"and earned \033[32m${achievements['countries'][countries_index][2]}\033[0m.")
        print("----")
        money += achievements["countries"][countries_index][2]
        achieved.append(achievements["countries"][countries_index][1])
        countries_index += 1
    if money_earned >= achievements["money"][money_index][0]:
        print("You've achieved",achievements["money"][money_index][1],f"and earned \033[32m${achievements['money'][money_index][2]}\033[0m.")
        print("----")
        money += achievements["money"][money_index][2]
        achieved.append(achievements["money"][money_index][1])
        money_index += 1
    if total_distance >= achievements["distance"][distance_index][0]:
        print("You've achieved",achievements["distance"][distance_index][1],f"and earned \033[32m${achievements['distance'][distance_index][2]}\033[0m.")
        print("----")
        money += achievements["distance"][distance_index][2]
        achieved.append(achievements["distance"][distance_index][1])
        distance_index += 1
    if artefacts_earned >= achievements["artefacts"][artefacts_index][0]:
        print("You've achieved",achievements["artefacts"][artefacts_index][1],f"and earned \033[32m${achievements['artefacts'][artefacts_index][2]}\033[0m.")
        print("----")
        money += achievements["artefacts"][artefacts_index][2]
        achieved.append(achievements["artefacts"][artefacts_index][1])
        artefacts_index += 1
    if events_completed >= achievements["events"][events_index][0]:
        print("You've achieved",achievements["events"][events_index][1],f"and earned \033[32m${achievements['events'][events_index][2]}\033[0m.")
        print("----")
        money += achievements["events"][events_index][2]
        achieved.append(achievements["events"][events_index][1])
        events_index += 1
    if converted_amount >= achievements["convert"][convert_index][0]:
        print("You've achieved", achievements["convert"][convert_index][1],f"and earned \033[32m${achievements['convert'][convert_index][2]}\033[0m.")
        print("----")
        money += achievements["convert"][convert_index][2]
        achieved.append(achievements["convert"][convert_index][1])
        convert_index += 1

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