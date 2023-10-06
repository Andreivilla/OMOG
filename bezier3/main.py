import pygame
import sys

# Inicialize o Pygame
pygame.init()

# Defina as cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

# Defina a largura e altura da janela
WIDTH, HEIGHT = 800, 600

# Crie a janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curva de Bézier Cúbica Interativa")

# Função para calcular os pontos da curva de Bézier
def bezier(p0, p1, p2, p3, t):
    x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    return x, y

# Defina os quatro pontos de controle e seus rótulos
p0 = [100, 300]
p1 = [300, 100]
p2 = [500, 500]
p3 = [700, 300]

p0_label = "P0 (100, 300)"
p1_label = "P1 (300, 100)"
p2_label = "P2 (500, 500)"
p3_label = "P3 (700, 300)"

# Lista para armazenar os pontos de controle e seus rótulos
points = [(p0, p0_label), (p1, p1_label), (p2, p2_label), (p3, p3_label)]

# Variável para controlar o progresso da curva
t = 0.0

# Lista para armazenar o histórico de pontos da curva
curve_points = []

# Variável para controlar o movimento do ponto (None para nenhum, índice para o ponto em movimento)
moving_point = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Verifique se o mouse foi pressionado perto de algum ponto de controle
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, (point, _) in enumerate(points):
                if abs(mouse_x - point[0]) <= 10 and abs(mouse_y - point[1]) <= 10:
                    moving_point = i
        elif event.type == pygame.MOUSEBUTTONUP:
            # Pare de mover o ponto quando o mouse é liberado
            moving_point = None

    # Se um ponto está sendo movido, atualize sua posição com a posição atual do mouse
    if moving_point is not None:
        x, y = pygame.mouse.get_pos()
        points[moving_point] = ([x, y], f"P{moving_point} ({x}, {y})")

        # Recalcule a curva quando um ponto de controle for movido
        curve_points = []
        for t in range(101):
            t /= 100
            x, y = bezier(*[p for p, _ in points], t)
            curve_points.append((int(x), int(y)))

    # Limpe a tela
    screen.fill(WHITE)

    # Desenhe marcadores nos pontos de controle
    for (x, y), _ in points:
        pygame.draw.circle(screen, GREEN, (x, y), 5)

    # Desenha linhas entre os pontos
    pygame.draw.lines(screen, GREY, False, [p for p, _ in points])

    # Desenhe rótulos dos pontos
    font = pygame.font.Font(None, 24)
    for (x, y), label in points:
        text = font.render(label, True, BLACK)
        screen.blit(text, (x + 10, y - 20))

    # Desenhe o rastro da curva
    if len(curve_points) > 1:
        pygame.draw.lines(screen, RED, False, curve_points, 2)

    # Atualize a tela
    pygame.display.flip()

    pygame.time.delay(10)

# Encerre o Pygame
pygame.quit()
sys.exit()
