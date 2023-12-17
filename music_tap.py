# Modules
from random import randint
from time import time
import pgzrun

# Variables
light = Actor("light1", (600, 300))
taps = avali_keys = []
game_over = use_next_light = False
lives = 5
start_time = time()

# Draw
def draw():
    global light, taps, game_over, lives, start_time, final_time
    
    screen.clear()
    screen.fill((25, 25, 25))
    
    if game_over:
        screen.draw.text("GAME OVER!", (200, 200), fontsize=100)
        screen.draw.text(f"Your time: {final_time}", (300, 350), fontsize=35)
    else:
        light.draw()
        screen.draw.text(f"Lives: {lives}", (650, 10))
        screen.draw.text(f"Time: {round(time()-start_time, 3)}", (650, 30))
        for tap in taps:
            tap.draw()

# Tap summoning
def summon():
    global taps
    rand_num = randint(0, 3)
    taps.append(Actor(["left", "right", "down", "up"][rand_num], (rand_num*150+75, 0)))
    clock.schedule(summon, randint(4, 8)/8+3/((time()-start_time)/4))

clock.schedule(summon, 4)

# Tap updating
def update_taps():
    global game_over, taps, avali_keys, lives, final_time
    if not game_over:
        for index in range(len(taps)):
            try:
                taps[index].y += 6.5+0.05*(time()-start_time)
                if taps[index].y > 525:
                    avali_keys.append(taps[index].image)
                if taps[index].y > 675:
                    avali_keys.remove(taps[index].image)
                    taps[index] = None
                    lives -= 1
                    if lives == 0:
                        game_over = True
                        music.stop()
                        final_time = round(time()-start_time, 3)
            except:
                continue
                
    taps = list(filter(lambda tap: tap!=None, taps))
    clock.schedule(update_taps, 1/65)

update_taps()

# Light updating
def next_light():
    global use_next_light, light
    
    if use_next_light:
        use_next_light = False
        light.image = "light1"
    else:
        use_next_light = True
        light.image = "light2"

clock.schedule_interval(next_light, 0.2)

# Key clicking
def check_key(key: str):
    global taps, avali_keys, lives, game_over, final_time
    if key in avali_keys:
        avali_keys.remove(key)
        for index in range(len(taps)):
            if taps[index].y > 525 and taps[index].image == key:
                taps[index] = None
                break
    else:
        lives -= 1
        if lives == 0:
            game_over = True
            music.stop()
            final_time = round(time()-start_time, 3)

def on_key_up(key):
    global lives, game_over
    if not game_over:
        if key == keys.LEFT:
            check_key("left")
        elif key == keys.RIGHT:
            check_key("right")
        elif key == keys.DOWN:
            check_key("down")
        elif key == keys.UP:
            check_key("up")

# Music
music.play("music")
pgzrun.go()