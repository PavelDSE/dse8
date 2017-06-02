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
#CD_strut = 0.1  
CD_strut_cruise = 0.016          #-      #als de strut een NACA 0025 airfoil is, M=0.11, Re=200,000
CD_strut_sideslip45 = 0.50      # -      #45deg sideslip

#CD_strut = 1.2          #-      #als de strut een cylinder is
LGs_l = 1.              #m      #lengte landing gear, placeholder value
LGs_d_cruise = 0.025           #m      #diameter strut
LGs_d_sideslip45 = LGs_l*np.sin(45)+LGs_d_cruise*np.cos(45)    #m2    #diameter strut seen from flow in 45deg sideslip

LGs_cruise_S = LGs_l*LGs_d_cruise     #m2     #frontal area in cruise
LGs_sideslip45_S = LGs_l*LGs_d_sideslip45     #m2     #frontal area in 45deg sideslip flight
CD0_LGstruts_cruise = LGstruts*CD_strut_cruise*LGs_cruise_S/Wing_S
CD0_LGstruts_sideslip45 = LGstruts*CD_strut_sideslip45*LGs_sideslip45_S/Wing_S

#Total CD0
CD0_clean = CD0_pilot + CD0_wing
CD0_total_cruise = CD0_pilot + CD0_wing + CD0_LGstruts_cruise + CD0_LG     #change _cruise to _sideslip45 to take this flight condition into account
CD0_total_sideslip45 = CD0_pilot + CD0_wing + CD0_LGstruts_sideslip45 + CD0_LG  
drag_total_cruise = np.array([["Source","CD0","%of total"],
                   ["Pilot",CD0_pilot,100*CD0_pilot/CD0_total_cruise],
                   ["Wing",CD0_wing,100*CD0_wing/CD0_total_cruise],
                   ["LG",CD0_LG,100*CD0_LG/CD0_total_cruise],
                   ["LG struts",CD0_LGstruts_cruise,100*CD0_LGstruts_cruise/CD0_total_cruise],
                   ["Total",CD0_total_cruise,100]
])
drag_total_sideslip45 = np.array([["Source","CD0","%of total"],
                   ["Pilot",CD0_pilot,100*CD0_pilot/CD0_total_sideslip45],
                   ["Wing",CD0_wing,100*CD0_wing/CD0_total_sideslip45],
                   ["LG",CD0_LG,100*CD0_LG/CD0_total_sideslip45],
                   ["LG struts",CD0_LGstruts_sideslip45,100*CD0_LGstruts_sideslip45/CD0_total_sideslip45],
                   ["Total",CD0_total_sideslip45,100]
])
clean = np.array([["Source","CD0","%of total"],
                   ["Pilot",CD0_pilot,100*CD0_pilot/CD0_clean],
                   ["Wing",CD0_wing,100*CD0_wing/CD0_clean],
                   ["Clean",CD0_clean,100]
])

print drag_total_cruise
print drag_total_sideslip45
print clean