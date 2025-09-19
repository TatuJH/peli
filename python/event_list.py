events = {
    1:{
        "event":"You are given an investment opportunity on the street by a man in a trench coat. He says that by giving him \033[32m$100\033[0m you could make \033[32m$300\033[0m." ,
        "input":"Do you accept (a) or decline (d)?",
        "choices":{
            "a":{
                "cost":{"money":100,"time":0,"artefacts":0},
                "results":{
                    1:{"money":300,"time":0,"artefacts":0,"text":"The opportunity actually paid out. You earned \033[32m$300.\033[0m"},
                    2:{"money":0,"time":0,"artefacts":0,"text":"The opportunity was real... But you lost your \033[32m$100\033[0m."},
                    3:{"money":200,"time":-5,"artefacts":0,"text":"The man takes off running! You chase him and get your \033[32m$100\033[0m back. You also manage to snatch \033[32m$100\033[0m extra from him, but lose \033[34m5 days\033[0m in the process."}
                }
            },
            "d":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":0,"artefacts":0,"text":"You decline the man's offer. It was probably a scam anyway."}
                }
            }
        }
    },
    2:{
        "event":"You meet a witch, who says she can buy you time. Literally. She offers you \033[34m30 days\033[0m in exchange for \033[32m$100\033[0m.",
        "input":"Do you accept (a) or decline (d)?",
        "choices":{
            "a":{
                "cost":{"money":100,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":30,"artefacts":0,"text":"You bought yourself some time with \033[32m$100\033[0m. \033[34m30 days\033[0m to be exact."}
                }
            },
            "d":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":-5,"artefacts":0,"text":"You decline the witch's offer. She gets mad and curses you, draining you of \033[34m5 days\033[0m."}
                }
            }
        }
    },
    3:{
        "event":"You get lost, somehow.",
        "input":"Would you like to turn left (l), right (r) or continue straight (s)?",
        "choices":{
            "l":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":-10,"artefacts":0,"text":"You get even more lost, losing \033[34m10 days\033[0m in the process. Eventually, you find your way back."}
                }
            },
            "r":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":0,"artefacts":0,"text":"As you turn right, you notice that the airport is literally just there. Talk about luck."}
                }
            },
            "s":{
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
        "input":"Do you pray on your knees (k), standing up (s) or do you leave (l)?",
        "choices":{
            "k":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":0,"artefacts":1,"text":"Something rumbles. A hatch opens underneath the monument, revealing \033[33m1 artefact\033[0m! The gods must be pleased."}
                }
            },
            "s":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":-100,"time":-10,"artefacts":0,"text":"The monument starts glowing red. The gods didn't seem to like your praying. You feel a curse sweeping through you, draining you of \033[32m$100\033[0m and \033[34m10 days\033[0m."}
                }
            },
            "l":{
                "cost":{"money":0,"time":0,"artefacts":0},
                "results":{
                    1:{"money":0,"time":0,"artefacts":0,"text":"You decide to leave. Better not accidentally disrespect the gods."},
                    2:{"money":0,"time":-5,"artefacts":0,"text":"You decide to leave, but feel the earth starting to tremble. The gods weren't happy about your lack of praying. You black out and lose \033[34m5 days\033[0m."}
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