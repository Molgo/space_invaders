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
        
def criar_inimigos(l, c, spacing, screen_width=1000):
    inimigos = []
    start_x = spacing // 2
    start_y = 50
    for i in range(l):
        row = []
        for j in range(c):
            monster = Sprite('./assets/enemyRes.png')
            monster.x = start_x + j * (monster.width + spacing)
            monster.y = start_y + i * (monster.height + spacing)
            row.append(monster)
        inimigos.append(row)
    return inimigos

def desenhar_inimigo(inimigos):
    for row in inimigos:
        for monster in row:
            monster.draw()

def movimento_inimgo(inimigos, direction, delta_time, screen_width=1000):
    flag = False

    for row in inimigos:
        for monster in row:
            if direction == "right" and monster.x + monster.width >= screen_width:
                direction = "left"
                flag = True
            elif direction == "left" and monster.x <= 0:
                direction = "right"
                flag = True

    for row in inimigos:
        for monster in row:
            if direction == "right":
                monster.x += 150 * delta_time
            else:
                monster.x -= 150 * delta_time
    if flag:
        for row in inimigos:
            for monster in row:
                monster.y += monster.height // 2

    return direction

def inimigo_jogador(inimigos, player):
    for row in inimigos:
        for monster in row:
            if monster.y + monster.height >= player.y:
                gameover()
    return False

def limpar_inimigo(inimigos):
    for row in inimigos:
        for monster in row:
            row.remove(monster)
        inimigos.remove(row)

def projetil_inimigo(listaProj, inimigos, l, c):

    esquerda = min(monster.x for row in inimigos for monster in row)
    direita = max(monster.x + monster.width for row in inimigos for monster in row)
    topo = min(monster.y for row in inimigos for monster in row)
    base = max(monster.y + monster.height for row in inimigos for monster in row)   

    for proj in listaProj:
        if proj.x > direita or proj.x + proj.width < esquerda or proj.y > base or proj.y + proj.height < topo:
            continue
        else:
            for row in inimigos:
                for monster in row:
                    if proj.collided(monster):
                        listaProj.remove(proj)
                        row.remove(monster)
                        return True
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

    l = 5
    c = 8
    spacing = 20
    direcao_inimigo = "right"
    inimigos = criar_inimigos(l, c, spacing)

    vidas = 3
    pontos = 0

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

        direcao_inimigo = movimento_inimgo(inimigos, direcao_inimigo, delta_time)

        desenhar_inimigo(inimigos)

        if inimigo_jogador(inimigos, player):
            print("Game Over")
            janela.set_background_color((0,0,0))
            return 0
        
        if projetil_inimigo(listaP, inimigos, l, c):
            pontos += 10
            print(pontos)
            print(vidas)

        if not any(inimigos):
            playGame()
        
        if teclado.key_pressed("ESC"):
            return
        
        janela.draw_text(f"Vidas: {vidas}", janela.width - 120, 10, size=24, color=(255, 255, 255), bold=True)
        janela.draw_text(f"Pontos: {pontos}", janela.width - 140, 40, size=24, color=(255, 255, 255), bold=True)
        
        janela.update()