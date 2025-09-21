events = {
    1:{
        "event":"You are given an investment opportunity on the street by a man in a trench coat. He says that by giving him \033[32m$100\033[0m you could make \033[32m$300\033[0m." ,
        "input":"Do you \033[35maccept\033[0m or \033[35mdecline\033[0m?",
        "choices":{
            "accept":{
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
        "event":"You meet a witch, who says she can buy you time. Literally. She offers you \033[34m30 days\033[0m in exchange for \033[32m$100\033[0m.",
        "input":"Do you \033[35maccept\033[0m or \033[35mdecline\033[0m?",
        "choices":{
            "accept":{
                "cost":{"money":100,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":30,"artefacts":0,"text":"You bought yourself some time with \033[32m$100\033[0m. \033[34m30 days\033[0m to be exact."}
                }
            },
            "decline":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":-5,"artefacts":0,"text":"You decline the witch's offer. She gets mad and curses you, draining you of \033[34m5 days\033[0m."}
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
                    1:{"money":50,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m of your time. On a positive note, you find \033[32m$50\033[0m on the ground."},
                    2:{"money":100,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m of your time. On a positive note, you find \033[32m$100\033[0m on the ground."},
                    3:{"money":200,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m of your time. On a positive note, you find \033[32m$200\033[0m on the ground."}
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
                    1:{"money":0,"time":0,"artefacts":1,"text":"Something rumbles. A hatch opens underneath the monument, revealing \033[33m1 artefact\033[0m! The gods must be pleased."}
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
                    1:{"money":0,"time":0,"artefacts":0,"text":"You decide to leave. Better not accidentally disrespect the gods."},
                    2:{"money":0,"time":-5,"artefacts":0,"text":"You decide to leave, but feel the earth starting to tremble. The gods weren't happy about your lack of praying. You black out and lose \033[34m5 days\033[0m."}
                }
            }
        }
    },
    5:{
        "event":"You see a man in a suit strolling on the street. He seems to be giving money to everyone kind enough to greet him.",
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
    }
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