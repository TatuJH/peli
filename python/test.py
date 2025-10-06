import random

def fight(amount):
    hp = 15 + amount * 5
    guarding = False
    fight_over = False
    # hp, dmg, dodge, speed
    types = {
    "Bulwark":[16, 6, 0, 3],
    "Warden":[10, 4, 2.5, 2],
    "Vessel":[8, 2, 5, 0],
    "Zealot":[12, 3, 3.33, 1]
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
        print(f"You're minding your business, as you feel a tap on your shoulder. You turn around to a to a robed man. A heretic, trying to stop you. You prepare to fight.")
    else:
        print(f"You're minding your business, as you feel a tap on your shoulder. You turn around to a to a group of {amount} robed men. Heretics, trying to stop you. You prepare to fight.")

    print("----")

    for enemy in range(amount):
        enemies.append(random.choice(["Bulwark", "Vessel", "Warden", "Zealot"]))
        enemies_in_fight[enemy]["hp"] = types[enemies[enemy]][0]
        enemies_in_fight[enemy]["dmg"] = types[enemies[enemy]][1]
        enemies_in_fight[enemy]["ddg"] = types[enemies[enemy]][2]
        enemies_in_fight[enemy]["spd"] = types[enemies[enemy]][3]

    changing_amount = amount

    while not fight_over:
        for enemy in range(amount):
            if enemies_in_fight[enemy]["hp"] == 0:
                temp = 'unconscious'
            elif enemies_in_fight[enemy]["spd"] == 0:
                temp = 'attacking'
            else:
                temp = f'charging for {enemies_in_fight[enemy]["spd"]} turns'
            if enemy < amount-1:
                if enemies_in_fight[enemy]["hp"] != 0:
                    print(f"Enemy \033[35m{enemy+1}\033[0m: "+f"\033[1m{enemies[enemy]}\033[0m"+f' \033[33m{enemies_in_fight[enemy]["hp"]}\033[0m'+ f' (\033[36m{temp}\33[0m)',end=" | ")
            else:
                if enemies_in_fight[enemy]["hp"] != 0:
                    print(f"Enemy \033[35m{enemy + 1}\033[0m: " + f"\033[1m{enemies[enemy]}\033[0m"+ f' \033[33m{enemies_in_fight[enemy]["hp"]}\033[0m'+ f' (\033[36m{temp}\33[0m)')

        print(f"----\n\033[33m{hp}\033[0m | \033[35mSTRIKE\033[0m (\033[35m#\033[0m)\033[0m | \033[35mPUSH\033[0m (\033[35m#\033[0m)\033[0m | \33[35mGUARD\033[0m | \033[35mESCAPE\033[0m")
        action = ""
        tempactionlist = ["slow", "guard", "escape"]
        for i in range(amount):
            if enemies_in_fight[i]["hp"] != 0:
                tempactionlist.append(f"strike {i+1}")
        for i in range(amount):
            if enemies_in_fight[i]["hp"] != 0:
                tempactionlist.append(f"push {i+1}")
        while action not in tempactionlist:
            action = input("> ").strip().lower()
        print("----")
        if action == "escape":
            if random.random() <= 0.3:
                if hp == 20:
                    print("You manage to escape the ambush unscathed.")
                    print("----")
                else:
                    print("You manage to escape the ambush.")
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
                        print(f"The \033[1m{enemies[enemynumber]}\033[0m loses all his stamina and gets knocked out.")
                        changing_amount -= 1
                else:
                    dmg = int(round(random.randint(3,6)))
                    print(f"The blow lands, dealing \033[31m{dmg}\033[0m damage.")
                    enemies_in_fight[enemynumber]["hp"] = enemies_in_fight[enemynumber]["hp"] - dmg
                    if enemies_in_fight[enemynumber]["hp"] <= 0:
                        print("----")
                        enemies_in_fight[enemynumber]["hp"] = 0
                        print(f"The \033[1m{enemies[enemynumber]}\033[0m loses all his stamina and gets knocked out.")
                        changing_amount -= 1
            print("----")
            if changing_amount == 0:
                print(f"Having defeated all the heretics, you earn \033[32m${amount*100}\033[0m.")
                fight_over = True
        elif "push" in action:
            enemynumber = int(action[5])-1
            print(f"You push the \033[1m{enemies[enemynumber]}\033[0m back, slowing their advance by \033[36m2 turns\033[0m. The \033[1m{enemies[enemynumber]}\033[0m retaliates, dealing \033[31m{enemies_in_fight[enemynumber]['dmg'] // 3}\033[0m damage.")
            enemies_in_fight[enemynumber]["spd"] = enemies_in_fight[enemynumber]["spd"] + 2
            hp -= enemies_in_fight[enemynumber]['dmg'] // 3
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
            print("You lose all your stamina and land in a puddle of mud. The heretics win and leave the scene.")
            fight_over = True
        guarding = False

fight(random.randint(1,4))
