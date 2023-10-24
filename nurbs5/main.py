import pygame
import sys
from bezier3 import Bezier3
#from nurbs5 import Nurbs5
from nurbs5 import Nurbs5

pygame.init()

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Defina a largura e altura da janela
WIDTH, HEIGHT = 1000, 800

# Crie a janela pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier 3 com Nurbs 5")

points = []
#pontos da curva
# Desenha a curva através dos pontos
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

    # Limpa a tela
    screen.fill(WHITE)
    #digita legenda
    font = pygame.font.Font(None, 24)
    legend_text = '''
    Clique para gerar os pontos 
    Os 4 primeiros gerarão a curva bezier 
    Os 4 seguintes gerarão a curva nurbs 
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

    #calcula os pontos da curva de bezier
    if len(points)>3:
        curve_points_bezier = Bezier3(points).curve_points()
        pygame.draw.lines(screen, RED, False, curve_points_bezier, 2)
    
    #calcula os pontos da curva nurbs
    if len(points)>8:
        curve_points_nurbs = Nurbs5(points).curve_points()
        pygame.draw.lines(screen, YELLOW, False, curve_points_nurbs, 2)

    # Atualize a tela
    pygame.display.flip()

    pygame.time.delay(10)

# Fecha a tela e encerra o programa
pygame.quit()
sys.exit()
