from graphics import Canvas
import time

'''
RULES:
Mario can walk, run, jump, walljump
generate enemies
enemies die if you land on them
touching flag wins
'''
    
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 900
PLAYER_DIMENSIONS = (29, 13)
SIZE = 20

# if you make this larger, the game will go slower
DELAY = 1/60
PLAYER_START_POS = (2, 39)
FLAG_START_POS = (38, 8)
DIRECTION_MAPPINGS = {
                      'd': 'r', 'ArrowRight': 'r',
                      'a': 'l', 'ArrowLeft': 'l',
                      'w': 'jump', 'ArrowUp': 'jump', 'space': 'jump'
                     }

def draw_background(canvas):
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 'sky blue')

def draw_block(canvas, px, py):
    inset = 2
    id = canvas.create_rectangle(px, py, px+SIZE, py+SIZE, 'black')
    canvas.create_rectangle(px+inset, py+inset, px+SIZE-inset, py+SIZE-inset, 'brown')
    return id

def draw_coin(canvas, x, y):
    buffer = 5
    inset = 2
    outter = canvas.create_rectangle(x*SIZE+buffer, y*SIZE+buffer, x*SIZE+SIZE-buffer, y*SIZE+SIZE-buffer, 'black')
    inner = canvas.create_rectangle(x*SIZE+buffer+inset, y*SIZE+buffer+inset, x*SIZE+SIZE-buffer-inset, y*SIZE+SIZE-buffer-inset, 'yellow')
    return (outter, inner)

def draw_enemy(canvas, x, y):
    buffer = 3
    inner = []
    hitbox = canvas.create_rectangle(x*SIZE+buffer, y*SIZE+buffer, x*SIZE+SIZE-buffer, y*SIZE+SIZE-1, 'sky blue')
    # body
    inner.append(canvas.create_rectangle(x*SIZE+buffer+3, y*SIZE+SIZE-15, x*SIZE+SIZE-buffer-3, y*SIZE+SIZE-14, 'brown'))
    inner.append(canvas.create_rectangle(x*SIZE+buffer+1, y*SIZE+SIZE-13, x*SIZE+SIZE-buffer-1, y*SIZE+SIZE-11, 'brown'))
    inner.append(canvas.create_rectangle(x*SIZE+buffer, y*SIZE+SIZE-10, x*SIZE+SIZE-buffer, y*SIZE+SIZE-5, 'brown'))
    # eyes
    inner.append(canvas.create_rectangle(x*SIZE+buffer+2, y*SIZE+SIZE-9, x*SIZE+buffer+4, y*SIZE+SIZE-8, 'white'))
    inner.append(canvas.create_rectangle(x*SIZE+SIZE-buffer-4, y*SIZE+SIZE-9, x*SIZE+SIZE-buffer-2, y*SIZE+SIZE-8, 'white'))
    inner.append(canvas.create_rectangle(x*SIZE+buffer+3, y*SIZE+SIZE-8, x*SIZE+buffer+4, y*SIZE+SIZE-8, 'black'))
    inner.append(canvas.create_rectangle(x*SIZE+SIZE-buffer-4, y*SIZE+SIZE-8, x*SIZE+SIZE-buffer-3, y*SIZE+SIZE-8, 'black'))
    # dots
    inner.append(canvas.create_rectangle(x*SIZE+SIZE-buffer-3, y*SIZE+SIZE-12, x*SIZE+SIZE-buffer-3, y*SIZE+SIZE-12, 'tan'))
    inner.append(canvas.create_rectangle(x*SIZE+SIZE-buffer-8, y*SIZE+SIZE-14, x*SIZE+SIZE-buffer-8, y*SIZE+SIZE-14, 'tan'))
    inner.append(canvas.create_rectangle(x*SIZE+SIZE-buffer-9, y*SIZE+SIZE-6, x*SIZE+SIZE-buffer-9, y*SIZE+SIZE-6, 'tan'))
    inner.append(canvas.create_rectangle(x*SIZE+buffer+1, y*SIZE+SIZE-10, x*SIZE+buffer+1, y*SIZE+SIZE-10, 'tan'))
    # legs
    inner.append(canvas.create_rectangle(x*SIZE+buffer+2, y*SIZE+SIZE-4, x*SIZE+buffer+4, y*SIZE+SIZE-1, 'tan'))
    inner.append(canvas.create_rectangle(x*SIZE+SIZE-buffer-4, y*SIZE+SIZE-4, x*SIZE+SIZE-buffer-2, y*SIZE+SIZE-1, 'tan'))

    return (hitbox, inner)

