import numpy as np

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
    
class G:    #bezier nurbs 
    def __init__(self, points):
        self.points = points
        self.bezier = [points[i][0] for i in range(len(points)) if i < 4]
        self.nurbs = [points[i][0] for i in range(len(points)) if i > 2]

    def build_point(self, x, y, n):
        return ([x, y], f"P{n} ({x}, {y})")
    
    def g1(self):

        bezier_lasts_2 = np.array([self.bezier[i] for i in range(len(self.bezier)) if i > 1]) # 2 3
        nurbs_firts_2 = np.array([self.nurbs[i] for i in range(len(self.nurbs)) if i < 2])#0 1 

        resulting_vector = (nurbs_firts_2[0] - nurbs_firts_2[1]).astype(np.float64)
        resulting_vector_mod = np.linalg.norm( resulting_vector)
        resulting_vector /=  resulting_vector_mod
        position_dir = (bezier_lasts_2[1] - bezier_lasts_2[0]).astype(np.float64)
        position_mag = np.linalg.norm(position_dir)

        new_positionxy = np.append(nurbs_firts_2[0] + (resulting_vector * position_mag), 1)

        self.points[2] = self.build_point(new_positionxy[0], new_positionxy[1], 2)#terceiro ponto da primeira curva
        return self.points
    
    def g2(self):

        bezier_lasts_3 = np.array([self.bezier[i] for i in range(len(self.bezier)) if i > 0]) # 1 2 3
        nurbs_firts_3 = np.array([self.nurbs[i] for i in range(len(self.nurbs)) if i < 3])#0 1 2

        #vetores resultantes vet1 - vet2
        resulting_vector1 = (nurbs_firts_3[0] - nurbs_firts_3[1]).astype(np.float64)
        resulting_vector1 /= np.linalg.norm(resulting_vector1)
        
        resulting_vector2 = nurbs_firts_3[2] - nurbs_firts_3[1]
        resulting_vector2_mag = np.linalg.norm(resulting_vector2)

        resulting_vector3 = (bezier_lasts_3[2] - bezier_lasts_3[1]).astype(np.float64)
        resulting_vector3 /= np.linalg.norm(resulting_vector3)
        
        resulting_vector4 = (bezier_lasts_3[0] - bezier_lasts_3[1]).astype(np.float64)
        resulting_vector4 /= np.linalg.norm(resulting_vector4)

        angle = np.arccos(np.dot(resulting_vector4, resulting_vector3))
        
        if (resulting_vector3[1] >= 0 and resulting_vector4[0] <= 0):
            angle += np.pi

        if (resulting_vector3[1] <= 0 and resulting_vector4[0] >= 0):
            angle += np.pi
        
        #matrix de rotação = 
        #|cos -sen|
        #|sen cos |
        matrix = np.array([
                            [np.cos(angle), -np.sin(angle)], 
                            [np.sin(angle), np.cos(angle)]
                        ],)


        new_vector = np.dot(matrix, resulting_vector1)
        new_vector_mag = new_vector * resulting_vector2_mag
        new_pointxy = nurbs_firts_3[1] + new_vector_mag

        self.points[5] = self.build_point(new_pointxy[0], new_pointxy[1], 2)#terceiro ponto da segunda curva
        return self.points

