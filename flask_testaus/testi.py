import mysql.connector
import random
import data

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame',
    user='tatu',
    password='Tietokannat1',
    autocommit=True
)

cursor = conn.cursor()

class Artefact:
    def __init__(self, nimi, arvo, manner):
        self.name = nimi
        self.value = arvo
        self.continent = manner

uncompleted_events = []

def getallevents(money_modifier):
    return {
        1:{
            "event":f"You are given an investment opportunity on the street by a man in a trench coat. He says that by giving him ${int(round(100*money_modifier))} you could make ${int(round(300*money_modifier))}." ,
            "input":"Do you want to invest or decline the opportunity?",
            "choices":{
                "Invest":{
                    f"cost":{"money":int(round(100*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{f"money":int(round(300*money_modifier)),"time":0,"artefacts":0,"text":f"The opportunity actually paid out. You earned ${int(round(300*money_modifier))}."},
                        2:{"money":0,"time":0,"artefacts":0,"text":f"The opportunity was real... But you lost your ${int(round(100*money_modifier))}."},
                        3:{"money":int(round(200*money_modifier)),"time":-10,"artefacts":0,"text":f"The man takes off running! You chase him and get your ${int(round(100*money_modifier))} back. You also manage to snatch ${int(round(100*money_modifier))} extra from him, but lose 10 days in the process."}
                    }
                },
                "Decline":{
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
                "Accept":{
                    "cost":{f"money":200,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":15,"artefacts":0,"text":"You bought yourself some time. 10 days to be exact."}
                    }
                },
                "Decline":{
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
                "Left":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-10,"artefacts":0,"text":"You get even more lost, losing 10 days in the process. Eventually, you find your way back."}
                    }
                },
                "Right":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"As you turn right, you notice that the airport is literally just there. Talk about luck."}
                    }
                },
                "Straight":{
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
                "Knees":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"Something rumbles. A hatch opens underneath the monument, revealing an artefact. The gods must be pleased."},
                        2:{"money":0,"time":-15,"artefacts":1,"text":"The monument shakes and reveals something under it. You take a peek and lose consciousness. You wake up 15 days later and find an artefact next to you."},
                        3:{"money":int(round(-100*money_modifier)),"time":-10,"artefacts":0,"text": f"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of ${int(round(100*money_modifier))} and 10 days."}

                    }
                },
                "Standing":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(-100*money_modifier)),"time":-10,"artefacts":0,"text":f"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of ${int(round(100*money_modifier))} and 10 days."},
                        2:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"You feel a pleasant sensation. The gods must've been pleased with your praying. You notice you're carrying ${int(round(100*money_modifier))} more than before."}
                    }
                },
                "Leave":{
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
                "Hello":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"The man replies and hands you ${int(round(100*money_modifier))}."}
                    }
                },
                "Good evening":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":int(round(200*money_modifier)),"time":0,"artefacts":0,"text":f"The man seems happy and hands you ${int(round(200*money_modifier))}."},
                        2:{"money":int(round(300*money_modifier)),"time":0,"artefacts":0,"text":f"The man says how refreshing good manners are and hands you ${int(round(300*money_modifier))}."}
                    }
                },
                "Nothing":{
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
                "Refuse":{
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
                "Buy":{
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
                "Pass":{
                    "cost":{"money":0,"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":0,"text":"You? Superstitious? Like any normal person, you decide to save your money."}
                    }
                }
            }
        },
        8:{
            "event":"You hear sounds of metal hitting rock. Upon further inspection, you find a dig site, where a dozen men are swinging their pickaxes. One of the men offers you their position for 20 days.",
            "input":f"Do you accept it, pay the man ${int(round(200*money_modifier))} to dig for you or refuse?",
            "choices":{
                "Accept":{
                    "cost":{"money":0,"time":20,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"You dig and dig. Finally, your pickaxe strikes something softer. You frantically wipe away some dirt, revealing a slightly battered artefact."},
                        2:{"money":int(round(50*money_modifier)),"time":0,"artefacts":0,"text":f"You dig and dig. Finally, your pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around ${int(round(50*money_modifier))}."}
                    }
                },
                "Pay":{
                    "cost":{"money":int(round(200*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":0,"artefacts":1,"text":"The man digs and digs. Finally, his pickaxe strikes something softer. You rush to the scene, frantically wipe away some dirt and reveal a slightly battered artefact."},
                        2:{"money":int(round(50*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around ${int(round(50*money_modifier))}."},
                        3:{"money":int(round(100*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around ${int(round(100*money_modifier))}."},
                        4:{"money":int(round(150*money_modifier)),"time":0,"artefacts":0,"text":f"The man digs and digs. Finally, his pickaxe strikes something softer. Unfortunately, it's just a small gold nugget. Might be worth around ${int(round(150*money_modifier))}."}
                    }
                },
                "Refuse":{
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
                "Rent":{
                    "cost":{"money":int(round(50*money_modifier)),"time":0,"artefacts":0},
                    "results":{
                        1:{"money":0,"time":-10,"artefacts":0,"text":"You wait out the storm, losing 10 days. At least you leave the motel unscathed."}
                    }
                },
                "Shelter":{
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
                "Inside": {
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
                "Surroundings": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 1,
                            "text": "You walk around the building, and see a pile of dirt with a shovel beside it. You decide to dig and after 5 days, your shovel hits an artefact."},
                        2: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You don't really see anything after a walk around the building. You decide to just leave it be."}
                    }
                },
                "Away": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You walk away. There was probably nothing in that place anyway, besides rotting floorboards."}
                    }
                }
            }
        },
        11: {
            "event": "You explore the nearby wildlife sanctuary. Halfway through your trail, you notice a campsite full of people in indigenous clothing. Perhaps they have an artefact you could take?",
            "input": "Do you continue your relaxing walk or greet the tribesmen.. Or try stealing from them?",
            "choices": {
                "Walk": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 20, "artefacts": 0,
                            "text": "You walk the rest of the trail and feel completely at peace. As if you have no rush at all."
                                    "The sense of calmness extends your time by 10 days."},
                        2: {"money": 0, "time": -5, "artefacts": 0,
                            "text": "You forgot to read the length of the trail and walk a ridiculous distance.You spend 5 days in various lodges along the trail until you finally get to the end."},
                        3: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You find the quickest way out of the trail and get back on your journey."},
                    }
                },
                "Greet": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 1,
                            "text": "You spend 5 days living with the tribesmen, who tell you that they're living like their ancestors once did in this area.Happy with your stay, they send you off with a souvenir."},
                        2: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You greet the tribesmen and are treated to seemingly endless tales about the people who used to live in these lands.You fall asleep out of boredom and get kicked out of the campsite for this."},
                        3: {"money": 0, "time": 15, "artefacts": 0,
                            "text": "You find the tribesmen worshipping a false idol and hastily do right by attacking their totem."
                                    "The police are called on you but your righteous actions earn you the favour of your god. You get away and are granted 15 days time."
                            }
                    }
                },
                "Steal": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You put on a friendly facade and when the moment is right, you sneakily take something without anyone seeing it.After leaving you realize it was just a worthless plastic replica."},
                        2: {"money": 0, "time": -10, "artefacts": 0,
                            "text": "You greet the campers and immediately are caught trying to steal a historic artefact. You explain your righteous mission, but to no avail."
                                    "You spend 10 days in jail for attempted thievery."
                            },
                        3: {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": "You put on a friendly facade and when the moment is right, you sneakily take something without anyone seeing it."
                                    f"You find the item to be too paltry of an offering and pawn it off for ${int(round(200 * money_modifier))}."},
                        4: {"money": 0, "time": 0, "artefacts": -1,
                            "text": "You put on a friendly facade and when the moment is right, you attempt to steal something from the campers but get caught. "
                                    "They end up taking one of your artefacts as punishment and exile you."},
                    }
                }
            }
        },
        12: {
            "event": "You come across a cockfighting ring. The host is beckoning passersby to come and bet on one of the roosters."
                     "'C'mon up and bet on one of these fightin' birds! Paying 2:1 on winning bets!'",
            "input": f"Do you leave, bet ${int(round(200 * money_modifier))}, ${int(round(400 * money_modifier))} or try betting an artefact?",
            "choices": {
                f"{int(round(200 * money_modifier))}": {
                    "cost": {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(200 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "The birds are placed into the ring and the bell rings!!"
                                    "After a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(200 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "The birds are placed into the ring and the bell rings!!"
                                    "The referee tries egging on the roosters to engage in battle, but fails."
                                    f"After a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained ${int(round(400 * money_modifier))}!!"},
                        3: {"money": int(round(200 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(200 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "The birds are placed into the ring and the bell rings!!"
                                    f"The roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded ${int(round(200 * money_modifier))}."}
                    }
                },
                f"{int(round(400 * money_modifier))}": {
                    "cost": {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(400 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "The birds are placed into the ring and the bell rings!!"
                                    "After a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": int(round(800 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(400 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    f"The birds are placed into the ring and the bell rings!!"
                                    f"The referee tries egging on the roosters to engage in battle, but fails."
                                    f"After a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation. You've gained ${int(round(800 * money_modifier))}!!"},
                        3: {"money": int(round(400 * money_modifier)), "time": 0, "artefacts": 0,
                            "text": f"You bet ${int(round(400 * money_modifier))} on one of the roosters and join the crowd to watch the battle."
                                    "The birds are placed into the ring and the bell rings!!"
                                    f"The roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw. You're refunded ${int(round(400 * money_modifier))}."}
                    }
                },
                "Artefact": {
                    "cost": {"money": 0, "time": 0, "artefacts": 1},
                    "results": {
                        1: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You try to convince the referee to accept an artefact as a bet."
                                    "'Tell you what, I'll take this and give you two treasures from my collection if you win!"
                                    "The birds are placed into the ring and the bell rings!!"
                                    "After a few minutes, your rooster waddles away from the opponent and sits down. It's declared the loser and you leave the ring disappointed."},
                        2: {"money": 0, "time": 0, "artefacts": 2,
                            "text": "You try to convince the referee to accept an artefact as a bet."
                                    "'Tell you what, I'll take this and give you two treasures from my collection if you win!"
                                    "The birds are placed into the ring and the bell rings!!"
                                    "The referee tries egging on the roosters to engage in battle, but fails."
                                    "After a while, the opposing rooster sits down and you immediately declare your bird the winner by resignation."
                                    "The referee concedes and gives you 2 artefacts from his collection!!"},
                        3: {"money": 0, "time": 0, "artefacts": 1,
                            "text": "You try to convince the referee to accept an artefact as a bet."
                                    "'Tell you what, I'll take this and give you two treasures from my collection if you win!"
                                    "The birds are placed into the ring and the bell rings!!"
                                    "The roosters eat seeds off the ground for 20 minutes until the referee gets bored and declares the bout a draw."
                                    "You're given an artefact from his collection."}
                    }
                },
                "Leave": {
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
                "Check": {
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
                "Sleep": {
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
                "Hide": {
                    "cost": {"money": 0, "time": 0, "artefacts": 0},
                    "results": {
                        1: {"money": 0, "time": -5, "artefacts": 0,
                            "text": "You get into a fetal position under a blanket and wait out the entire night. Morning comes and you feel exhausted. Your sleep debt costs you 5 days."},
                        2: {"money": 0, "time": 0, "artefacts": 0,
                            "text": "You quickly grab your belongings and hide under a pile of clothes. You hear someone stepping in and looking around. Thankfully, they don't notice you."}
                    }
                }
            }
        },
    14: {
        "event": "Haluaisitko saada tai menettää artefaktin",
        "input": "debug",
        "choices": {
            "saada": {
                "cost": {"money": 0, "time": 0, "artefacts": 0},
                "results": {
                    1: {"money": 0, "time": 0, "artefacts": 1,
                        "text": "ok saat yhen"}
                }
            },
            "menettää": {
                "cost": {"money": 0, "time": 0, "artefacts": 0},
                "results": {
                    1: {"money": 0, "time": 0, "artefacts": -1,
                        "text": "ok otin sulta yhen"}
                }
            },
            "menettää maksamalla": {
                "cost": {"money": 0, "time": 0, "artefacts": 1},
                "results": {
                    1: {"money": 0, "time": 0, "artefacts": 0,
                        "text": "kiitti bro"}
                }
            },
            "maksaa 1 saada 2": {
                "cost": {"money": 0, "time": 0, "artefacts": 1},
                "results": {
                    1: {"money": 0, "time": 0, "artefacts": 2,
                        "text": "ok saat 2 takas"}
                }
            }
        }
    }
}

achievements = {
    "distance":[
        (10000, "First Steps", "Travelled 10000 km", 50),
        (30000, "Beginner Traveler", "Travelled 30000 km", 75),
        (60000, "Intermediate Traveler", "Travelled 60000 km", 100),
        (80000, "Advanced Traveler", "Travelled 80000 km", 150),
        (125000, "Master Traveler", "Travelled 125000 km", 300),
        (175000, "Business Class", "Travelled 175000 km", 400),
        (200000, "First Class", "Travelled 200000 km", 500),
        (250000, "Apostle", "Travelled 250000 km", 500),
        (9999999999999999999999, "error", "error", 999999999999)
    ],
    "countries":[
        (3, "Sightseer", "Visited 4 countries", 75),
        (6, "Tourist", "Visited 6 countries", 100),
        (10, "Regular", "Visited 10 countries", 150),
        (13, "Dual Citizenship", "Visited 13 countries", 200),
        (18, "Missionary", "Visited 18 countries", 350),
        (9999999999999999999999, "error", "error", 9999999999)
    ],
    "money":[
        (300, "Intern", "Earned $300", 50),
        (600, "Hard Worker", "Earned $600", 100),
        (1200, "Businessman", "Earned $1200", 150),
        (2000, "CEO", "Earned $2000", 200),
        (3000, "Tithe", "Earned $3000", 300),
        (4000, "Peter's Pence", "Earned $4000", 300),
        (99999999999999999999999999, "error", "error", 9999999999999999)
    ],
    "artefacts":[
        (1, "Explorer", "Found your first artefact", 50),
        (3, "Treasure Hunter", "Found 3 artefacts", 100),
        (8, "Culture Preserver", "Found 8 artefacts", 150),
        (12, "Indiana Jones", "Found 12 artefacts", 200),
        (9999999999999999999999, "error", "error", 9999999999999)
    ],
    "events":[
        (3, "Risk-taker", "Completed 2 events", 75),
        (6, "Lucky Guy", "Completed 6 events", 125),
        (10, "True Adventurer", "Completed 10 events", 150),
        (16, "Fortuna", "Completed 16 events", 300),
        (999999999999999999999, "error", "error", 9999999999999)
    ],
    "convert":[
        (1, "Believer", "Converted heretics once", 100),
        (2, "Faithful", "Converted heretics 2 times", 150),
        (4, "Devotee", "Converted heretics 4 times", 200),
        (7, "Chosen One", "Converted heretics 7 times", 300),
        (10, "Mandate from Heaven", "Converted heretics 10 times", 400),
        (999999999999999999999, "error", "error", 99999999)
    ]
}

def start():
    for eve in getallevents(0):
        uncompleted_events.append(eve)

def scores():
    cursor.execute("SELECT id, score FROM scores;")
    scores = cursor.fetchall()

    if scores:
        return {score[0]: score[1] for score in scores}
    else:
        return {}

# tää returnaa nyt listan uusista artefakteista
# parametreina nykyiset artefaktit, nykyinen manner ja annettava määrä
def add_artefacts(artefacts, cont, count = 1):
    #global artefacts_earned
    #artefacts_earned += count

    # Hanki kaikki mahd. aarteiden nimet mantereen perusteella
    tup = list(data.artefact_names[cont])

    # Sekoita artefaktien lista jotta pelaaja ei saa jokaisella pelikerralla samoja aarteita ekana
    random.shuffle(tup)

    # Luo erikseen lista pelaajan omistamista aarteiden nimistä
    # -> artefacts listaa olioita eikä sanoja joten ei voida verrata sillä
    names = list()
    for nm in artefacts:
        names.append(nm.name)

    new_artefacts = list()

    # Montako artefaktia lisätään?
    for c in range(0,count):
        # Satunnainen rahamäärä
        val = random.randint(600, 1000)

        # Montako mahdollista nimeä on?
        for i in range(0,len(tup)):
            nimi = tup[i]

            # Pelaaja ei voi saada duplikaatteja artifakteista
            if nimi not in names:
                new_artefacts.append(Artefact(nimi, val, cont))
                names.append(nimi)
                # Poistu loopista jos löydettiin käyttämätön nimi
                break
            else:
                if i == len(tup)-1:
                    # Mikäli pelaajalla on jo JOKAINEN aarre mantereelta, valitse satunnaisesti duplikaatti
                    nimi = tup[random.randint(0,len(tup)-1)]
                    new_artefacts.append(Artefact(nimi, val, cont))
                    names.append(nimi)

    return new_artefacts

# tälle annetaan artefaktilista sekä nykyinen manner sekä annettu indeksi (jos myydään artefakti, -1 meinaa ei myydä)
def remove_artefacts(artefacts, cont, count = 1, index = -1):
    # Poista tältä mantereelta kotoisin artefakti ekana
    priority = list()
    removables = list()

    for a in artefacts:
        if a.continent == cont:
            priority.append(a)
    # Tee randomilla jos ei anneta indeksiä (eli jos jokin event ottaa pelaajalta)
    if index == -1:
        for a in range(0,count):
            if len(priority) > 0:
                removables.append(artefacts[random.randint(0, len(priority)-1)])
            else:
                removables.append(artefacts[random.randint(0, len(artefacts)-1)])
    else:
        removables.append(artefacts[index])

    # palautetaan artefakti, joka poistetaan
    return removables

def get_event(modifier):
    global uncompleted_events
    # testausta varten laitetaan lista täyteen taas jos se on tyhjä
    if len(uncompleted_events) == 0:
        for eve in getallevents(modifier):
            uncompleted_events.append(eve)
    numero = random.choice(uncompleted_events)
    uncompleted_events.remove(numero)

    # TESTI EVENT
    # numero = 14
    choices = []
    mcosts = []
    tcosts = []
    acosts = []

    for choice in getallevents(modifier)[numero]["choices"]:
        choices.append(choice)
        mcosts.append(getallevents(modifier)[numero]["choices"][choice]['cost']['money'] * modifier)
        tcosts.append(getallevents(modifier)[numero]["choices"][choice]['cost']['time'])
        acosts.append(getallevents(modifier)[numero]["choices"][choice]['cost']['artefacts'])

    return {
        "number": numero,
        "text": getallevents(modifier)[numero]["event"],
        "question": getallevents(modifier)[numero]["input"],
        "choices": choices,
        "money_costs": mcosts,
        "time_costs": tcosts,
        "artefacts_costs": acosts
    }
    # debug
    # print(thing)
    return thing

def work(modifier):
    max_money = int(round(200 * modifier))
    min_money = int(round(100 * modifier))
    jobs = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher","cucumber quality inspector", "tree doctor", "farmer's assistant","professional supermarket greeter"]
    moneygain = random.randint(min_money, max_money)

    return {
        "text":f"You decide to work as a {random.choice(jobs)}. You earn ${moneygain}, but lose 10 days.",
        "money":moneygain,
        "time":15
    }

def get_event_result(numero, choice, modifier):
    result = random.randint(1, len(getallevents(modifier)[numero]["choices"][choice]["results"]))

    return {
        "text" : getallevents(modifier)[numero]["choices"][choice]["results"][result]["text"],
        "money" : getallevents(modifier)[numero]["choices"][choice]["results"][result]["money"] * modifier,
        "time" : getallevents(modifier)[numero]["choices"][choice]["results"][result]["time"],
        "artefact_count" : getallevents(modifier)[numero]["choices"][choice]["results"][result]["artefacts"]
    }

def start_fight(amount):
    player_hp = 10 + 5 * amount
    player_heals = 0 + amount // 2

    # hp, dmg, dodge, speed
    types = {
        "Bulwark": [16, 7, 1, 3],
        "Warden": [10, 4, 2.5, 2],
        "Vessel": [7, 2, 4, 0],
        "Zealot": [12, 3, 3, 1]
    }

    enemies_in_fight = {}
    for i in range(amount):
        enemy = random.choice(list(types.keys()))
        stats = types[enemy]

        enemies_in_fight[i] = {
            "type": enemy,
            "hp": stats[0],
            "dmg": stats[1],
            "ddg": stats[2],
            "spd": stats[3],
            "d_spd": stats[3]
        }

    return {
        "text": f"You find a group of {amount} robed men. You prepare to convert them, no matter the cost.",
        "player_hp": player_hp,
        "player_heals": player_heals,
        "enemies_in_fight": enemies_in_fight,
        "amount": amount,
        "guarding": False
    }

def get_airport(current_airport):
    global cursor
    airport_list = []
    data = []
    desc = []
    sql = f'SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE airport.name="{current_airport}" AND country.iso_country = airport.iso_country'
    cursor.execute(sql)
    data.append(cursor.fetchmany(3))

    if current_airport != "Ancient Chamber":
        sql = f'SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE airport.continent="AN" AND country.iso_country = airport.iso_country'
        cursor.execute(sql)
        data.append(cursor.fetchmany(3))

    for cont in ['NA', 'EU', 'AS', 'SA', 'OC', 'AF']:
        sql = f'(SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE type="small_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country AND airport.name NOT LIKE "%/%" ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE type="large_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country AND airport.name NOT LIKE "%/%" ORDER BY RAND() LIMIT 1) UNION ALL (SELECT airport.name AS aname, country.name AS cname, latitude_deg AS latitude, longitude_deg AS longitude, airport.continent AS continent, ident AS icao, type  FROM airport, country WHERE type="medium_airport" AND airport.continent="{cont}" AND country.iso_country = airport.iso_country AND airport.name NOT LIKE "%/%" ORDER BY RAND() LIMIT 1)'
        cursor.execute(sql)
        data.append(cursor.fetchmany(3))

    for i in range(len(cursor.description)):
        desc.append(cursor.description[i][0])

    for group in data:
        for row in group:
            airport = {}
            for i in range(len(desc)):
                airport[desc[i]] = row[i]
            airport_list.append(airport)

    for airport in airport_list:
        if airport["continent"] == "EU":
            airport["alt_cont"] = "Europe"
        elif airport["continent"] == "AS":
            airport["alt_cont"] = "Asia"
        elif airport["continent"] == "SA":
            airport["alt_cont"] = "South America"
        elif airport["continent"] == "OC":
            airport["alt_cont"] = "Oceania"
        elif airport["continent"] == "AF":
            airport["alt_cont"] = "Africa"
        elif airport["continent"] == "NA":
            airport["alt_cont"] = "North America"
        elif airport["continent"] == "AN":
            airport["alt_cont"] = "Antarctica"
        if airport["type"] == "small_airport":
            airport["cost"] = 150
        elif airport["type"] == "medium_airport":
            airport["cost"] = 300
        elif airport["type"] == "large_airport":
            airport["cost"] = 450

    return airport_list

def winning(money, time, total_distance, achieved, visited_countries):
    global cursor

    score = money + total_distance // 60 + time * 10

    #lisää score databaseen, testauksen aikana ei käytössä
    #cursor = conn.cursor()
    #cursor.execute("INSERT INTO scores (score) VALUES (%s)", (score,))
    #conn.commit()

    return {
        "achievements": achieved,
        "visited_countries": visited_countries,
        "total_distance": total_distance,
        "money": money,
        "time": time,
        "score": score,
        "money_score": money,
        "time_score": time * 10,
        "distance_score": total_distance // 60
    }