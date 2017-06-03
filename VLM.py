# -*- coding: utf-8 -*-
"""
Hier een poging tot Vortex Lattice Method voor ons planform
De methode is gekopieerd van een gozer op github, directory aqreed/PyVLM
"""

#imports
import numpy as np



###### PyVLM / geometry.py


#Cross-product
def cross_prod(a,b):
    x = a[0]*b[1] - a[1]*b[0]
    return x


#Dot product
def vect_dot(a,b):
    x = a[0]*b[0] + a[1]*b[1] 
    return x


#Normalized direction vector van A naar B
def norm_dir_vect(A,B):
    AB = B - A
    a = AB / (AB.dot(AB))**0.5
    return a
   
   
#Afstand tussen een punt en een rechte lijn
def dist_point2line(P,A,B):
    AB = B - A
    PB = B - P
    a = AB / (AB.dot(AB))**0.5
    b = np.empty_like(a)
    b[0] = a[1]
    b[1] = -a[0]
    
    if cross_prod(PB,a) == 0:
        d = 0
    else:
        d = abs(vect_dot(PB,b))
    return d


#Area van een polygon met 4 hoeken in 2D
def area_4points(A,B,C,D):
    S = cross_prod(A,B) + cross_prod(B,C) + \
        cross_prod(C,D) + cross_prod(D,A)
    S *= 0.5
    return abs(S)
    
    
    
###### PyVLM / vortices.py
    

#define position of the horseshoe vortex  
def vortex_position_in_panel(P1,P2,P3,P4):
    
    P1P2 = P2 - P1
    P3P4 = P4 - P3
    P1P4 = P4 - P1
    
    A = P1 + P1P2 / 4
    B = A + P1P2 / 2
    C = P3 + P3P4 / 4
    D = C + P3P4 / 2
    AD = D - A
    P = A + AD / 2
    
    results = [P,A,B,C,D]
    return results


#induced velocity at point P due to horeshoe vortex
def v_induced_by_horseshoe_vortex(P,A,B,C,D,gamma=1):
    
    pi = np.pi
    epsilon = 1e-3
    i_1 = np.array([-1,0])
    i_2 = norm_dir_vect(B,C)
    i_3 = np.array([1,0])

    #vortex Inf->A->B
    i_PB = norm_dir_vect(P,B)
    h_1 = dist_point2line(P,A,B)
    if h_1 < epsilon:
        v_1 = 0
    else:
        sign_1 = np.sign(cross_prod(i_PB,i_1))
        cos_2 = vect_dot(-i_PB,i_1)
        v_1 = sign_1 * (gamma/(4*pi*h1)) * (1-cos_2)
    
    #vortex B->C
    i_PC = norm_dir_vect(P,C)
    h_2 = dist_point2line(P,B,C)
    if h_2 < epsilon:
        v_2 = 0
    else:
        sign_2 = np.sign(cross_prod(i_PC,i_2))
        cos_1 = vect_dot(-i_PB,i_2)
        cos_2 = vect_dot(-i_PC,i_2)
        v_2 = sign_2 * (gamma/(4*pi*h_2)) * (cos_1 - cos_2)
    
    #vortex C->D->Inf
    h_3 = dist_point2line(P,C,D)
    if h_3 < epsilon:
        v_3 = 0
    else:
        sign_3 = np.sign(cross_prod(i_PC,i_3))
        cos_1 = vect_dot(-i_PC,i_3)
        v_3 = sign_3 * (gamma/(4*pi*h_3)) * (cos_1 + 1)
    
    #return total induced velocities
    v_trail = v_1 + v_3
    v_total = v_trail + v_2
    return v_total, v_trail
    

#induced velocity at point P due to a straight line vortex
def v_induced_by_finite_vortex_line(P,A,B,gamma=1):
    
    i = norm_dir_vect(A,B)
    i_PA = norm_dir_vect(P,A)
    i_PB = norm_dir_vect(P,B)
    
    h = dist_point2line(P,A,B)
    sign = np.sign(cross_prod(i_PA,i))
    cos_1 = vect_dot(-i_PA,i)
    cos_2 = vect_dot(-i_PB,i)
    
    v = sign * (gamma/(4*pi*h)) * (cos_1 - cos_2)
    return v
    


###### PyVLM / panel.py


class Panel(object):
    
    #hoekpunten
    def __init__(self,P1,P2,P3,P4):
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4
    
    #area
    def area(self):
        return area_4points(self.P1,self.P2,self.P3,self.P4)
        
    #span (must be constant along panel)
    def span(self):
        b = self.P3[1] - self.P2[1]
        return abs(b)
    
    #x,y coordinates of the horseshoe corners and conctrol point
    def _vortex_position(self):
        points = vortex_position_in_panel(self.P1,self.P2,self.P3,self.P4)
        return points
    
    #x,y coordinates of the control point
    def control_point(self):
        control_point_position = self._vortex_position()[0]
        return control_point_position
    
    #induced velocity by horseshoe and bounded segment at controll point
    def induced_velocity(self, control_point_pos):
        _points_vortex = self._vortex_position()
        v = v_induced_by_horseshoe_vortex(control_point_pos,
                                          _points_vortex[1],
                                          _points_vortex[2],
                                          _points_vortex[3],
                                          _points_vortex[4])
        return v[0],v[1]
    
        

###### PyVLM / mesh_generator.py

#generates mesh
class Mesh(object):
    
    #object parametres
    def __init__(self, leading_edges, chords, n, m):
        self.leading_edges = leading_edges
        self.chords = chords
        self.n = n
        self.m = m
        self.mesh_points = []
        self.mesh_panels = []
        self.panel_pos_chordwise = []
        self.panel_span = []
    
    
    #list with points x,y coordinates
    def points(self):
        
        Pi = self.leading_edges[0]
        Pf = self.leading_edges[1]
        chord_1 = np.array([self.chords[0],0])
        chord_2 = np.array([self.chords[1],0])
        n = self.n
        m = self.m
        
        for i in range(0, n+1):
            PiPf = Pf - Pi
            P = Pi
            for j in range(0, m+1):
                self.mesh_points.append(P)
                P = P + PiPf / m
            Pi = Pi + chord_1 / n
            Pf = Pf + chord_2 / n
            
        return self.mesh_points
        
    
    #list with panel corner coordinates
    def panels(self):
        
        n = self.n
        m = self.m 
        N_panels = n * m
        
        for i in range(0, N_panels):
            k = int(i/m)
            P1 = self.mesh_points[i + k + m + 1]
            P2 = self.mesh_points[i + k]
            P3 = self.mesh_points[i + k + 1]
            P4 = self.mesh_points[i + k + m + 2]
            
            self.mesh_panels.append([])
            self.mesh_panels[i].append(P1)
            self.mesh_panels[i].append(P2)
            self.mesh_panels[i].append(P3)
            self.mesh_panels[i].append(P4)