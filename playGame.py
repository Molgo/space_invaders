from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *

def projetil(player,listaProj):
    projetil = Sprite("./assets/shot.png",1)
    projetil.x = player.x + projetil.width * 4
    projetil.y = player.y - projetil.height + 5
    listaProj.append(projetil)
    
def tiro(janela,listaProj):
    for i in listaProj:
        i.y -= 500*janela.delta_time()
        i.draw()
        if (i.y<-50):
            listaProj.remove(i)

def gameover():
    janela = Window(1000, 700)
    teclado = janela.get_keyboard()
    fundo = Sprite("./assets/background.png",1)
    gameoverTexto = Sprite("assets/gameOver.png")
    gameoverTexto.set_position(janela.width/2 - gameoverTexto.width/2, janela.width/2 - gameoverTexto.width/2)

    while True:
        fundo.draw()
        gameoverTexto.draw()
        janela.update()

        if teclado.key_pressed("ESC"):
            return
        
def create_monsters(rows, cols, spacing, screen_width=1000):
    monsters = []
    start_x = spacing // 2
    start_y = 50
    for i in range(rows):
        row = []
        for j in range(cols):
            monster = Sprite('./assets/enemyRes.png')
            monster.x = start_x + j * (monster.width + spacing)
            monster.y = start_y + i * (monster.height + spacing)
            row.append(monster)
        monsters.append(row)
    return monsters

def draw_monsters(monsters):
    for row in monsters:
        for monster in row:
            monster.draw()
def move_monsters(monsters, direction, delta_time, screen_width=1000):
    speed = 100  
    move_down = False

    for row in monsters:
        for monster in row:
            if direction == "right" and monster.x + monster.width >= screen_width:
                direction = "left"
                move_down = True
            elif direction == "left" and monster.x <= 0:
                direction = "right"
                move_down = True

    for row in monsters:
        for monster in row:
            if direction == "right":
                monster.x += speed * delta_time
            else:
                monster.x -= speed * delta_time
    if move_down:
        for row in monsters:
            for monster in row:
                monster.y += monster.height // 2

    return direction

def monsters_reach_player(monsters, player):
    for row in monsters:
        for monster in row:
            if monster.y + monster.height >= player.y:
                gameover()
    return False

def playGame():

    janela = Window(1000,700)
    janela.set_title("Space invaders")

    teclado = janela.get_keyboard()

    fundo = Sprite("./assets/background.png",1)

    player = Sprite("./assets/player.png",1)
    player.x = janela.width/2
    player.y = janela.height - player.height

    listaP = []
    cooldown = 0

    rows = 5
    cols = 8
    spacing = 20
    monster_direction = "right"
    monsters = create_monsters(rows, cols, spacing)

    while True:
        delta_time = janela.delta_time()

        fundo.draw()

        player.draw()
        if (teclado.key_pressed("A") or teclado.key_pressed("LEFT")):
            player.x -= 300 * janela.delta_time()
        if (teclado.key_pressed("D") or teclado.key_pressed("RIGHT")):
            player.x += 300 * janela.delta_time()
        if ((player.x+player.width/2)<0):
            player.set_position(janela.width-player.width/2, player.y)
        if ((player.x+player.width/2)>janela.width): 
            player.set_position(0-player.width/2,player.y)
        if (teclado.key_pressed("SPACE") and cooldown<=0):
            projetil(player,listaP)
            cooldown = 3    
        cooldown-=5*janela.delta_time()
        tiro(janela,listaP)

        monster_direction = move_monsters(monsters, monster_direction, delta_time)

        draw_monsters(monsters)

        if monsters_reach_player(monsters, player):
            print("Game Over")
            janela.set_background_color((0,0,0))
            return 0
        
        if teclado.key_pressed("ESC"):
            return
        
        janela.update()