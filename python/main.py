import random
import mysql.connector
from artefacts import *
from trivia_list import *
from geopy import distance
from achievements import *

money_modifier = 1.0

events = dict()

def get_all_events():
    global money_modifier
    global events
    events.clear()
    print(f"money mod on nyt event jutussa {money_modifier}")
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
                        3:{"money":int(round(200*money_modifier)),"time":-5,"artefacts":0,"text":f"The man takes off running! You chase him and get your \033[32m${int(round(100*money_modifier))}\033[0m back. You also manage to snatch \033[32m${int(round(100*money_modifier))}\033[0m extra from him, but lose \033[34m5 days\033[0m in the process."}
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
            "event":f"You meet a witch, who says she can buy you time. Literally. She offers you \033[34m15 days\033[0m in exchange for \033[32m${int(round(100*money_modifier))}\033[0m.",
            "input":"Do you \033[35maccept\033[0m or \033[35mdecline\033[0m the offer?",
            "choices":{
                "accept":{
                    "cost":{f"money":int(round(100*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":15,"artefacts":0,"text":"You bought yourself some time. \033[34m15 days\033[0m to be exact."}
                    }
                },
                "decline":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-5,"artefacts":0,"text":"The witch gets mad at you declining her offer. She curses you, draining you of \033[34m5 days\033[0m."}
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
                        1:{"money":0,"time":0,"artefacts":1,"text":"Something rumbles. A hatch opens underneath the monument, revealing an \033[33martefact\033[0m. The gods must be pleased."}
                    }
                },
                "standing":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(-100*money_modifier)),"time":-10,"artefacts":0,"text":f"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of \033[32m${int(round(100*money_modifier))}\033[0m and \033[34m10 days\033[0m."}
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
            "event":f'You accidentally bump into a towering man on the street. You try to apologize, but the man seeks \033[32m{int(round(200*money_modifier))}\033[0m in compensation for "physical pain". Like he felt anything.',
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
                        4:{"money":0,"time":30,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive \033[34m30 days\033[0m."},
                        5:{"money":0,"time":45,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive \033[34m45 days\033[0m."},
                        6:{"money":0,"time":60,"artefacts":0,"text":"You toss the coin into the well and feel a surge of energy coursing through you. You receive \033[34m60 days\033[0m."}
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
            "event":"You hear sounds of metal hitting rock. Upon further inspection, you find a dig site, where a dozen men are swinging their pickaxes. One of the men offers you their position for \033[34m20 days\033[0m.",
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
        10:{
            "event":"You see an old building in the distance. Walking closer to it, you become pretty sure it's abandoned.",
            "input":"Do you go \033[35minside\033[0m the building, check its \033[35msurroundings\033[0m it, or walk \033[35maway\033[0m?",
            "choices":{
                "inside":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"The inside of building is very dark and you decide to use your phone's flashlight. On the ground, you spot an \033[33martefact\033[0m buried in rubble."},
                        2:{"money":0,"time":-10,"artefacts":1,"text":"As you walk in, a trapdoor opens under your feet. The fall is harsh, and you wake up after \033[34m10 days\033[0m to the glimmering of an \033[33martefact\033[0m."},
                        3:{"money":0,"time":0,"artefacts":0,"text":"You walk around the house, but find nothing inside. It seems the building was abandoned for a reason."}
                    }
                },
                "surroundings":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-5,"artefacts":1,"text":"You walk around the building, and see a pile of dirt with a shovel beside it. You decide to dig and after \033[34m5 days\033[0m, your shovel hits an \033[33martefact\033[0m."},
                        2:{"money":0,"time":0,"artefacts":0,"text":"You don't really see anything after a walk around the building. You decide to just leave it be."}
                    }
                },
                "away":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"You walk away. There was probably nothing in that place anyway, besides rotting floorboards."}
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
                            "text": "You walk the rest of the trail and feel completely at peace. As if you have \033[34mno rush at all.\033[0m"},
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
                        3: {"money": int(round(200*money_modifier)), "time": 0, "artefacts": 0,
                            "text": "You put on a friendly facade and when the moment is right, you sneakily take something without anyone seeing it."
                                    f"\nAfter examining your new treasure, you find it to be too paltry of an offering and pawn it off for \033[32m${int(round(200*money_modifier))}\033[0m."},
                        4: {"money": 0, "time": 0, "artefacts": -1,
                            "text": "You put on a friendly facade and when the moment is right, you attempt to steal something from the campers but get caught. \n"
                                    "They end up taking one of your \033[33martefacts\033[0m as punishment and exile you."},
                    }
                }
            }
        },
        12: {
            "event": "You come across a cockfighting ring. The host is beckoning passersby to come and bet on one of the roosters.\n"
                     "\033[36m'C'mon up and bet on one of them there fine game birds! Paying 2:1 on winning bets!'\033[0m",
            "input": f"Do you \033[35mleave\033[0m, bet $\033[35m{int(round(200*money_modifier))}\033[0m, $\033[35m{int(round(400*money_modifier))}\033[0m or try betting an \033[35martefact\033[0m?",
            "choices": {
                "200": {
                    "cost": {"money": int(round(200*money_modifier)), "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(200*money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": int(round(400*money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(200*money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    f"\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained \033[32m${int(round(400*money_modifier))}\033[0m!!"},
                        3: {"money": int(round(200*money_modifier)), "time": 0, "artefacts": 0,
                                    "text": f"You bet \033[32m${int(round(200*money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!"
                                    f"\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded \033[32m${int(round(200*money_modifier))}\033[0m."}
                    }
                },
                "400": {
                    "cost": {"money": int(round(400*money_modifier)), "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(400*money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": int(round(800*money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet \033[32m${int(round(400*money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    f"\nThe birds are placed into the ring and the bell rings!!\n"
                                    f"\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    f"\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained \033[32m${int(round(800*money_modifier))}\033[0m!!"},
                        3: {"money": int(round(400*money_modifier)), "time": 0, "artefacts": 0,
                                    "text": f"You bet \033[32m${int(round(400*money_modifier))}\033[0m on one of the roosters and join the crowd to watch the battle."
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    f"\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded \033[32m${int(round(400*money_modifier))}\033[0m."}
                    }
                },
                "artefact": {
                    "cost": {"money": 0, "time": 0, "artefacts": 1},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet.\n"
                                    "\033[36m'Tell you what, I'll take this and give you \033[33mtwo treasures\033[36m from my collection if you win!\033[0m\n"
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "After a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": 0, "time": 0, "artefacts": 2,
                            "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet.\n"
                                    "\033[36m'Tell you what, I'll take this and give you \033[33mtwo treasures\033[36m from my collection if you win!\033[0m\n"
                                    "\n\nThe birds are placed into the ring and the bell rings!!"
                                    "\nThe referee tries egging on the roosters to engage in battle, but fails."
                                    "\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation.\n"
                                    "The referee concedes and gives you \033[33m2 artefacts\033[0m from his collection!!"},
                        3: {"money": 0, "time": 0, "artefacts": 1,
                            "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet.\n"
                                    "\033[36m'Tell you what, I'll take this and give you \033[33mtwo treasures\033[36m from my collection if you win!\033[0m\n"
                                    "\nThe birds are placed into the ring and the bell rings!!\n"
                                    "\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw.\n"
                                    "You're given \033[33man artefact\033[0m from his collection."}
                    }
                },
                "leave": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You decide to not gamble on chickens fighting.\n"
                            }
                        }
                    },
                }
            },

    }

get_all_events()
money = 5000
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

for eve in events:
    uncompleted_events.append(eve)


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

    money = 100000
    time = 365
    artefacts = list()
    cont = "AN"
    conts = ["AF", "AN", "AS", "EU", "NA", "OC", "SA"]
    airport = "Ancient Chamber"
    country = "Antarctica"
    size = "ritual_site"
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
              f"You are given \033[34m{int(time)}\033[0m days\033[0m to complete your quest - otherwise the ritual fails.\n"
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

def print_all():
    print(money, time, cont, country, size, airport, artefacts, uncompleted_events, latlong, total_distance, visited_countries)

def add_artefact(count):
    global cont
    global artefacts_earned

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
        print("Good thing you had no artefacts to lose!")

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
    global money_earned
    global artefacts_earned
    global events_completed
    event_id = random.choice(uncompleted_events)
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
    if events[event_id]["choices"][choice]["cost"]["artefacts"] > 0:
        remove_artefact(events[event_id]["choices"][choice]["cost"]["artefacts"])

    outcome = random.randint(1, len(events[event_id]["choices"][choice]["results"]))

    #Tapahtuman lopputulos
    print(events[event_id]["choices"][choice]["results"][outcome]["text"],f"\n----")
    money += events[event_id]["choices"][choice]["results"][outcome]["money"]
    if events[event_id]["choices"][choice]["results"][outcome]["money"] > 0:
        money_earned += events[event_id]["choices"][choice]["results"][outcome]["money"]
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
    print("----")

def choose_continent():
    global cont
    cont_temp = ""
    ant_temp = False
    new_cont = False
    print(
        f"You are currently in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m. Other available continents are",
        end=" ")
    for i in range(len(conts)):
        if cont != conts[i]:
            if i < len(conts) - 2:
                print(f"\033[35m{conts[i]}\033[0m", end=", ")
            elif i < len(conts) - 1:
                print(f"\033[35m{conts[i]}\033[0m", end=" and ")
            else:
                print(f"\033[35m{conts[i]}\033[0m.")
    if cont != "AN":
        while cont_temp != "stay" or cont_temp not in conts:
            cont_temp = input(f"You can either \033[35mstay\033[0m in \033[31m{cont}\033[0m or choose a new continent.\n> ").strip().upper()
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

def winning():
    global game_over
    global money
    global time
    global total_distance

    score = 0

    score += money
    score += total_distance
    score += time

    color_temp = [f"\033[31m{c}\033[0m" for c in visited_countries]
    text = ", ".join(color_temp[:-1]) + " and " + color_temp[-1]
    print(
        "You have arrived at the Ancient Chamber in Antarctica before your time ran out. Well done!\n"
        "Now, it's finally time to complete the ritual, with the \033[33martefacts\033[0m you have collected.\n"
        "Placing the \033[33martefacts\033[0m on the ground in a circle, everything starts to shake.\n"
        "The chamber fills with fog, and you see something blurry in front of you, could it be? It must be!\n"
        "A figure steps through the fog and you recognize it, it's god himself. You have done it!!!"
    )
    print("----")
    print(
        "Along your jorney you visited " + text + f", and travelled a total of \033[36m{total_distance} km\033[0m rewarding you", (total_distance // 60), "points\n"
        f"You had \033[32m${money}\033[0m rewarding you", money, f"points and \033[34m{time} days\033[0m rewarding you", (time * 10), "points.\n"
        "Your total score was", score
    )

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
        cursor.close()
        if row is None:
            print(f"Warning: coordinates for {airport!r} not found; distance not updated.")
        else:
            dest = (row[0], row[1])  # (lat, lon)
            total_distance += int(round(distance.distance(latlong, dest).km))
            latlong = dest

        if new_cont:
            money -= int(costs[answer_temp-1] * 1.5)
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


        print(f"You arrive in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m.")
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
    global money_earned

    achievement()
    if cont != "AN":
        quiz(cont)

    # muokattava lista
    all_actions = ["work", "explore", "auction", "check", "depart"]
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
                "Would you like to either \033[35mcheck\033[0m your stats, \033[35mwork\033[0m, \033[35mexplore\033[0m, visit the \033[35mauction\033[0m house or \033[35mdepart\033[0m?\n> ")

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
            time -= 10
            print("----")
            achievement()
        elif action == "explore":
            event()
            achievement()
        elif action == "auction":
            shop()
            achievement()
        elif action == "check":
            check_inventory()
            # reppuun katsominen ei vie paljon aikaa
            remaining_actions += 1
            achievement()

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
                print(
                    f"Your journey ended in \033[31m{airport}\033[0m in \033[31m{country}\033[0m, \033[31m{cont}\033[0m.")
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

    if len(visited_countries) >= achievements["countries"][countries_index][0]:
        print("You've achieved",achievements["countries"][countries_index][1])
        print("----")
        countries_index += 1
    if money_earned >= achievements["money"][money_index][0]:
        print("You've achieved",achievements["money"][money_index][1])
        print("----")
        money_index += 1
    if total_distance >= achievements["distance"][distance_index][0]:
        print("You've achieved",achievements["distance"][distance_index][1])
        print("----")
        distance_index += 1
    if artefacts_earned >= achievements["artefacts"][artefacts_index][0]:
        print("You've achieved",achievements["artefacts"][artefacts_index][1])
        print("----")
        artefacts_index += 1
    if events_completed >= achievements["events"][events_index][0]:
        print("You've achieved",achievements["events"][events_index][1])
        print("----")
        events_index += 1

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
    all_artefacts_test()
    #jos haluu testaa kaikkien artefaktien kanssa, esim voittoa varten
    choose_continent()

    while not game_over:
        check_gameover(False)
        airport_actions()

game_loop()