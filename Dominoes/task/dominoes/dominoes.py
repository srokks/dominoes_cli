# Write your code here
import random


def shuffle_board(domino_set):
    '''

    :param domino_set:
    :return:
    '''
    player_pieces = []
    computer_pieces = []
    stock = domino_set.copy()
    for i in range(7):
        choice = random.choice(stock)
        stock.remove(choice)
        player_pieces.append(choice)
        choice = random.choice(stock)
        stock.remove(choice)
        computer_pieces.append(choice)
    return {'stock': stock, 'player': player_pieces, 'computer': computer_pieces, 'cur_player': None}


def change_player(hands):
    '''

    :param hands:
    :return:
    '''
    hands['cur_player'] = 'player' if hands['cur_player'] == 'computer' else 'computer'


def add_to_snake(hands, tile, pos):
    '''

    :param hands:
    :param tile:
    :param pos:
    :return:
    '''
    playing_hand_name = 'player' if tile in hands['player'] else 'computer' # checks from with hand is played
    hands[playing_hand_name].remove(tile) # removes tile from playing hand
    if pos:  # True - extend domino snake
        if hands['snake'][-1][-1] != tile[0]:
            tile = list(reversed(tile))
        hands['snake'].append(tile)
    else: # False add at [0] index
        if hands['snake'][0][0] != tile[1]:
            tile = list(reversed(tile))
        hands['snake'].insert(0, tile)

def determine_first_move(hands):
    '''

    :param hands:
    :return:
    '''
    dragon_snake = max(hands['player'] + hands['computer'])  # search the max tile from players hands
    first_player = 'computer' if dragon_snake in hands['computer'] else 'player' # defines who plays first
    hands['cur_player'] = first_player  # add to hands dict
    hands[first_player].remove(dragon_snake) # remove tile from playing hand
    hands.update({'snake': [dragon_snake]}) # add it to hands
    change_player(hands) # change player


def print_interface(hands):
    '''

    :param hands:
    :return:
    '''
    print('=' * 70)
    print(f"Stock size: {len(hands['stock'])}")
    print(f"Computer pieces: {len(hands['computer'])}")
    print()
    if len(hands['snake']) > 6:  # if snake extends 6 tile length
        print(''.join([str(x) for x in hands['snake']][0:3]), end='') # print first 3 ...
        print('...', end='') # ...
        print(''.join([str(x) for x in hands['snake']][-3:])) # and last 3
    else:
        print(''.join([str(x) for x in hands['snake']])) # print full snake
    print()
    print('Your pieces:') # shows player tiles
    for pos, el in enumerate(hands['player'], 1):
        print(pos, el, sep=':')
    print()


def take_from_stock(hands, id):
    '''

    :param hands: deck of domino tiles
    :param id: who is taking from stack
    :return: None
    '''
    if len(hands['stock']) > 0:
        tile = hands['stock'].pop(-1)
        hands[id].append(tile)


def computer_turn(hands):
    '''
    Computer turn logic
    :param hands: dict of prepared hands
    '''
    list_of_vals = [x for el in hands['computer'] for x in el]  # gens strig of values in computer hands
    count_of_vals = {i: list_of_vals.count(i) for i in range(0, 7)}  # calculate population of vals in hand
    # create score dict with tile as key and sum of pop of number -
    tiles_score = {str(el): count_of_vals[el[0]] + count_of_vals[el[1]] for el in hands['computer']}
    # sort dictionary for taking from first
    tiles_score = dict(sorted(tiles_score.items(), key=lambda item: item[1], reverse=True))
    while len(tiles_score) > 0: # while tiles score is not empty
        tile = max(tiles_score, key=lambda key: tiles_score[key]) # takes max tile from tiles_score
        tile_list = [int(tile[1]),int(tile[4])] # converts str key of list to list
        pos = bool  # inits pos val
        if verify_move(hands, tile_list, True): # checks right side of snake
            pos = True
        elif verify_move(hands, tile_list, False):# checks left side of snake
            pos = False
        if pos is not None: # if theres match ands pos is setted
            add_to_snake(hands, tile_list, pos)  # add to snake
            break
        else:
            tiles_score.pop(tile)  # pop from and check next tile from list
    if len(tiles_score) == 0:  # if non of tiles matches
        take_from_stock(hands, 'computer') # take from stock

def player_turn(hands):
    '''
    Player turn logic
    :param hands: dict of prepared hands
    '''
    while True:
        input_ = input() # takes input
        min = -len(hands['player'])  # defines min of input
        max = len(hands['player'])  # defines min of input
        if input_.lstrip('-').isdigit():  # checks if input is digit
            input_ = int(input_)
            if input_ in range(min, max + 1): # check if input is in min,max range
                break
        print('Invalid input. Please try again.')
    if input_ == 0:  # takes from stock
        take_from_stock(hands, 'player')
    else:
        tile = hands['player'].__getitem__(abs(input_) - 1)  # takes tile from players hand
        pos = True if input_ > 0 else False  # defines add side for add_snake
        if verify_move(hands, tile, pos):  # check if move is valid
            add_to_snake(hands, tile, pos)  # adds tile to snake
        else:
            print("Illegal move. Please try again.")
            player_turn(hands)  # loops if selected tile cannot be inputed to snake


def verify_move(hands, tile, pos):
    '''
    Verify entered move
    :param hands: dict of prepared hands
    :param tile: list as tile
    :param pos: True of False according to where put in domino snake
    :return:
    '''
    # Checks with side is chosen and save val in side
    if pos:  # if side is right
        side = hands['snake'][-1][-1]  # last right val of snake
    else:
        side = hands['snake'][0][0]  # last left val of snake
    # Checks if value is in tile
    if side in tile: # checks if side is in tile
        return True
    else:
        return False


def who_win(hands):
    '''
    Check win condition
    :param hands: dict of prepared hands
    :return: str or False
    '''
    # Check who runs out of tiles a set him as winner
    if len(hands['player']) == 0:
        return 'player'
    if len(hands['computer']) == 0:
        return 'computer'
    if check_draw(hands): # check if theres draw
        return 'draw'
    else:
        return False


def check_draw(hands):
    '''
    Check if theres draw in domino snake
    :param hands: dict of prepared hands
    '''
    if hands['snake'][0][0] == hands['snake'][-1][-1]:  # if both ends same
        end = hands['snake'][0][0]  # save end val
        if [x for el in hands['snake'] for x in el].count(end) == 8:  # if theres 8 vals in snake
            return True  # it's draw return True
    else:
        return False  # you can play


def game_loop():
    '''
    Main dominos game loop
    '''
    domino_set = list([j, i] for i in range(7) for j in range(i + 1)) # gens set of domino tiles
    hands = shuffle_board(domino_set)  # shuffle tiles between stock/player/computer
    determine_first_move(hands)  # determines who has first move
    while True:
        # Main game loop
        print_interface(hands)  # prints board
        win_stat = who_win(hands) # checks win condition
        if win_stat == 'player':
            print("Status: The game is over. You won!")
            break
        elif win_stat == 'computer':
            print("Status: The game is over. The computer won!")
            break
        elif win_stat == 'draw':
            print("Status: The game is over. It's a draw!")
            break

        # Player turn logic
        if hands['cur_player'] == "computer":
            input("Status: Computer is about to make a move. Press Enter to continue...")
            computer_turn(hands)
        elif hands['cur_player'] == 'player':
            print("Status: It's your turn to make a move. Enter your command.")
            player_turn(hands)
        change_player(hands) # change player after turn


if __name__ == '__main__':
    game_loop()