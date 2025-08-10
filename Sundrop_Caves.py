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
    # save map
    # save fog
    # save player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

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
    if direction == 'up' and fog[y-1][x] != ' ':
        return fog[y-1][x]
    elif direction == 'down' and fog[y+1][x] != ' ':
        return fog[y+1][x]
    elif direction == 'left' and fog[y][x-1] != ' ':
        return fog[y][x-1]
    elif direction == 'right' and fog[y][x+1] != ' ':
        return fog[y][x+1]
    else:
        return True

def enter_mine():
    if player['portalPosition'] != [0, 0]:
        player['x'], player['y'] = player['portalPosition']
    else:
        player['x'], player['y'] = 0, 0

    player['turns'] = TURNS_PER_DAY
    while True:
        print(f"DAY {player['day']}")
        draw_view(fog, player)
        print(f"Turns left: {player['turns']} Load: {player['copper'] + player['silver'] + player['gold']} / {player['backpack']} Steps: {player['steps']}")
        print("(WASD) to move")
        print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")
        action = input("Action? ").lower()

        if action == "q":
            break
        elif action == "m":
            draw_map(fog, player)
        elif action == "i":
            show_information(player)
        elif action == "p":
            # Portal logic here
            pass
        elif action in "wasd":
            if action == "w" and player['y'] > 0:
                if check_ore('up') != True and player['copper'] + player['silver'] + player['gold'] == player['backpack']:
                    print('Your backpack is full')
                else:
                    move_player('up')
            elif action == "s" and player['y'] < len(game_map) - 1:
                if check_ore('down') != True and player['copper'] + player['silver'] + player['gold'] == player['backpack']:
                    print('Your backpack is full')
                else:
                    move_player('down')
            elif action == "a" and player['x'] > 0:
                if check_ore('left') != True and player['copper'] + player['silver'] + player['gold'] == player['backpack']:
                    print('Your backpack is full')
                else:
                    move_player('left')
            elif action == "d" and player['x'] < len(game_map[0]) - 1:
                if check_ore('right') != True and player['copper'] + player['silver'] + player['gold'] == player['backpack']:
                    print('Your backpack is full')
                else:
                    move_player('right')
            else:
                print("You can't move in that direction.")
        else:
            print("Invalid action.")

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
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

def show_buy_menu():
    print("----------------------- Shop Menu -------------------------")
    if player['pickaxe'] != 3:
        print(f"(P)ickaxe upgrade to Level {player['pickaxe']+1} to mine {pickaxe_level(player['pickaxe']+1)} ore for {pickaxe_price[player['pickaxe']-1]} GP")
    print(f"(B)ackpack upgrade to carry {player['backpack']+2} items for {(player['backpack']+2)*2} GP")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP: {player['GP']}")
    print("-----------------------------------------------------------")
            
#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")


show_main_menu()
choice = input("Your choice? ")
if choice.lower() == "n":
    game_map, fog = initialize_game(game_map,fog,player)
    player['name'] = input("Greetings, miner! What is your name? ")
    print(f"Pleased to meet you, {player['name']}, Welcome to Sundrop Town!")
    print()
    while True:
        if player['nextDay'] == True:
            player['nextDay'] = False
            player['day'] += 1
        show_town_menu()
        choice = input("Your choice? ")
        if choice.lower() == "b":
            while True:
                show_buy_menu()
                choice = input("Your choice? ")
                if choice.lower() == "b":
                    upgrade_backpack()
                elif choice.lower() == "p":
                    upgrade_pickaxe()
                elif choice.lower() == "l":
                    break
            #todo
        if choice.lower() == "i":
            show_information(player)
            #todo
        if choice.lower() == "m":
            draw_map(fog, player)
        if choice.lower() == "e":
            print("---------------------------------------------------")
            print(f"{f'DAY {player['day']}':^51}")
            print("---------------------------------------------------")
            enter_mine()
        if choice.lower() == "money":
            player['GP'] += 300