import numpy as np

class Nurbs:
    def __init__(self, points):
        self.points = np.array([point[0] for point in points])
        self.pesosNurbs = np.array([1, 1, 1.5, 1, 1, 1])        

    # Função para calcular a curva NURBS
    def curva_nurbs(self, pontosControle, pesos, t):
        n = len(pontosControle) - 1
        p = 5  # Grau da curva NURBS

        numPontos = len(t)
        curva = np.zeros((numPontos, 2))

        for i in range(n + 1):
            blend = self.comb(p, i) * (1 - t[:, np.newaxis]) ** (p - i) * t[:, np.newaxis] ** i  # Coeficiente binomial
            curva += blend * pesos[i] * pontosControle[i, :]
        
        return curva
    
        # Função para calcular os coeficientes binomiais
    def comb(self, n, k):
        return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))

    def curve_points(self):
        t = np.linspace(0, 1, 100)

        # Desenho da curva NURBS
        return self.curva_nurbs(self.points, self.pesosNurbs, t)