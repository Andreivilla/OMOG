import pygame
import sys
import numpy as np
from bezier3 import Bezier3
#from nurbs5 import Nurbs5
from nurbs5 import Nurbs5
from g import G

pygame.init()

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

#define o tamanho da janela 
WIDTH, HEIGHT = 1000, 800

#janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier 3 com Nurbs 5")


smooth = False
#points = []
points = [([88, 536], 'P0 (88, 536)'), ([136, 274], 'P1 (136, 274)'), ([171, 502], 'P2 (171, 502)'), ([220, 227], 'P3 (220, 227)'), ([257, 499], 'P4 (257, 499)'), ([306, 234], 'P5 (306, 234)'), ([330, 432], 'P6 (330, 432)'), ([417, 210], 'P7 (417, 210)'), ([457, 411], 'P8 (457, 411)')]

#pontos da curva
#para poder ter cores diferentes
curve_points_bezier = []
curve_points_nurbs = []
#t = 0.0#t bezier

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            points.append(([mouse_x, mouse_y], f"P{len(points)} ({mouse_x}, {mouse_y})"))
        elif event.type == pygame.KEYDOWN:#ao clicar c(clera) limpa os pontos
            if event.key == pygame.K_c:
                points = []
                curve_points = []
                smooth = False
            if event.key == pygame.K_s:
                smooth = True

    # Limpa a tela
    screen.fill(WHITE)
    #digita legenda
    font = pygame.font.Font(None, 24)
    legend_text = '''
    Clique para gerar os pontos 
    Os 4 primeiros geram a curva bezier 
    Os 4 seguintes geram a curva nurbs 
    C para limpar a tela'''
    lines = legend_text.split('\n')
    line_height = 24  # tamanho da fonte
    xtxt, ytxt = 10, 10
    for line in lines:#gerar o texto guia do programa
        text = font.render(line, True, BLACK)
        screen.blit(text, (xtxt, ytxt))
        ytxt += line_height  #escreve na linha de baixo
    
    # Desenha marcadores nos pontos de controle
    
    for (x, y), _ in points:
        pygame.draw.circle(screen, GREEN, (x, y), 5)

    # Desenha linhas entre os pontos
    if len(points)>1:
        pygame.draw.lines(screen, GREY, False, [p for p, _ in points])

    # Rótulos dos pontos
    font = pygame.font.Font(None, 24)
    for (x, y), label in points:
        text = font.render(label, True, BLACK)
        screen.blit(text, (x + 10, y - 20))

    #Otavio UDESC: G1 o segundo ponto da segunda curva é movido para fazer ele colinear com o penúltimo e último ponto da primeira curva
    #Otavio UDESC: G2 é sobre o ângulo entre os três últimos pontos da primeira curva, que tem que fazer o ângulo dos três primeiros pontos da segunda se igual

    #calcula os pontos da curva de bezier
    #bezier nurbs 
    #zap é nurbs bezier ta td invertido então
    if len(points)>3:
        if  len(points) > 8:
            curve_points_nurbs = Nurbs5(points).curve_points()
            pygame.draw.lines(screen, YELLOW, False, curve_points_nurbs, 2)

            #suavizar ao clicar s(smooth)
            if smooth == True:
                g = G(points)
                points = g.g1()
                points = g.g2() 

            curve_points_bezier = Bezier3(points).curve_points()
        else:
            curve_points_bezier = Bezier3(points).curve_points()
        pygame.draw.lines(screen, RED, False, curve_points_bezier, 2)

    # atualize a tela
    pygame.display.flip()

    pygame.time.delay(10)

# Fecha a tela e encerra o programa
pygame.quit()
sys.exit()
