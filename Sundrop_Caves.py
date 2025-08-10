from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

pieces = {}
pieces['copper'] = (1,5)
pieces['silver'] = (1,3)
pieces['gold'] = (1,2)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    #Map loading code
    for x in map_file.read().split("\n"):
        map_struct.append(list(x))
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()
    return map_struct

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    for i in range(max(0, player['y'] - 1), min(len(fog), player['y'] + 2)):
        for j in range(max(0, player['x'] - 1), min(len(fog[0]), player['x'] + 2)):
            fog[i][j] = game_map[i][j]
    return fog


def initialize_game(game_map, fog, player):
    # initialize map
    game_map = load_map("level1.txt", game_map)

    #Initialize fog
    for x in range(len(game_map)):
        fog.append(["?"]*len(game_map[0]))

    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['name'] = ""
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['pickaxe'] = 1
    player['backpack'] = 10
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['nextDay'] = True
    player['portalPosition'] = [0, 0]
    player['enteredMine'] = False

    fog = clear_fog(fog, player)
    return game_map, fog

    
# This function draws the entire map, covered by the fof
def draw_map(fog, player):
    print()
    fog[player['y']][player['x']] = "M"
    print("+------------------------------+")
    for x in fog:
        print("|", end="")
        for i in x:
            print(i, end="")
        print("|")
    print("+------------------------------+")
    print()

# This function draws the 3x3 viewport
def draw_view(fog, player):
    print(f"DAY {player['day']}")

def pickaxe_level(level):
    if level == 1:
        return "bronze"
    elif level == 2:
        return "silver"
    elif level == 3:
        return "gold"

