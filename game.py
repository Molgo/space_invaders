from PPlay.window import *
from PPlay.sprite import *
from PPlay.animation import *
from PPlay.gameimage import *
from random import random


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

def projetilInimigo(listaProjInimigos,inimigo,):
    projetilInimigo = Sprite("./assets/enemyShot.png",1)
    projetilInimigo.x = inimigo.x + 50
    projetilInimigo.y = inimigo.y + projetilInimigo.height + 50
    if (random() < 0.3 and len(listaProjInimigos) == 0):
        listaProjInimigos.append(projetilInimigo)
    
def tiroInimigo(janela,listaProjInimigos):
    for i in listaProjInimigos:
        i.y += 500*janela.delta_time()
        i.draw()
        if (i.y>janela.height):
            listaProjInimigos.remove(i)

def gameover():
    janela = Window(1000, 700)
    teclado = janela.get_keyboard()
    fundo = Sprite("./assets/background.png",1)
    gameoverTexto = Sprite("assets/gameOver.png")
    gameoverTexto.set_position(janela.width/2 - gameoverTexto.width/2, janela.width/2 - gameoverTexto.width/2)
    nome = input("Insira seu nome: ")

    while True:
        fundo.draw()
        gameoverTexto.draw()
        janela.update()

        if teclado.key_pressed("ESC"):
            quit()

def criar_inimigos(l, c, spacing):
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

def desenhar_shield(listaShield):
    for shield in listaShield:
        shield.draw()

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

def dano(listaProj, inimigos):

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

def danoPlayer(listaPInimigo, player, invulnerable_time, invulnerable):
    if invulnerable:
        return False
    for proj in listaPInimigo:
        if proj.collided(player):
            listaPInimigo.remove(proj)
            invulnerable_time[0] = 2
            return True
    return False

def danoShield(listaShield, listaPInimigo, listaShieldHelth):
    for index, shield in enumerate(listaShield):
        for proj in listaPInimigo:
            if proj.collided(shield):
                listaPInimigo.remove(proj)
                listaShieldHelth[index] -= 1
                if listaShieldHelth[index] <= 0:
                    listaShield.remove(shield)
                    listaShieldHelth.remove(listaShieldHelth[index])

def danoShieldPlayer(ListaShield, listaP):
    for shield in ListaShield:
        for proj in listaP:
            if proj.collided(shield):
                listaP.remove(proj)


def playGame():

    janela = Window(1000,700)
    janela.set_title("Space invaders")

    teclado = janela.get_keyboard()
    mouseClick = janela.get_mouse()

    fundo = Sprite("./assets/background.png",1)

    player = Sprite("./assets/player.png",1)
    player.x = janela.width/2 - player.width/2
    player.y = janela.height - player.height

    shield1 = Sprite("./assets/shield.png",1)
    shield1.set_position(janela.width/2 - shield1.width/2, player.y - shield1.height * 2)
    shieldHealth1 = 3

    shield2 = Sprite("./assets/shield.png",1)
    shield2.set_position((janela.width/2 - shield2.width/2) - (10 * shield2.width), player.y - shield2.height * 2)
    shieldHealth2 = 3

    shield3 = Sprite("./assets/shield.png",1)
    shield3.set_position((janela.width/2 - shield3.width/2) + (10 * shield3.width), player.y - shield3.height * 2)
    shieldHealth3 = 3

    listaShield = [shield1, shield2, shield3]
    listaShieldHealth = [shieldHealth1, shieldHealth2, shieldHealth3]

    listaP = []
    cooldown = 0

    listaPInimigo = []
    cooldownInimigo = 3

    pontos = 0
    vidas = 3

    invulnerable = False
    invulnerable_time = [0]
    blink_time = 0

    l = 3
    c = 5
    spacing = 20
    direcao_inimigo = "right"
    inimigos = criar_inimigos(l, c, spacing)

    while True:
        delta_time = janela.delta_time()

        fundo.draw()
        
        if invulnerable_time[0] > 0:
            invulnerable_time[0] -= delta_time
            blink_time += delta_time
            if blink_time >= 0.1:
                blink_time = 0
                player.visible = not player.visible
            invulnerable = True
            player.x = janela.width / 2 - player.width / 2
            player.y = janela.height - player.height
        else:
            invulnerable = False
            player.visible = True

        if player.visible:
            player.draw()

        desenhar_shield(listaShield)

        if (teclado.key_pressed("A") or teclado.key_pressed("LEFT")) and not invulnerable:
            player.x -= 300 * janela.delta_time()
        if (teclado.key_pressed("D") or teclado.key_pressed("RIGHT")) and not invulnerable:
            player.x += 300 * janela.delta_time()
        if ((player.x+player.width/2)<0):
            player.set_position(janela.width-player.width/2, player.y)
        if ((player.x+player.width/2)>janela.width): 
            player.set_position(0-player.width/2,player.y)
        if (teclado.key_pressed("SPACE") and cooldown <= 0) or (mouseClick.is_button_pressed(1) and cooldown <= 0) and not invulnerable:
            projetil(player,listaP)
            cooldown = 3    
        cooldown-=5*janela.delta_time()
        tiro(janela,listaP)

        desenhar_inimigo(inimigos)

        direcao_inimigo = movimento_inimgo(inimigos, direcao_inimigo, delta_time)

        if (cooldownInimigo>0):
            cooldownInimigo-=1
        if (cooldownInimigo==0):
            for i in inimigos:
                for j in i:
                    projetilInimigo(listaPInimigo,j)
            cooldownInimigo = 7
        tiroInimigo(janela,listaPInimigo)

        if inimigo_jogador(inimigos, player):
            print("Game Over")
            janela.set_background_color((0,0,0))
            return 0
        
        if dano(listaP, inimigos):
            pontos += 10

        if danoPlayer(listaPInimigo, player, invulnerable_time, invulnerable):
            vidas -= 1
            player.x = janela.width/2
            player.y = janela.height - player.height
            if vidas <= 0:
                gameover()

        danoShield(listaShield, listaPInimigo, listaShieldHealth)
        
        danoShieldPlayer(listaShield, listaP)

        if teclado.key_pressed("ESC"):
            return
        
        janela.draw_text(f"Vidas: {vidas}", janela.width - 120, 10, size=24, color=(255, 255, 255), bold=True)
        janela.draw_text(f"Pontos: {pontos}", janela.width - 140, 40, size=24, color=(255, 255, 255), bold=True)
        
        janela.update()
