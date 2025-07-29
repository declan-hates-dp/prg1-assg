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
    x = player['x']
    y = player['y']
    if x != 0:
        fog[y][x-1] = game_map[y][x-1]
        if y != 0:
            fog[y-1][x-1] = game_map[y-1][x-1]
        if y != len(fog)-1:
            fog[y+1][x-1] = game_map[y-1][x-1]
    if x != len(fog[0])-1:
        fog[y][x+1] = game_map[y][x+1]
        if y != len(fog)-1:
            fog[y+1][x+1] = game_map[y+1][x+1]
        if y != 0:
            fog[y-1][x+1] = game_map[y-1][x+1]
    if y != 0:
        fog[y-1][x] = game_map[y-1][x]
    if y != len(fog):
        fog[y+1][x] = game_map[y+1][x]
    fog[y][x] = game_map[y][x]
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
def draw_view(game_map, fog, player):
    return

# This function shows the information for the player
def show_information(player):
    return

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

def pickaxe_upgrade():
    pass

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
    pickaxe_upgrade()
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
                elif choice.lower() == "l":
                    break
            #todo
        if choice.lower() == "i":
            continue
            #todo
        if choice.lower() == "m":
            draw_map(fog, player)