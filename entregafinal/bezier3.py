class Bezier3:
    def __init__(self, points):
        self.points = points
        pass

    # Função da curva de Bézier
    def bezier(self, t):
        p0 = self.points[0][0]
        p1 = self.points[1][0]
        p2 = self.points[2][0]
        p3 = self.points[3][0]
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        return x, y
    
    def curve_points(self):
        t = 0.0
        curve = []
        while t < 1.0:
            x,y = self.bezier(t)
            curve.append((int(x), int(y)))
            t += 0.01
        return curve