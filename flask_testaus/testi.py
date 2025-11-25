
money_modifier = 1
eventit = {
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

def events(numero):
    return f'{eventit[numero]["event"]}'