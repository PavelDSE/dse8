# -*- coding: utf-8 -*-
"""
Created on Thu Jun 01 10:07:00 2017

@author: jelle
"""



import numpy as np
from math import *
import matplotlib.pyplot as plt


Wing_b = 15
wingSections= np.arange(0,Wing_b/2,0.01)


wingLEInit = [[0,0,0,1.5,0.3],[5,-0.3,-0.5,1.2,0.1],[7.5,1,0,0,0]]
airfoilC = [[0.0,0.0],[0.0,-0.02],[0.1,-0.08],[0.2,-0.10],[0.3,-0.12],[0.8,-0.05],[1.0,0.0],[0.8,-0.01],[0.5,0.0],[0.0,0.0]]
spar = [0.3,0.3,5]


#Returns the shape of the wing a location x from the root, in meters, returns: LEx[m], LEy[m], LEz[m], chord length[m], rotation[rad]
def wingFormat(x):
    x = float(x)
    wingLE = globals()['wingLEInit']
    wingLE = [[float(y) for y in p] for p in wingLE]
    for i in range(len(wingLE)-1):
        if x >= wingLE[i][0] and x <= wingLE[i+1][0]:
            l = (x-wingLE[i][0])/(wingLE[i+1][0]-wingLE[i][0])        
            return x,l*wingLE[i+1][1]+(1-l)*wingLE[i][1],l*wingLE[i+1][2]+(1-l)*wingLE[i][2],l*wingLE[i+1][3]+(1-l)*wingLE[i][3],l*wingLE[i+1][4]+(1-l)*wingLE[i][4]
            
def airfoilThickness(x,y):    
    if x > Wing_b or x < 0: raise Exception("x out of bound")
    LEX,LEY,LEZ,LEC,LET = wingFormat(x)
    if y > LEY+LEC or y < LEY: raise Exception("y out of bound")
    transform = np.matrix([[cos(LET),sin(LET)],[-sin(LET),cos(LET)]])
    AF = np.matrix(airfoilC)
    y = (y-LEY)/LEC
    AFtwist = AF * transform
    AFtwist = np.array(AFtwist.reshape((len(airfoilC),2)))
    print AFtwist
    first = True
    for i in range(len(airfoilC)-1):
        if y-min(AFtwist[i][0],AFtwist[i+1][0]) >= 0 and y-min(AFtwist[i][0],AFtwist[i+1][0]) < abs(AFtwist[i][0] - AFtwist[i+1][0]):
            if first: 
                first = False
                upperZYcoord = i
            else:
                lowerZYcoord = i
                break
    upperZ = (y-AFtwist[upperZYcoord][0])/(AFtwist[upperZYcoord][0]-AFtwist[upperZYcoord+1][0])*(AFtwist[upperZYcoord][1]-AFtwist[upperZYcoord+1][1])+AFtwist[upperZYcoord][1]
    lowerZ = (y-AFtwist[lowerZYcoord][0])/(AFtwist[lowerZYcoord][0]-AFtwist[lowerZYcoord+1][0])*(AFtwist[lowerZYcoord][1]-AFtwist[lowerZYcoord+1][1])+AFtwist[lowerZYcoord][1]
    
    return upperZ*LEC+LEZ,lowerZ*LEC+LEZ
            
            
            
def sparProperties(x,spar):
    sparYRootProcent,sparYTipProcent,sparLength,sparType,sparDimentions= spar[:4]
    if sparLength > Wing_b: raise Exception("sparLength > Wing_b")
    tipLEX,tipLEY,tipLEZ,tipLEChord,tipLETwist = wingFormat(sparLength)
    tipX = sparLength    
    tipY = tipLEY+cos(tipLETwist)*tipLEChord*sparYTipProcent
    tipZ = tipLEZ+sin(tipLETwist)*tipLEChord*sparZTipProcent
    rootLEX,rootLEY,rootLEZ,rootLEChord,rootLETwist = wingFormat(0)
    rootX = 0
    rootY = sparYRootProcent*cos(rootLETwist)*rootLEChord
    rootZ = sparYRootProcent*sin(rootLETwist)*rootLEChord
    y = x/sparLength * (tipY-rootY)+rootY
    z = x/sparLength * (tipZ-rootZ)+rootZ
    LEX,LEY,LEZ,LEChord,LETwist = wingFormat(x)
    upperZ,lowerZ = airfoilThickness(x,y)   
    
    for i in range(len(sparDimentions)-1):
        if x >= sparDimentions[i][0] and x < sparDimentions[i+1][0]:
            s = i 
            break
        
    xr = (x-sparDimentions[s][0]) / (sparDimentions[s+1][0]-sparDimentions[s][0])
    if sparType == 'Cylinder':
        Ixx = Iyy = I = pi/4 * (((xr * (sparDimentions[i+1][3]-sparDimentions[i][3])+sparDimentions[i][3])**4)-(xr * (sparDimentions[i+1][4]-sparDimentions[i][4])+sparDimentions[i][4])**4))  
    
    
    return x,y,z,upperZ,lowerZ,I
    
    
    
    
    
    
def twistCheck(ribs,spar,stringers): 
    
    momentX = 0
    for i in range(len(ribs)):
        r = -i-1
        momentX += momentX(ribs[r][0])-forceZ(x)*(sparProperties(ribs[r+1][0],spar)[0]-sparProperties(ribs[r][0],spar)[0])
            
    
    
    
    


#wingParameters = {}
#for i in wingSections:
#    wingParameters['wingSections'] += [wingSection[i]]
#    wingParameters['wingShape'] += 
#
#
#wingParameters = {
#    'wingSections': wingSections
#    'wingShape' : 
#        
#    'chordLength' : []
#    'sparLocation': [[0,0.4,0],[0,0.4,0],[0,0.4,0],[0,0.4,0],[0,0.4,0]]
#
#
#}
#
#
#
#
#def wingBendingCheck(wingParameters):
#    













