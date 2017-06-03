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
sideslip = 45 #deg
DA_pilot_sideslip = sideslip*(0.235-0.226)/10+0.226 #lin relation assumed (see p. 32 Kilkenny)
#print DAPilotfn
CD0_pilot = DA
CD0_pilot_sideslip = DA_pilot_sideslip/Wing_S

#CD0 wing <-- gaat veel veranderen door airfoil design
CD0_wing = 0.0060 #placeholder, 


#Landing gears -> voegt niks toe aan CD0_clean als ze retractable zijn
wheels = 2.             #-      #amount of wheels    
LG_d  = 0.2             #m      #landing wheel diameter, placeholder value
LG_w  = 0.1             #m      #landing wheel width, placeholder value
LG_S  = LG_d * LG_w     #m2     #frontal area LG
LG_S_sideslip45 = LG_d*LG_w*np.cos(45)*LG_d*np.sin(45)
CD_LG = 0.30            #-      #is 0.15 if we include fairings
CD0_LG = wheels*CD_LG*(LG_S/Wing_S)
CD0_LG_sideslip45 = wheels*CD_LG*(LG_S_sideslip45/Wing_S) # CD_LG assumed to be constant, new value t.b.d.


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
CD0_total_cruise = CD0_pilot + CD0_wing + CD0_LGstruts_cruise + CD0_LG     
CD0_total_sideslip45 = CD0_pilot + CD0_wing + CD0_LGstruts_sideslip45 + CD0_LG  
drag_total_cruise = np.array([["Source","CD0","%of total"],
                   ["Pilot",CD0_pilot,100*CD0_pilot/CD0_total_cruise],
                   ["Wing",CD0_wing,100*CD0_wing/CD0_total_cruise],
                   ["LG",CD0_LG,100*CD0_LG/CD0_total_cruise],
                   ["LG struts",CD0_LGstruts_cruise,100*CD0_LGstruts_cruise/CD0_total_cruise],
                   ["Total",CD0_total_cruise,100]
])
drag_total_sideslip45 = np.array([["Source","CD0","%of total"],
                   ["Pilot",CD0_pilot_sideslip,100*CD0_pilot_sideslip/CD0_total_sideslip45],      
                   ["Wing",CD0_wing,100*CD0_wing/CD0_total_sideslip45],         #wing CD0 for now assumed to be constant in sideslip
                   ["LG",CD0_LG_sideslip45,100*CD0_LG_sideslip45/CD0_total_sideslip45],
                   ["LG struts",CD0_LGstruts_sideslip45,100*CD0_LGstruts_sideslip45/CD0_total_sideslip45],
                   ["Total",CD0_total_sideslip45,100]
])
clean = np.array([["Source","CD0","%of total"],
                   ["Pilot",CD0_pilot,100*CD0_pilot/CD0_clean],
                   ["Wing",CD0_wing,100*CD0_wing/CD0_clean],
                   ["Clean",CD0_clean,100]
])
drag=np.zeros((5,3)) #this is going to be the float array to include all drag configurations,
#currently: column 0 clean, column 1 cruise, column 2 sideslip at 45deg
#drag[[1,2,3,4,5],[1,2]]=
dclean = np.array(clean[1:,1], dtype=float)
print drag[0:2,0]
print dclean[0:2]
drag[0:2,0] = dclean[0:2]
drag[4,0]=dclean[2]
dcruise = np.array(drag_total_cruise[1:,1], dtype=float)
drag[0:5,1] = dcruise
dsideslip45 = np.array(drag_total_sideslip45[1:,1], dtype=float)
drag[0:5,2] = dsideslip45
print drag
