# Write your code here
import random


def shuffle_board(domino_set):
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
    "Function changes current player "
    hands['cur_player'] = 'player' if hands['cur_player'] == 'computer' else 'computer'


def add_to_snake(hands, tile, pos):
    playing_hand_name = 'player' if tile in hands['player'] else 'computer'
    hands[playing_hand_name].remove(tile)
    if pos:
        if hands['snake'][-1][-1] != tile[0]:
            tile = list(reversed(tile))
        hands['snake'].append(tile)
    else:
        if hands['snake'][0][0] != tile[1]:
            tile = list(reversed(tile))
        hands['snake'].insert(0, tile)



def print_hands(hands):
    print("Stock pieces:", hands['stock'])
    print("Computer pieces:", hands['computer'])
    print("Player pieces:", hands['player'])
    print("Domino snake:", hands['snake'])
    print("Status:", hands['cur_player'])


def determine_first_move(hands):
    dragon_snake = max(hands['player'] + hands['computer'])  # search the max tile from players hands
    first_player = 'computer' if dragon_snake in hands['computer'] else 'player'
    hands['cur_player'] = first_player
    hands[first_player].remove(dragon_snake)
    hands.update({'snake': [dragon_snake]})
    change_player(hands)


def print_interface(hands):
    print('=' * 70)
    print(f"Stock size: {len(hands['stock'])}")
    print(f"Computer pieces: {len(hands['computer'])}")
    print()
    if len(hands['snake']) > 6:  # if snake extends 6 tile length
        print(''.join([str(x) for x in hands['snake']][0:3]), end='')
        print('...', end='')
        print(''.join([str(x) for x in hands['snake']][-3:]))
    else:
        print(''.join([str(x) for x in hands['snake']]))
    print()
    print('Your pieces:')
    for pos, el in enumerate(hands['player'], 1):
        print(pos, el, sep=':')
    print()


def take_from_stack(hands, id):
    if len(hands['stock']) > 0:
        tile = hands['stock'].pop(-1)
        hands[id].append(tile)


def computer_turn(hands):
    """Computer turn logic"""
    list_of_vals = [x for el in hands['computer'] for x in el]
    count_of_vals = {i: list_of_vals.count(i) for i in range(0, 7)}
    tiles_score = {str(el): count_of_vals[el[0]] + count_of_vals[el[1]] for el in hands['computer']}
    tiles_score = dict(sorted(tiles_score.items(), key=lambda item: item[1], reverse=True))
    while len(tiles_score) > 0:
        tile = max(tiles_score, key=lambda key: tiles_score[key]) # takes max tile from tiles_score
        tile_list = [int(tile[1]),int(tile[4])]
        pos = None
        if verify_move(hands, tile_list, True):
            pos = True
        elif verify_move(hands, tile_list, False):
            pos = False
        if pos is not None:
            add_to_snake(hands, tile_list, pos)
            break
        else:
            tiles_score.pop(tile)


def player_turn(hands):
    while True:
        input_ = input()
        min = -len(hands['player'])
        max = len(hands['player'])
        if input_.lstrip('-').isdigit():
            input_ = int(input_)
            if input_ in range(min, max + 1):
                break
        print('Invalid input. Please try again.')
    if input_ == 0:
        take_from_stack(hands, 'player')
    else:
        tile = hands['player'].__getitem__(abs(input_) - 1)  # takes tile from players hand
        pos = True if input_ > 0 else False  # defines add side for add_snake
        if verify_move(hands, tile, pos):  # check if move is valid
            add_to_snake(hands, tile, pos)  # adds tile to snake
        else:
            print("Illegal move. Please try again.")
            player_turn(hands)


def verify_move(hands, tile, pos):
    """Werfies if  tile can be added to snake. Returns l/r str if can and fals if not"""""
    # Checks with side is chosen and save val in side
    if pos:  # if side is right
        side = hands['snake'][-1][-1]  # last right val of snake
    else:
        side = hands['snake'][0][0]  # last left val of snake
    # Checks if value is in tile
    if side in tile:
        return True
    else:
        return False


def who_win(hands):
    "Checks status of board"
    if len(hands['player']) == 0:
        return 'player'
    if len(hands['computer']) == 0:
        return 'computer'
    if check_draw(hands):
        return 'draw'
    else:
        return False


def check_draw(hands):
    '''Function return True if theres draw in snake'''
    if hands['snake'][0][0] == hands['snake'][-1][-1]:  # if both ends same
        end = hands['snake'][0][0]  # save end val
        if [x for el in hands['snake'] for x in el].count(end) == 8:  # if theres 8 vals in snake
            return True  # it's draw return True
    else:
        return False  # you can play


def game_loop():
    domino_set = list([j, i] for i in range(7) for j in range(i + 1))
    hands = shuffle_board(domino_set)  # dict of stock,plater,comp of list of hands
    determine_first_move(hands)
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
        if hands['cur_player'] == "computer":
            input("Status: Computer is about to make a move. Press Enter to continue...")
            computer_turn(hands)
        elif hands['cur_player'] == 'player':
            print("Status: It's your turn to make a move. Enter your command.")
            player_turn(hands)
        change_player(hands)


game_loop()
