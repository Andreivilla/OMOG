import numpy as np

class Nurbs5:
    def __init__(self, points):
        self.points = np.array([points[i][0] for i in range(len(points)) if i > 2 and i <9])
        self.weights = np.array([1, 1, 1.5, 1, 1, 1])

    #coeficientes binomiais
    def comb(self, k, i):
        return np.math.factorial(k) / (np.math.factorial(i) * np.math.factorial(k - i))

    def curve_points(self):
        n = len(self.points) - 1
        k = 5  # grau da curva NURBS
        t = np.linspace(0, 1, 100)

        npoints = len(t)
        curve = np.zeros((npoints, 2))

        for i in range(n + 1):
            blend = self.comb(k, i) * (1 - t[:, np.newaxis]) ** (k - i) * t[:, np.newaxis] ** i  # binomial
            curve += blend * self.weights[i] * self.points[i, :]
            
        return curve