# This function shows the information for the player
def show_information(player):
    print()
    print("----- Player Information -----")
    print(f"Name: {player['name']}")
    print(f"Portal position: ({player['portalPosition'][0]}, {player['portalPosition'][1]})")
    print(f"Pickaxe level: {player['pickaxe']} ({pickaxe_level(player['pickaxe'])})")
    print(f"------------------------------")
    print(f"Load: {player['copper'] + player['silver'] + player['gold']} / {player['backpack']}")
    print("------------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("------------------------------")


# This function saves the game
def save_game(game_map, fog, player):
    with open("savefile/game_map.txt", "w") as f:
        for row in game_map:
            f.write("".join(row) + "\n")
    with open("savefile/fog_map.txt", "w") as f:
        for row in fog:
            f.write("".join(row) + "\n")
    with open("savefile/player_data.txt", "w") as f:
        f.write(str(player))

# This function loads the game
def load_game(game_map, fog, player):
    with open("savefile/game_map.txt", "r") as f:
        game_map = f.read().strip().split("\n")
    with open("savefile/fog_map.txt", "r") as f:
        fog = f.read().strip().split("\n")
    with open("savefile/player_data.txt", "r") as f:
        player = eval(f.read())
    return game_map, fog, player

def show_high_scores():
    highscores = []
    temp = []
    with open('highscores.txt', 'r') as f:
        for x in f.read().strip().split("\n"):
            highscores.append(x.split())
        print("----------------------------")
        print("Top 5 High Scores:")
        highscores.sort(key=lambda x: (int(x[2]), int(x[3]), -int(x[1])))
        print("Rank | Name       | GP   | Days | Steps")
        print("----------------------------------------")
        for num, x in enumerate(highscores[:5], 1):
            print(f"{num:>4} | {x[0]:<10} | {x[1]:>4} | {x[2]:>4} | {x[3]:>5}")
    print("----------------------------------------")

def upgrade_backpack():
    global player
    if player['GP'] >= (player['backpack']+2)*2:
        player['backpack'] += 2
        player['GP'] -= player['backpack']*2
        print(f"Congratulations! You can now carry {player['backpack']} items!")
    else:
        print("You do not have enough GP to purchase this...")

def upgrade_pickaxe():
    if player['GP'] >= pickaxe_price[player['pickaxe']-1]:
        player['GP'] -= pickaxe_price[player['pickaxe']-1]
        player['pickaxe'] += 1
        print(f"Congratulations! You can now mine {pickaxe_level(player['pickaxe'])}")
    else:
        print("You do not have enough GP to do this...")

def generate_view(game_map, player):
    view_map = [[' ',' ',' '],
                [' ','M',' '],
                [' ',' ',' ']]
    x, y = player['x'], player['y']
    if y == 0:
        view_map[0][0] = "#"
        view_map[0][1] = "#"
        view_map[0][2] = "#"
    if y == len(game_map) - 1:
        view_map[2][0] = "#"
        view_map[2][1] = "#"
        view_map[2][2] = "#"
    if x == 0:
        view_map[0][0] = "#"
        view_map[1][0] = "#"
        view_map[2][0] = "#"
    if x == len(game_map[0]) - 1:
        view_map[0][2] = "#"
        view_map[1][2] = "#"
        view_map[2][2] = "#"
    for row in range(len(view_map)):
        for i in range(len(view_map[row])):
            if view_map[row][i] != '#' and view_map[row][i] != 'M':
                view_map[row][i] = game_map[y - 1 + row][x - 1 + i]
    return view_map

def draw_view(fog, player):
    x, y = player['x'], player['y']
    view = generate_view(fog, player)
    print("+---+")
    for row in view:
        print("|" + ''.join(row) + "|")
    print("+---+")

def move_player(direction):
    x,y = player['x'], player['y']
    if direction == 'up':
        fog[y][x] = ' '
        fog[y-1][x] = 'M'
        player['y'] -= 1
    elif direction == 'down':
        fog[y][x] = ' '
        fog[y+1][x] = 'M'
        player['y'] += 1
    elif direction == 'left':
        fog[y][x] = ' '
        fog[y][x-1] = 'M'
        player['x'] -= 1
    elif direction == 'right':
        fog[y][x] = ' '
        fog[y][x+1] = 'M'
        player['x'] += 1
    clear_fog(fog, player)

def check_ore(direction):
    x, y = player['x'], player['y']
    if direction == 'up' and fog[y-1][x] != ' ' and fog[y-1][x] != 'T':
        return fog[y-1][x]
    elif direction == 'down' and fog[y+1][x] != ' ' and fog[y+1][x] != 'T':
        return fog[y+1][x]
    elif direction == 'left' and fog[y][x-1] != ' ' and fog[y][x-1] != 'T':
        return fog[y][x-1]
    elif direction == 'right' and fog[y][x+1] != ' ' and fog[y][x+1] != 'T':
        return fog[y][x+1]
    else:
        return True

def enter_town():
    if player['nextDay'] == True:
        player['nextDay'] = False
        player['day'] += 1
    if player['enteredMine']:
        print("You head back to town.")
        sell_ores(player)
    show_town_menu()

def enter_portal(player):
    player['portalPosition'] = [player['x'], player['y']]
    print("-----------------------------------------------------")
    print("You place your portal stone here and zap back to town.")
    enter_town()

def sell_ores(player):
    revenue = 0
    copper, silver, gold = False, False, False
    if player['copper'] > 0:
        copper = True
        revenue += player['copper'] * randint(prices['copper'][0], prices['copper'][1])
    if player['silver'] > 0:
        silver = True
        revenue += player['silver'] * randint(prices['silver'][0], prices['silver'][1])
    if player['gold'] > 0:
        gold = True
        revenue += player['gold'] * randint(prices['gold'][0], prices['gold'][1])
    if copper or silver or gold:
        print(f"You sell{f" {player['copper']} copper ore" if copper else ""}{" and" if copper and (silver or gold) else ""}{f" {player['silver']} silver ore" if silver else ""}{" and" if silver and gold else ""}{f" {player['gold']} gold ore" if gold else ""} for {revenue} GP.")
        player['copper'], player['silver'], player['gold'] = 0, 0, 0
        player['GP'] += revenue
        print(f"You now have {player['GP']} GP!")
        if player['GP'] >= WIN_GP:
            win()
    else:
        print("You have nothing to sell...")
    
def win():
    print("-------------------------------------------------------------")
    print(f"Woo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
    print("You now have enough to retire and play video games every day.")
    print(f"And it only took you {player['day']} days and {player['steps']} steps!")
    print("-------------------------------------------------------------")
    with open("highscores.txt", "a") as f:
         f.write(f"{player['name']} {player['GP']} {player['day']} {player['steps']}\n")
    main_menu()

def mine_ore(ore_type):
    x,y = player['x'], player['y']
    mined = randint(pieces[mineral_names[ore_type]][0], pieces[mineral_names[ore_type]][1])
    player[mineral_names[ore_type]] += mined
    print(f"You mined {mined} piece(s) of {mineral_names[ore_type]}")
    if player['copper'] + player['silver'] + player['gold'] > player['backpack']:
        excess = (player['copper'] + player['silver'] + player['gold']) - player['backpack']
        print(f"...but you can only carry {mined-excess} more piece(s)!")
        player[mineral_names[ore_type]] -= excess
    game_map[y][x] = ' '

def enter_mine():
    player['enteredMine'] = True
    player['nextDay'] = True
    if player['portalPosition'] != [0, 0]:
        player['x'], player['y'] = player['portalPosition']
    else:
        player['x'], player['y'] = 0, 0

    player['turns'] = TURNS_PER_DAY
    while player['turns'] > 0:
        print(f"DAY {player['day']}")
        draw_view(fog, player)
        print(f"Turns left: {player['turns']} Load: {player['copper'] + player['silver'] + player['gold']} / {player['backpack']} Steps: {player['steps']}")
        print("(WASD) to move")
        print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")
        action = input("Action? ").lower()
        print()
        print("---------------------------------------------------")

        if action == "q":
            break
        elif action == "m":
            draw_map(fog, player)
        elif action == "i":
            show_information(player)
        elif action == "p":
            enter_portal(player)
        elif action in "wasd":
            if action == "w" and player['y'] > 0:
                ore = check_ore('up')
                if ore != True and player['copper'] + player['silver'] + player['gold'] == player['backpack']:
                    print('Your backpack is full')
                    continue
                else:
                    move_player('up')
                    if ore in mineral_names:
                        mine_ore(ore)
            elif action == "s" and player['y'] < len(game_map) - 1:
                ore = check_ore('down')
                if ore != True and player['copper'] + player['silver'] + player['gold'] == player['backpack']:
                    print('Your backpack is full')
                    continue
                else:
                    move_player('down')
                    if ore in mineral_names:
                        mine_ore(ore)
            elif action == "a" and player['x'] > 0:
                ore = check_ore('left')
                if ore != True and player['copper'] + player['silver'] + player['gold'] == player['backpack']:
                    print('Your backpack is full')
                    continue
                else:
                    move_player('left')
                    if ore in mineral_names:
                        mine_ore(ore)
            elif action == "d" and player['x'] < len(game_map[0]) - 1:
                ore = check_ore('right')
                if ore != True and player['copper'] + player['silver'] + player['gold'] == player['backpack']:
                    print('Your backpack is full')
                    continue
                else:
                    move_player('right')
                    if ore in mineral_names:
                        mine_ore(ore)
            else:
                print("You can't move in that direction.")
                continue
            player['turns'] -= 1
            player['steps'] += 1
            if game_map[player['y']][player['x']] == 'T':
                enter_town()
        else:
            print("Invalid action.")
    print("You are exhausted.")
    enter_portal(player)

def show_player_information(player):
    print()
    print("--- Player Information ---")
    print(f"Name: {player['name']}")
    print(f"Current position: ({player['x']}, {player['y']})")
    print(f"Pickaxe level: {player['pickaxe']} ({pickaxe_level(player['pickaxe'])})")
    print(f"Gold: {player['gold']}")
    print(f"Silver: {player['silver']}")
    print(f"Bronze: {player['bronze']}")
    print("---------------------------")
    print(f"Load: {(player['copper'] + player['silver'] + player['gold'])} / {player['backpack']}")
    print("---------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("---------------------------")

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    while True:
        print()
        print(f"DAY {player['day']}")
        print("----- Sundrop Town -----")
        print("(B)uy stuff")
        print("See Player (I)nformation")
        print("See Mine (M)ap")
        print("(E)nter mine")
        print("Sa(V)e game")
        print("(Q)uit to main menu")
        print("------------------------")
        choice = input("Your choice? ")
        if choice.lower() == "b":
            while True:
                show_buy_menu()
                choice = input("Your choice? ")
                if choice.lower() == "b":
                    upgrade_backpack()
                elif choice.lower() == "p":
                    if player['pickaxe'] < 3:
                        upgrade_pickaxe()
                    else:
                        print("Your pickaxe is already upgraded to the max!")
                elif choice.lower() == "l":
                    break
                else:
                    print("Please select a valid option")
        elif choice.lower() == "i":
            show_information(player)
        elif choice.lower() == "m":
            draw_map(fog, player)
        elif choice.lower() == "e":
            print("---------------------------------------------------")
            print(f"{f'DAY {player['day']}':^51}")
            print("---------------------------------------------------")
            enter_mine()
        elif choice.lower() == "v":
            save_game(game_map, fog, player)
        elif choice.lower() == "q":
            break
        else:
            print("Please select a valid option")
        

def show_buy_menu():
    print("----------------------- Shop Menu -------------------------")
    if player['pickaxe'] != 3:
        print(f"(P)ickaxe upgrade to Level {player['pickaxe']+1} to mine {pickaxe_level(player['pickaxe']+1)} ore for {pickaxe_price[player['pickaxe']-1]} GP")
    print(f"(B)ackpack upgrade to carry {player['backpack']+2} items for {(player['backpack']+2)*2} GP")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP: {player['GP']}")
    print("-----------------------------------------------------------")

def main_menu():
    global game_map, fog, player
    while True:
        show_main_menu()
        choice = input("Your choice? ")
        if choice.lower() == "n":
            game_map, fog = initialize_game(game_map,fog,player)
            player['name'] = input("Greetings, miner! What is your name? ")
            print(f"Pleased to meet you, {player['name']}, Welcome to Sundrop Town!")
            print()
            enter_town()
        elif choice.lower() == "l":
            game_map, fog, player = load_game(game_map, fog, player)
            print(f"Welcome back, {player['name']}!")
            print()
            enter_town()
        elif choice.lower() == "h":
            show_high_scores()
        elif choice.lower() == "q":
            break
        else:
            print("Please select a valid option")

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")
main_menu()