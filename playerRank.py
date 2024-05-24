from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *

def playerRank():

    janela = Window(1000,700)
    janela.set_title("Space invaders")

    teclado = janela.get_keyboard()

    janela.set_background_color((0,0,0))

    while True:
        
        if teclado.key_pressed("ESC"):
            janela.set_background_color((0,0,0))
            return
        
        janela.update()