def draw_row(canvas, blocks, row, skip_idx):
    py = row * SIZE

    # outter floor/ceiling
    for pos in range(1, (CANVAS_WIDTH//SIZE)-1):
        px = pos * SIZE

        if pos not in skip_idx:
            blocks.add(draw_block(canvas, px, py))

def draw_blocks(canvas, blocks, row, place_idx):
    py = row * SIZE

    # outter floor/ceiling
    for pos in range(1, (CANVAS_WIDTH//SIZE)-1):
        px = pos * SIZE

        if pos in place_idx:
            blocks.add(draw_block(canvas, px, py))

def generate_walls(canvas, blocks):
    px = 0

    # outter floor/ceiling
    for pos in range(CANVAS_WIDTH//SIZE):
        px = pos * SIZE
        floor_height = CANVAS_HEIGHT-20
        ceiling_height = 0
        blocks.add(draw_block(canvas, px, floor_height))
        blocks.add(draw_block(canvas, px, ceiling_height))

    # outter left and right walls
    for pos in range(1, (CANVAS_HEIGHT//SIZE)):
        py = pos * SIZE
        left_wall = 0
        right_wall = CANVAS_WIDTH-20
        blocks.add(draw_block(canvas, left_wall, py))
        blocks.add(draw_block(canvas, right_wall, py))
    
    draw_row(canvas, blocks, 38, [37, 38, 39, 40, 41, 42, 43])
    draw_row(canvas, blocks, 34, [1, 2, 3, 40, 41, 42, 43])
    draw_row(canvas, blocks, 28, [37, 38, 39, 40, 41, 42, 43])
    draw_blocks(canvas, blocks, 24, [1, 2, 3])
    draw_row(canvas, blocks, 20, [1, 2, 3, 4, 5, 6, 7, 40, 41, 42, 43])
    draw_row(canvas, blocks, 14, [37, 38, 39, 40, 41, 42, 43])
    draw_row(canvas, blocks, 8,  [1, 2, 3, 40, 41, 42, 43])

    
    for pos in range(8, 39):
        py = pos*SIZE
        tunnel_wall = 40*SIZE
        blocks.add(draw_block(canvas, tunnel_wall, py))


def draw_flag(canvas, col, row):
    px, py = col*SIZE, row*SIZE

    # base
    canvas.create_rectangle(px, py-1, px+SIZE, py-3, 'grey')
    canvas.create_rectangle(px+5, py-4, px+SIZE-5, py-6, 'grey')
    # pole
    id = canvas.create_rectangle(px+8, py-7, px+SIZE-8, py-80, 'black')
    # flag
    canvas.create_rectangle(px, py-81, px+SIZE-8, py-83, 'lightgreen')
    canvas.create_rectangle(px+5, py-84, px+SIZE-8, py-86, 'lightgreen')
    canvas.create_rectangle(px+8, py-87, px+SIZE-8, py-88, 'lightgreen')

    return id

def collision_detection(canvas, player, blocks, enemies, coins, flag, x_dir, y_dir):
    py, py2 = canvas.get_top_y(player), canvas.get_top_y(player) + canvas.get_obj_height(player)
    px, px2 = canvas.get_left_x(player), canvas.get_left_x(player) + canvas.get_obj_width(player)
    touched_flag = False
    touched_coin = False
    alive = True
    killed_enemy = False

    # falling
    if y_dir > 0:
        collisions = canvas.find_overlapping(px, py2+1, px2, py2+2)
        if len(collisions) > 1:
            for coll in collisions:
                if coll in blocks:
                    y_dir = 0
                elif coll == flag:
                    touched_flag = True
                elif coll in coins.keys():
                    touched_coin = True
                    canvas.delete(coll)
                    canvas.delete(coins[coll])
                elif coll in enemies.keys():
                    killed_enemy = True
                    # print('KILLED ENEMY')
                    # print(enemies[coll])
                    for part in enemies[coll]:
                        canvas.delete(part)
                    canvas.delete(coll)

    # up
    if y_dir < 0:
        collisions = canvas.find_overlapping(px, py-1, px2,py-2)
        if len(collisions) > 1:
            for coll in collisions:
                if coll in blocks:
                    y_dir = 0
                elif coll == flag:
                    touched_flag = True
                elif coll in coins.keys():
                    touched_coin = True
                    canvas.delete(coll)
                    canvas.delete(coins[coll])
                elif coll in enemies.keys():
                    alive = False
    
    # right
    if x_dir > 0:
        collisions = canvas.find_overlapping(px2+1, py, px2+2, py2)
        if len(collisions) > 1:
            for coll in collisions:
                if coll in blocks:
                    x_dir = 0
                elif coll == flag:
                    touched_flag = True
                elif coll in coins.keys():
                    touched_coin = True
                    canvas.delete(coll)
                    canvas.delete(coins[coll])
                elif coll in enemies.keys():
                    alive = False
    
    # left
    if x_dir < 0:
        collisions = canvas.find_overlapping(px-1, py, px-2, py2)
        if len(collisions) > 1:
            for coll in collisions:
                if coll in blocks:
                    x_dir = 0
                elif coll == flag:
                    touched_flag = True
                elif coll in coins.keys():
                    touched_coin = True
                    canvas.delete(coll)
                    canvas.delete(coins[coll])
                elif coll in enemies.keys():
                    alive = False

    return (x_dir, y_dir, alive, touched_flag, touched_coin, killed_enemy)

def input_correction(pinputs, delta_x, delta_y):

    # adjust velocity for moving/jumping
    for input in pinputs:
        if input in DIRECTION_MAPPINGS.keys():
            if DIRECTION_MAPPINGS[input] == 'r':
                if delta_x < 25:
                    delta_x += 10
                    if delta_x > 25:
                        delta_x = 25
            elif DIRECTION_MAPPINGS[input] == 'l':
                if delta_x > -25:
                    delta_x -= 10
                    if delta_y < -25:
                        delta_y = -25
            elif DIRECTION_MAPPINGS[input] == 'jump':
                if delta_y == 0:
                    delta_y = 65

    return (delta_x, delta_y)

def gravity_correction(delta_y):
    # gravity
    if delta_y > 0:
        delta_y -= 1
    elif delta_y > -25:
        delta_y -= 5
    elif delta_y > -75:
        delta_y -= 10

    return delta_y

def fade(n):
    res = n

    if res == 0:
        res = 0
    elif res == 25:
        res -= 3
    elif res >= 20:
        res -= 2
    elif res > 0:
        res -= 1
    elif res <= -25:
        res += 3
    elif res <= 20:
        res += 2
    elif res < 0:
        res += 1

    return res

def update_player(canvas, player, pvelocity, pinputs, blocks, enemies, coins, flag_id):
    logs = []
    delta_x, delta_y = pvelocity
    logs.append('initial x:' + str(delta_x) + 'y:' + str(delta_y))

    # gradually slow old velocity
    delta_x, delta_y = fade(delta_x), fade(delta_y)
    logs.append('faded x:' + str(delta_x) + 'y:' + str(delta_y))

    # adjust velocity for player inputs
    delta_x, delta_y = input_correction(pinputs, delta_x, delta_y)
    logs.append('input adj x:' + str(delta_x) + 'y:' + str(delta_y))


    # adjust delta y for gravity
    delta_y = gravity_correction(delta_y)
    logs.append('gravity adj y:' + str(delta_y))
    
    # collision check (0's out negative delta_y)
    x_dir, y_dir = 0, 0
    if delta_x > 0:
        x_dir = 5
    elif delta_x < 0:
        x_dir = -5
    
    if delta_y > 0:
        y_dir = -5
    elif delta_y < 0:
        y_dir = 5

    x_dir, y_dir, alive, touched_flag, touched_coin, killed_enemy = collision_detection(canvas, player['hitbox'], blocks, enemies, coins, flag_id, x_dir, y_dir)

    if y_dir == 0:
        delta_y = 0

    for key in player.keys():
        canvas.move(player[key], x_dir, y_dir)

    # for log in logs:
    #     print(log)

    return ((delta_x, delta_y), alive, touched_flag, touched_coin, killed_enemy)

def calculate_score(enemies_killed, coins_collected, touched_flag):
    res = 0

    if touched_flag:
        res += 100
    
    res += coins_collected*5

    res += enemies_killed*25
    
    return res

def draw_player(canvas, px, py):
    player = {}
    pheight, pwdith = PLAYER_DIMENSIONS
    
    player['hitbox'] = canvas.create_rectangle(px*SIZE, py*SIZE, px*SIZE + pwdith, py*SIZE + pheight, 'sky blue')
    player['hattop'] = canvas.create_rectangle(px*SIZE+3, py*SIZE, px*SIZE+pwdith-3, py*SIZE+1, 'red')
    player['hatbrim'] = canvas.create_rectangle(px*SIZE+2, py*SIZE+2, px*SIZE+pwdith, py*SIZE+3, 'red')
    player['head'] = canvas.create_rectangle(px*SIZE+3, py*SIZE+4, px*SIZE+pwdith-3, py*SIZE+9, 'tan') 
    player['eyewhite'] = canvas.create_rectangle(px*SIZE+pwdith-5, py*SIZE+5, px*SIZE+pwdith-3, py*SIZE+7, 'white')
    player['pupil'] = canvas.create_rectangle(px*SIZE+pwdith-4, py*SIZE+6, px*SIZE+pwdith-3, py*SIZE+7, 'black')
    player['chest'] = canvas.create_rectangle(px*SIZE+2, py*SIZE+10, px*SIZE+pwdith-2, py*SIZE+pheight-7, 'red')
    player['rarm'] = canvas.create_rectangle(px*SIZE+pwdith-1, py*SIZE+10, px*SIZE+pwdith, py*SIZE+pheight-8, 'grey')
    player['larm'] = canvas.create_rectangle(px*SIZE, py*SIZE+10, px*SIZE+2, py*SIZE+pheight-8, 'grey')
    player['rleg'] = canvas.create_rectangle(px*SIZE+pwdith-4, py*SIZE+pheight-7, px*SIZE+pwdith-2, py*SIZE+pheight-2, 'grey')
    player['lleg'] = canvas.create_rectangle(px*SIZE+2, py*SIZE+pheight-7, px*SIZE+4, py*SIZE+pheight-2, 'grey')
    player['rfoot'] = canvas.create_rectangle(px*SIZE+pwdith-4, py*SIZE+pheight-2, px*SIZE+pwdith, py*SIZE+pheight, 'red')
    player['lfoot'] = canvas.create_rectangle(px*SIZE+2, py*SIZE+pheight-2, px*SIZE+6, py*SIZE+pheight, 'red')

    return player

def generate_enemies(canvas, enemies):
    enemy_locs = [
        (8, 27)
    ]

    for loc in enemy_locs:
        x, y = loc
        enemy_id, parts = draw_enemy(canvas, x, y)
        enemies[enemy_id] = parts

def generate_coins(canvas, coins):
    coin_locs = [
        (1, 27), (1, 23), (3, 8), (38, 14), (38, 16), (38, 18),
        (38, 28), (38, 30), (38, 32),
        (38, 38), (38, 40), (38, 42),
        # drop down coins
        (42, 8), (42, 10), (42, 12), (42, 14), (42, 16), (42, 18), 
        (42, 20), (42, 22), (42, 24), (42, 26), (42, 28), (42, 30),
        (42, 32), (42, 34), (42, 36), (42, 38)
    ]

    for loc in coin_locs:
        x, y = loc
        outter, inner = draw_coin(canvas, x, y)
        coins[outter] = inner

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    blocks = set()
    enemies = {}
    coins = {}
    coins_collected = 0
    enemies_killed = 0

    # player variables
    px, py = PLAYER_START_POS
    pvelocity = (0, 0)
    score = 0

    # flag
    gx, gy = FLAG_START_POS

    game_in_progress = True

    draw_background(canvas)
    generate_walls(canvas, blocks)
    generate_coins(canvas, coins)
    generate_enemies(canvas, enemies)
    # print(enemies)
    flag = draw_flag(canvas, gx, gy)
    player = draw_player(canvas, px, py)

    # print(blocks)

    while(game_in_progress):
        pinputs = []
        canvas.update()
        for key in canvas.get_new_key_presses():
            pinputs.append(key.keysym)
        pvelocity, alive, touched_flag, touched_coin, killed_enemy = update_player(canvas, player, pvelocity, pinputs, blocks, enemies, coins, flag)
        time.sleep(DELAY)

        if touched_coin:
            coins_collected += 1
        if killed_enemy:
            enemies_killed += 1

        game_in_progress = alive and not touched_flag

    score = calculate_score(enemies_killed, coins_collected, touched_flag)
    
    canvas.create_text(25*SIZE, 25*SIZE, text="Final Score: "+str(score), anchor='center', font=('Helvetica 15 bold'))

    while(True):
        time.sleep(DELAY)
        canvas.update()  

main()