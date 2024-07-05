from PPlay.window import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *

def dificuldade():

    janela = Window(1000,700)
    janela.set_title("Space invaders")

    mouseClick = janela.get_mouse()
    teclado = janela.get_keyboard()

    janela.set_background_color((0,0,0))

    medium = Sprite("./assets/normalBtn.png",1)
    medium.set_position(janela.width/2 - medium.width/2, janela.height/2 - medium.height/2)
    mediumHover = Sprite("./assets/normalHover.png",1)
    mediumHover.set_position(medium.x, medium.y)

    hard = Sprite("./assets/hardBtn.png",1)
    hard.set_position(medium.x, medium.y + medium.height * 1.5)
    hardHover = Sprite("./assets/hardHover.png",1)
    hardHover.set_position(hard.x, hard.y)

    easy = Sprite("./assets/easyBtn.png",1)
    easy.set_position(medium.x, medium.y - medium.height * 1.5)
    easyHover = Sprite("./assets/easyHover.png",1)
    easyHover.set_position(easy.x, easy.y)

    while True:

        easy.draw()
        medium.draw()
        hard.draw()

        if mouseClick.is_over_object(easy):
                    easyHover.draw()
                    if mouseClick.is_button_pressed(1):
                        pass

        if mouseClick.is_over_object(medium):
                    mediumHover.draw()
                    if mouseClick.is_button_pressed(1):
                        pass

        if mouseClick.is_over_object(hard):
                    hardHover.draw()
                    if mouseClick.is_button_pressed(1):
                        pass
        
        if teclado.key_pressed("ESC"):
            janela.set_background_color((0,0,0))
            return
        
        janela.update()