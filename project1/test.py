import random

def fight(amount):
    hp = 15 + amount * 5
    heals = amount // 2
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
            fight_over = True
        guarding = False

fight(random.randint(1,4))
