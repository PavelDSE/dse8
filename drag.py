# -*- coding: utf-8 -*-
"""
Hier gaat team aero een poging doen de drag zo goed mogelijk te benaderen
"""

#imports
import numpy as np

#inputs from parameters
from parameters import Wing_S

#atmospheric properties


#Pilot, uit midterm report
DA = 0.1978 #m2
CD0_pilot = DA/Wing_S


#CD0 wing <-- gaat veel veranderen door airfoil design
CD0_wing = 0.0060 #placeholder, 


#Landing gears -> voegt niks toe aan CD0_clean als ze retractable zijn
wheels = 2.             #-      #amount of wheels    
LG_d  = 0.2             #m      #landing wheel diameter, placeholder value
LG_w  = 0.1             #m      #landing wheel width, placeholder value
LG_S  = LG_d * LG_w     #m2     #frontal area LG
CD_LG = 0.30            #-      #is 0.15 if we include fairings
CD0_LG = wheels*CD_LG*(LG_S/Wing_S)


#LG Struts
LGstruts = 2.           #-      #amount of struts
CD_strut = 0.1          #-      #als de strut een airfoil is
#CD_strut = 1.2          #-      #als de strut een cylinder is
LGs_l = 1.              #m      #lengte landing gear, placeholder value
LGs_d = 0.025           #m      #diameter strut
LGs_S = LGs_l*LGs_d     #m2     #frontal area
CD0_LGstruts = LGstruts*CD_strut*LGs_S/Wing_S


#Total CD0
CD0_clean = CD0_pilot + CD0_wing
CD0_total = CD0_pilot + CD0_wing + CD0_LGstruts + CD0_LG 

total = np.array([["Source","CD0","%of total"],
                   ["Pilot",CD0_pilot,100*CD0_pilot/CD0_total],
                   ["Wing",CD0_wing,100*CD0_wing/CD0_total],
                   ["LG",CD0_LG,100*CD0_LG/CD0_total],
                   ["LG struts",CD0_LGstruts,100*CD0_LGstruts/CD0_total],
                   ["Total",CD0_total,100]
])

clean = np.array([["Source","CD0","%of total"],
                   ["Pilot",CD0_pilot,100*CD0_pilot/CD0_clean],
                   ["Wing",CD0_wing,100*CD0_wing/CD0_clean],
                   ["Clean",CD0_clean,100]
])

print total
print clean