import pygame
import sys

pygame.init()

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

# Defina a largura e altura da janela
WIDTH, HEIGHT = 800, 600

# Crie a janela pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curva de Bézier")

# Função da curva de Bézier
def bezier(points, t):
    p0 = points[0][0]
    p1 = points[1][0]
    p2 = points[2][0]
    p3 = points[3][0]
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return x, y

points = []
#pontos da curva
# Desenha a curva através dos pontos
curve_points = []
t = 0.0#t bezier

# Variável para controlar o movimento do ponto (None para nenhum, índice para o ponto em movimento)
moving_point = None

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
    legend_text = "C para limpar a tela"
    text = font.render(legend_text, True, BLACK)
    screen.blit(text, (10, 10))

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

    if len(points)>3:
        #x, y = bezier(*[p for p, _ in points], t)
        x,y = bezier(points,t)
        #print(*[p for p, _ in points])
        curve_points.append((int(x), int(y)))        


    if len(curve_points) > 1:
        pygame.draw.lines(screen, RED, False, curve_points, 2)

    if t < 1.0:
        t += 0.01
    else:
        pygame.time.wait(1000)#para por 1(1000ms) segundo para visualizar a curva
        t = 0.0
        curve_points = []
    

    # Atualize a tela
    pygame.display.flip()

    pygame.time.delay(10)

# Fecha a tela e encerra o programa
pygame.quit()
sys.exit()
