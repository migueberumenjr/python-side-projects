from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create white magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 40, 1500, "white")
curaga = Spell("Curaga", 50, 3500, "white")


# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP or one party member", 9999)
hielixir = Item("Mega Elixir", "elixir", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Create player spell and items "bags"
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item": hielixir, "quantity": 2}, {"item": grenade, "quantity": 5}]


# Instantiate People
player1 = Person("Vegeta  ", 3260, 132, 500, 34, player_spells, player_items)
player2 = Person("Goku    ", 4160, 188, 511, 34, player_spells, player_items)
player3 = Person("Trunks  ", 3089, 174, 488, 34, player_spells, player_items)

enemy1 = Person("Frieza", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Buu   ", 18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Cell  ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print("\n")

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=============================================")

    print("\n")
    print("NAME                 HP                                     MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    print("\n")
    print("---------------------------------------------")

    for player in players:
        player.choose_action()
        choice = int(input("    Choose action: ")) - 1

        if choice == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            if enemy > len(enemies) - 1 or enemy < -1:
                continue

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        elif choice == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                if enemy > len(enemies) - 1 or enemy < -1:
                    continue

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        elif choice == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Mega Elixir":
                    for i in players:
                        i.hp == i.maxhp
                        i.mp == i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                if enemy > len(enemies) - 1 or enemy < -1:
                    continue

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    # Check if player won
    if len(enemies) == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if enemy won
    elif len(players) == 0:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    print("\n")
    # Enemy attack phase
    for enemy in enemies:
        # Choose attack
        enemy_choice = random.randrange(0,2)

        if enemy_choice == 0:
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ","") + " attacks " + players[target].name.replace(" ","") + " for", enemy_dmg, "points of damage")

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has died.")
                del players[target]

        elif enemy_choice == 1:
            magic_choice = random.randrange(0, len(enemy.magic))
            spell = enemy.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = enemy.get_mp()

            pct = (enemy.hp / enemy.maxhp) * 100

            if enemy.mp < spell.cost or spell.type == "white" and pct > 50:
                continue

            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "") + " for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, len(players))
                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + enemy.name.replace(" ","") + "'s " + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
