import pygame
import sys
from src import Bezier3
from src import Nurbs5
from src import G

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

points = []

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
                if smooth == None:
                    continue
                else:
                    smooth = True
                
    # Limpa a tela
    screen.fill(WHITE)
    #digita legenda
    font = pygame.font.Font(None, 24)
    legend_text = '''
    Clique para gerar os pontos 
    Os 4 primeiros geram a curva bezier 
    Os 4 seguintes geram a curva nurbs 
    C para limpar a tela
    S para suavizar'''
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

    #calcula os pontos da curva de bezier
    if len(points)>3:
        if  len(points) > 8:
            curve_points_nurbs = Nurbs5(points).curve_points()
            pygame.draw.lines(screen, YELLOW, False, curve_points_nurbs, 2)

            #suavizar ao clicar s(smooth)
            if smooth == True:                
                points = G(points).g1()
                points = G(points).g2()
                smooth = None
                

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
