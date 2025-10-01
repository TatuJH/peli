events = {
    1:{
        "event":"You are given an investment opportunity on the street by a man in a trench coat. He says that by giving him \033[32m$100\033[0m you could make \033[32m$300\033[0m." ,
        "input":"Do you want to \033[35minvest\033[0m or \033[35mdecline\033[0m the opportunity?",
        "choices":{
            "invest":{
                "cost":{"money":100,"time":0,"artefacts":0},
                "results":{
                    1:{"money":300,"time":0,"artefacts":0,"text":"The opportunity actually paid out. You earned \033[32m$300.\033[0m"},
                    2:{"money":0,"time":0,"artefacts":0,"text":"The opportunity was real... But you lost your \033[32m$100\033[0m."},
                    3:{"money":200,"time":-5,"artefacts":0,"text":"The man takes off running! You chase him and get your \033[32m$100\033[0m back. You also manage to snatch \033[32m$100\033[0m extra from him, but lose \033[34m5 days\033[0m in the process."}
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
        "event":"You meet a witch, who says she can buy you time. Literally. She offers you \033[34m15 days\033[0m in exchange for \033[32m$100\033[0m.",
        "input":"Do you \033[35maccept\033[0m or \033[35mdecline\033[0m the offer?",
        "choices":{
            "accept":{
                "cost":{"money":100,"time":0,"artefacts":0},
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
                    1:{"money":50,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m. On a positive note, you find \033[32m$50\033[0m on the ground."},
                    2:{"money":100,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m. On a positive note, you find \033[32m$100\033[0m on the ground."},
                    3:{"money":200,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m. On a positive note, you find \033[32m$150\033[0m on the ground."}
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
                    1:{"money":-100,"time":-10,"artefacts":0,"text":"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of \033[32m$100\033[0m and \033[34m10 days\033[0m."}
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
                    1:{"money":100,"time":0,"artefacts":0,"text":"The man replies and hands you \033[32m$100\033[0m."}
                }
            },
            "good evening":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":200,"time":0,"artefacts":0,"text":"The man seems happy and hands you \033[32m$200\033[0m."},
                    2:{"money":300,"time":0,"artefacts":0,"text":"The man says how refreshing good manners are and hands you \033[32m$300\033[0m."}
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
        "event":'You accidentally bump into a towering man on the street. You try to apologize, but the man seeks \033[32m$200\033[0m in compensation for "physical pain". Like he felt anything.',
        "input":"Do you pay him the \033[32m$\033[0m\033[35m200\033[0m he asks for, try to settle for \033[32m$\033[0m\033[35m100\033[0m or \033[35mrefuse\033[0m to pay?",
        "choices":{
            "200":{
                "cost":{"money":200,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":0,"artefacts":0,"text":"The man scoffs, relieving you of your \033[32m$200\033[0m. He gives you one last angry look and leaves."}
                }
            },
            "100":{
                "cost":{"money":100,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":-5,"artefacts":0,"text":"The man seems unimpressed. He looks you up and down, takes your \033[32m$100\033[0m and pushes you to the ground. You lose \033[34m 5 days\033[0m."}
                }
            },
            "refuse":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":-200,"time":0,"artefacts":0,"text":"The man seems outright outraged. He quickly reaches into your pocket and takes \033[32m$200\033[0m."},
                    2:{"money":-150,"time":0,"artefacts":0,"text":"The man seems outright outraged. He quickly reaches into your pocket and takes \033[32m$150\033[0m."}
                }
            }
        }
    },
    7:{
        "event":'You notice a small well. A woman stands next to it, holding a cardboard sign. On it, she has written: "One coin = \033[32m$300\033[0m." Must be a wishing well.',
        "input":"Do you want to \033[35mbuy\033[0m a coin for \033[32m$300\033[0m or \033[35mpass\033[0m on the opportunity?",
        "choices":{
            "buy":{
                "cost":{"money":300,"time":0,"artefacts":0},
                "results":{
                    1:{"money":300,"time":0,"artefacts":0,"text":"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find \033[32m$300\033[0m."},
                    2:{"money":450,"time":0,"artefacts":0,"text":"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find \033[32m$450\033[0m."},
                    3:{"money":600,"time":0,"artefacts":0,"text":"You toss the coin into the well and a bag of money falls from the sky. You're not sure how, but you also don't really care. Inside it you find \033[32m$600\033[0m."},
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
        "input":"Do you \033[35maccept\033[0m it, \033[35mpay\033[0m the man \033[32m$200\033[0m to dig for you or \033[35mrefuse\033[0m?",
        "choices":{
            "accept":{
                "cost":{"money":0,"time":20,"artefacts":0},
                "results":{
                    1:{"money":0,"time":0,"artefacts":1,"text":"You dig and dig. Finally, your pickaxe strikes something softer. You frantically wipe away some dirt, revealing a slightly battered \033[33martefact\033[0m."},
                    2:{"money":50,"time":0,"artefacts":0,"text":"You dig and dig. Finally, your pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around \033[32m$50\033[0m."}
                }
            },
            "pay":{
                "cost":{"money":200,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":0,"artefacts":1,"text":"The man digs and digs. Finally, his pickaxe strikes something softer. You rush to the scene, frantically wipe away some dirt and reveal a slightly battered \033[33martefact\033[0m."},
                    2:{"money":50,"time":0,"artefacts":0,"text":"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around \033[32m$50\033[0m."},
                    3:{"money":100,"time":0,"artefacts":0,"text":"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around \033[32m$100\033[0m."},
                    4:{"money":150,"time":0,"artefacts":0,"text":"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around \033[32m$150\033[0m."}
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
        "input":"Do you \033[35mrent\033[0m a room for the night for \033[32m$50\033[0m or try finding some makeshift \033[35mshelter\033[0m?",
        "choices":{
            "rent":{
                "cost":{"money":50,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":-10,"artefacts":0,"text":"You wait out the storm, losing \033[34m10 days\033[0m. At least you leave the motel unscathed."}
                }
            },
            "shelter":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":-100,"time":-15,"artefacts":0,"text":"You find a small crevice and hole up inside. You're left unharmed by the storm, but lose \033[34m15 days\033[0m and \033[32m$100\033[0m for the arthritis you develop."},
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
        "event": "You explore the nearby wildlife sanctuary. Midway through your trail, you notice a campsite full of people in indigenous clothing. \nPerhaps they have an \033[33martefact\033[0m you could take?",
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
                    3: {"money": 200, "time": 0, "artefacts": 0,
                        "text": "You put on a friendly facade and when the moment is right, you sneakily take something without anyone seeing it."
                                "\nAfter examining your new treasure, you find it to be too paltry of an offering and pawn it off for \033[32m$200\033[0m."},
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
        "input": "Do you \033[35mleave\033[0m, bet $\033[35m200\033[0m, $\033[35m400\033[0m or try betting an \033[35martefact\033[0m?",
        "choices": {
            "200": {
                "cost": {"money": 200, "time": 0, "artefacts": 0},
                "results": {
                    1: {"money": 0, "time": 0, "artefacts": 0,
                        "text": "You bet \033[32m$200\033[0m on one of the roosters and join the crowd to watch the battle."
                                "\nThe birds are placed into the ring and the bell rings!!\n"
                                "\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                    2: {"money": 400, "time": 0, "artefacts": 0,
                        "text": "You bet \033[32m$200\033[0m on one of the roosters and join the crowd to watch the battle."
                                "\nThe birds are placed into the ring and the bell rings!!\n"
                                "\nThe referee tries egging on the roosters to engage in battle, but fails."
                                "\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained \033[32m$400\033[0m!!"},
                    3: {"money": 200, "time": 0, "artefacts": 0,
                                "text": "You bet \033[32m$200\033[0m on one of the roosters and join the crowd to watch the battle."
                                "\nThe birds are placed into the ring and the bell rings!!"
                                "\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded \033[32m$200\033[0m."}
                }
            },
            "400": {
                "cost": {"money": 400, "time": 0, "artefacts": 0},
                "results": {
                    1: {"money": 0, "time": 0, "artefacts": 0,
                        "text": "You bet \033[32m$400\033[0m on one of the roosters and join the crowd to watch the battle."
                                "\nThe birds are placed into the ring and the bell rings!!\n"
                                "\nAfter a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                    2: {"money": 800, "time": 0, "artefacts": 0,
                        "text": "You bet \033[32m$400\033[0m on one of the roosters and join the crowd to watch the battle."
                                "\nThe birds are placed into the ring and the bell rings!!\n"
                                "\nThe referee tries egging on the roosters to engage in battle, but fails."
                                "\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained \033[32m$800\033[0m!!"},
                    3: {"money": 400, "time": 0, "artefacts": 0,
                                "text": "You bet \033[32m$400\033[0m on one of the roosters and join the crowd to watch the battle."
                                "\nThe birds are placed into the ring and the bell rings!!\n"
                                "\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded \033[32m$400\033[0m."}
                }
            },
            "artefact": {
                "cost": {"money": 0, "time": 0, "artefacts": 1},
                "results": {
                    1: {"money": 0, "time": 0, "artefacts": 0,
                        "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet.\n"
                                "He takes it and agrees to give two \033[33mnational treasures\033[0m from his collection, should you win.\n"
                                "\nThe birds are placed into the ring and the bell rings!!\n"
                                "After a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                    2: {"money": 0, "time": 0, "artefacts": 2,
                        "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet.\n"
                                "He takes it and agrees to give two \033[33mnational treasures\033[0m from his collection, should you win."
                                "\n\nThe birds are placed into the ring and the bell rings!!"
                                "\nThe referee tries egging on the roosters to engage in battle, but fails."
                                "\nAfter a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation.\n"
                                "The referee concedes and gives you \033[33m2 artefacts\033[0m from his collection!!"},
                    3: {"money": 0, "time": 0, "artefacts": 1,
                        "text": "You try to convince the referee to accept \033[33man artefact\033[0m as a bet.\n"
                                "He takes it and agrees to give two \033[33mnational treasures\033[0m from his collection, should you win.\n"
                                "\nThe birds are placed into the ring and the bell rings!!\n"
                                "\nThe roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw.\n"
                                "You're refunded \033[33man artefact\033[0m from his collection."}
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

#Eventin lisäys pohja:
#JÄRJESTYSLUKY:{
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

#HUOM! VÄRIKOODIT:
#Raha (vihreä): \033[32m$X\033[0m
#Aika (sininen): \033[34mX DAYS\033[0m
#Artefaktit (keltainen): \033[33mX ARTEFACT(S)\033[0m
#Vaihtoehdot (magenta): \033[35mTEKSTI\033[0m
#Paikat (punainen): \033[31mTEKSTI\033[0m
#Matka (syaani) \033[36mTEKSTI\033[0m