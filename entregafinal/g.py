import numpy as np

class G:    #bezier nurbs 
    def __init__(self, points):
        self.points = points
        self.bezier = [points[i][0] for i in range(len(points)) if i < 4]#self.build_curve_points(0, 3)
        self.nurbs = [points[i][0] for i in range(len(points)) if i > 3]
        #print('points: {}'.format(points))
        
        #print('nurbs: {}'.format(nurbs))
        #print('bezier: {}'.format(bezier))

    def build_point(self, x, y, n):
        return ([x, y], f"P{n} ({x}, {y})")
    

    #points
    #Otavio UDESC: G1 o segundo ponto da segunda curva é movido para fazer ele colinear com o penúltimo e último ponto da primeira curva
    #Otavio UDESC: G2 é sobre o ângulo entre os três últimos pontos da primeira curva, que tem que fazer o ângulo dos três primeiros pontos da segunda se igual
    def g1(self):
        #G1 o segundo ponto da segunda curva é movido para fazer ele colinear com o penúltimo e último ponto da primeira curva
        
        x1, y1 = self.nurbs[0]
        x2, y2 = self.nurbs[1]

        x = 2*x2 - x1
        y = 2*y2 - y1

        self.bezier[2] = [x, y]
        self.points[2] = self.build_point(x, y, 2)
        return self.points
    
    def g2(self):

        bezier_lasts_3 = np.array([self.bezier[i] for i in range(len(self.bezier)) if i > 0]) # 1 2 3
        nurbs_firs_3 = np.array([self.nurbs[i] for i in range(len(self.nurbs)) if i < 3])#0 1 2

        a_2 = (nurbs_firs_3[0] - nurbs_firs_3[1]).astype(np.float64)
        #a_2 = a_2.astype(np.float64)
        a_2 /= np.linalg.norm(a_2)
        b_2 = nurbs_firs_3[2] - nurbs_firs_3[1]
        b_2_mag = np.linalg.norm(b_2)

        a_1 = (bezier_lasts_3[2] - bezier_lasts_3[1]).astype(np.float64)
        #a_1 = a_1.astype(np.float64)
        a_1 /= np.linalg.norm(a_1)
        b_1 = (bezier_lasts_3[0] - bezier_lasts_3[1]).astype(np.float64)
        b_1 /= np.linalg.norm(b_1)

        angle = np.arccos(np.dot(b_1, a_1))
        if all(
            (
                a_1[1] >= 0,
                b_1[0] <= 0,
            ),
        ) or all(
            (
                a_1[1] <= 0,
                b_1[0] >= 0,
            ),
        ):

            angle += np.pi

        rotation_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
        )

        new_b_2 = np.dot(rotation_matrix, a_2)

        new_b_2_mag = new_b_2 * b_2_mag
        new_point = nurbs_firs_3[1] + new_b_2_mag

        #print('points: {}'.format(new_point))

        self.points[2] = self.build_point(new_point[0], new_point[1], 2)
        #state.curves[curva_2_index].points[2] = np.append(new_point, 1)

        #return self.points
        #G2 é sobre o ângulo entre os três últimos pontos da primeira curva, 
        # #que tem que fazer o ângulo dos três primeiros pontos da segunda se igual
        #angle_a = np.arctan2(self.nurbs[2][1] - self.nurbs[1][1], self.nurbs[2][0]-self.nurbs[1][0])
        #angle_b = np.arctan2(self.nurbs[3][1] - self.nurbs[2][1], self.nurbs[3][0]-self.nurbs[2][0])

        #ultimos 3 pontos da primeira curva
        #angle_a = np.arctan2(self.nurbs[0][1] - self.nurbs[0][1], self.nurbs[0][0] - self.nurbs[0][1])
        #angle_b = np.arctan2(self.nurbs[1][1] - self.nurbs[1][1], self.nurbs[1][0] - self.nurbs[1][0])
        #angle_c = np.arctan2(self.nurbs[2][1] - self.nurbs[2][1], self.nurbs[2][0] - self.nurbs[2][0])

        #calculo para os pontos de bezier
        #length = 1
        
        #points[5], points[6], points[7] = g.g2()
        #x, y = int(self.nurbs[1][0] + length*np.cos(angle_b)), int(self.nurbs[1][1] + length*np.sin(angle_b))
        #self.points[1] = self.build_point(x, y, 1)

        #x, y = int(self.nurbs[1][0] - length*np.cos(angle_b)), int(self.nurbs[1][1] - length*np.sin(angle_b))
        #self.points[2] = self.build_point(x, y, 2)

        #x, y = (int(self.nurbs[2][0] + length*np.cos(angle_c)), int(self.nurbs[2][1] + length*np.sin(angle_c)))
        #self.points[3] = self.build_point(x, y, 3)


        return self.points
        #return self.bezier[3], self.bezier[4], self.bezier[5]

        #print(angle_a)
