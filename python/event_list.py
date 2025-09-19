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
                    1:{"money":50,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m of your time. On the positive side, you find \033[32m$50\033[0m on the ground."},
                    2:{"money":100,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m of your time. On the positive side, you find \033[32m$100\033[0m on the ground."},
                    3:{"money":200,"time":-10,"artefacts":0,"text":"That wasn't the right way and you lose \033[34m10 days\033[0m of your time. On the positive side, you find \033[32m$200\033[0m on the ground."}
                }
            }
        }
    }
}