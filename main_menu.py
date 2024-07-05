from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.mouse import *
import game
import playerRank
import difficulty

def menu():
    janela = Window(1000,700)
    janela.set_title("Space invaders")

    mouseClick = janela.get_mouse()

    janela.set_background_color((0,0,0))

    play = Sprite("./assets/playBtn.png",1)
    play.set_position(janela.width/2 - play.width/2, (janela.height/2 + play.height/2) - play.height * 1.5)
    playHover = Sprite("./assets/playHover.png",1)
    playHover.set_position(play.x, play.y)

    title = Sprite("./assets/title.png")
    title.set_position(janela.width/2 - title.width/2, play.y - title.height * 2)

    dificuldade = Sprite("./assets/difficultyBtn.png",1)
    dificuldade.set_position(play.x, (janela.height/2 + dificuldade.height/2))
    dificuldadeHover = Sprite("./assets/difficultyHover.png",1)
    dificuldadeHover.set_position(dificuldade.x, dificuldade.y)

    ranking = Sprite("./assets/rankingBtn.png",1)
    ranking.set_position(play.x, (janela.height/2 + ranking.height/2) + ranking.height * 1.5)
    rankingHover = Sprite("./assets/rankingHover.png",1)
    rankingHover.set_position(ranking.x, ranking.y)

    sair = Sprite("./assets/exitBtn.png",1)
    sair.set_position(play.x, (janela.height/2 + sair.height/2) + sair.height * 3.0)
    sairHover = Sprite("./assets/exitHover.png")
    sairHover.set_position(sair.x, sair.y)

    while True:

        title.draw()
        play.draw()
        dificuldade.draw()
        ranking.draw()
        sair.draw()

        if mouseClick.is_over_object(play):
                    playHover.draw()
                    if mouseClick.is_button_pressed(1):
                        game.playGame()

        if mouseClick.is_over_object(dificuldade):
                    dificuldadeHover.draw()
                    if mouseClick.is_button_pressed(2):
                        difficulty.dificuldade()

        if mouseClick.is_over_object(ranking):
                    rankingHover.draw()
                    if mouseClick.is_button_pressed(1):
                        playerRank.playerRank()

        if mouseClick.is_over_object(sair):
                    sairHover.draw()
                    if mouseClick.is_button_pressed(1):
                        exit()

        janela.update()
        