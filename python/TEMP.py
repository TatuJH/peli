# def airport_actions():
#     global time
#     global money
#     global remaining_actions
#     remaining_actions = 3
#     #if remaining_actions == max_actions:
#     quiz(cont)
#
#     first_action = ""
#     second_action = ""
#     third_action = ""
#     all_actions = ["work", "explore", "auction"]
#     while remaining_actions >= 0:
#         check_inventory()
#         # Nollaa joka kierroksen alussa
#         action = ""
#         # Eka vuoro
#         if remaining_actions == 3:
#             print(
#                 f"You've just arrived, and thus have {remaining_actions} actions remaining on this airport before the spirit catches you.")
#         # toka ja kolmas
#         elif remaining_actions > 0:
#             if remaining_actions == 1:
#                 print(f"You have {remaining_actions} action remaining on this airport before the spirit catches you.")
#             else:
#                 print(f"You have {remaining_actions} actions remaining on this airport before the spirit catches you.")
#         # Vika
#         else:
#             print(f"You feel impending doom approaching.")
#             all_actions = ["leave"]
#         while action not in all_actions:
#             if remaining_actions > 0:
#                 action = input(
#                     "Would you like to either \033[35mwork\033[0m, \033[35mexplore\033[0m, or visit the \033[35mauction\033[0m house?\n> ")
#             else:
#                 action = input("You feel the overwhelming need to \033[35mLEAVE\033[0m immediately!\n> ")
#         print("----")
#         if remaining_actions > 0:
#             if action == "work":
#                 work = ["janitor", "fast food cook", "secretary", "freelance actor", "substitute teacher",
#                         "cucumber quality inspector", "tree doctor", "farmer's assistant",
#                         "professional supermarket greeter"]
#                 print(
#                     f"You decide to work as a {random.choice(work)}. You earn \033[32m$200\033[0m, but lose \033[34m10 days\033[0m.")
#                 money += 200
#                 time -= 10
#                 print("----")
#             elif action == "explore":
#                 event()
#             elif action == "auction":
#                 shop()
#
#             # Onko pelaaja tulhannut kaiken ajan?
#             check_gameover()
#             remaining_actions -= 1
#         else:
#             if action == "leave":
#                 # Onko pelaajalla rahaa, jolla lentää?
#                 check_gameover()
#                 choose_continent()
#                 return
#
#
#     # peli päättyis tähän lol
#     check_gameover()
#     return