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
wingChordInit = [[0,0,0],[10,-0.3,-0.5],[15,1,0]]



#Returns the shape of the wing a location x from the root, in meters, returns: LEx[m], LEy[m], LEz[m], chord length[m], rotation[rad]
def wingFormat(x):
    x = float(x)
    wingLE = globals()['wingLEInit']
    wingLE = [[float(y) for y in p] for p in wingLE]
    for i in range(len(wingLE)-1):
        if x >= wingLE[i][0] and x <= wingLE[i+1][0]:
            l = (x-wingLE[i][0])/(wingLE[i+1][0]-wingLE[i][0])        
            return x,l*wingLE[i+1][1]+(1-l)*wingLE[i][1],l*wingLE[i+1][2]+(1-l)*wingLE[i][2],l*wingLE[i+1][3]+(1-l)*wingLE[i][3],l*wingLE[i+1][4]+(1-l)*wingLE[i][4]
            
def airfoilThickness(y):
    
    
    
    return upperZ,lowerZ
            
            
            
def sparProperties(x,sparYRootProcent,sparYTipProcent,sparLength):
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
    upperZ,lowerZ = airfoilThickness((y-LEY)/LEChord)*LEChord   # take into account wing twist
    upprZ,lowerZ = upperZ+z, lowerZ+z
    
    return x,y,z,upperZ,lowerZ
    
def sparBendingCheck(x,
    
    
    
    
    


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













