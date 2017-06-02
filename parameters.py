"""
Hier alle parameters uit par_C7.py en par_allconcepts

Dit heb ik gedownload van de drive op 1 juni 13:30
Als je veranderingen gemaakt hebt daarna staan die hier dus nog niet in

Als je niet meer weet of je iets aangepast hebt valt het te mergen, doe dit voorzichtig (of vraag het even aan Rens)
Cheers


"""

import numpy as np




### Constants
g = 9.80665                                        #[m/s2]     Gravitational acc. Frank 10-5   
rho = 0.9046                                       #[kg/m3]    Assumption ISA 10000 ft. Frank 10-5
rho_0 = 1.225                                      #[kg/m3]    Assumption ISA Sea-Level. Frank 10-5
a_0 = 343.                                           #[m/s]     Ground level speed of sound. Rens 16-5
a_0ft = 1125.                                        #[ft/s]   #speed of sound in amerika yolo units. Rens 16-5
visc_0 = 1.789 * 10**-5                             #?          dynamic viscosity at sea level

### Requirements
V_stall_max = 25.*0.514444444                      #[m/s]      Cruise speed - requirement. Frank 10-5
climbrate = 1.3                                    #[m/s]      climb rate - 1000 ft. in 4 min. Frank
s_land = 80.                                       #[m]        Landing distance - assumption - Frank
n_max = 2.                                         #[-]        Performance maximum load factor - Frank
n_max_struc = 6.                                   #[-]        Structural maximum load factor - Frank
n_ult = 9.                                         # [-]       ultimate load factor - Frank
fl_time = 30.                                      #[min]      Flight time from requirements
weight_pilot_max = 85.                             #[kg]       Maximum pilot weight - requirements - Frank
weight_pilot_min = 65.                             #[kg]       Minimum pilot weight - requirements - Frank
pilot_length_average = 1.75                        #[m]        From requirements

### Right now, equal for every concept
TOP = 15.                                          #[-]        DIKKE GOK VAN RANDOM PLAATJE UIT ADSEE 1 SLIDES LECTURE 3 - Frank
f = 1.                                             #[-]        W_TO/W_L - no fuel - Frank
sigma = 1.                                         #[-]        only 1 if TO @ ground level - Frank

### propeller estimations, gelijk overal nu voor noise estimation
r_prop          = 2.3              #ft     #propeller radius, zelfde als e-lift
rpm             = 1950.            #-      #rotation propeller, zelfde als e-lift
blades          = 3.               #-      #number of propeller blades, schatting



concept = "Bird"

#V_cruise = 75.* 0.514444444                       #[m/s]      Cruise speed. Frank 10-5
V_cruise = 55 * 0.514444444                        #[m/s]      Cruise speed. Dikke snelheids verandering - Frank 15-5

#weight_OEW = 50.                                   #[kg]       Operational empty weight - REF data.- Frank 15-5
#weight_OEW = 49.                                   #[kg]        from Structures Jelle & Mariska - Operational empty weight - REF data.- Frank 15-5
weight_OEW = 58.                                   #[kg]        from Structures Jelle & Mariska - Operational empty weight - REF data.- Frank 15-5


weight_TO = (weight_OEW + weight_pilot_max) * g    #[N]        Take off weight - Frank

A = 11.                                             #[-]        aspect ratio - REF data - Frank 15-5

#Wing_S = 16.3101712222                            #[m2]       Wing area
Wing_S = 13.5427                                   #[m2]       Wing Area - Frank 15-5

Wing_b = np.sqrt(A*Wing_S)                         #[m]        Span - From aspect ratio and wing area - Frank 15-5

Wing_c = Wing_b/A                                  #[m]        Chord length from aspect and wing area - Frank 15-5

#C_Lmax_clean = 1.9                                 #[-]        REF data - Gok - Frank
C_Lmax_clean = 1.2                                 #[-]         MOET NOG GECHECKT WORDEN REF data - Gok - Frank     (Betere) REF data na praatje met Joris  - Gok - Frank 30 - 5                     
                    
                         
#C_Lmax_takeoff = 1.9                               #[-]        REF data - Gok - Frank
C_Lmax_takeoff = 1.2                                 #[-]         MOET NOG GECHECKT WORDEN REF data - Gok - Frank     (Betere) REF data na praatje met Joris  - Gok - Frank 30 - 5                     
              

#C_Lmax_landing= 1.8                               #[-]        REF data - Gok - Frank
#C_Lmax_landing= 2.0                                #[-]        REF data - Gok - Frank
C_Lmax_landing = 1.6                                 #[-]         MOET NOG GECHECKT WORDEN REF data - Gok - Frank     (Betere) REF data na praatje met Joris  - Gok - Frank 30 - 5                     
                    


C_L_alpha = 2 * np.pi   	                          #[-]        DIKKE GOK van flat plate theory - Frank

e_clean = 0.85                                      #[-]        Roskam ADSEE 1 slides - Frank

#C_D0_clean = 0.01                                 #[-]         Dikke gok - Frank - 10-5
#C_D0_clean = 0.15                                 #[-]         Schattting. Zie aerodynamics -> drag tradeoff - Rens - 15-5
#C_D0_clean = 0.021                                #[-]         #Nieuwe schatting van Rgoier 17- 5 ##Schattting. Zie aerodynamics -> drag tradeoff - Rens - 15-5
#C_D0_clean = 0.0307                                 #[-]         Nieuwe betere schattting. Zie aerodynamics -> drag tradeoff - Rens - 18-5
C_D0_clean = 0.06                                  #[-]         Nieuwe schatting over C_D0 na praatje met Joris Frank & Rens - 31 - 5 



delta_e_takeoff = 0.                               #[-]         no flaps - Frank
  
delta_e_landing = 0.                               #[-]         no flaps - Frank
 
delta_C_D0_takeoff = 0.                            #[-]         no flaps - Frank

delta_C_D0_landing = 0.                            #[-]         no flaps - Frank

efficiency_prop = 0.8                              #[-]        prop. effiency - DIKKE GOK - Frank

########### Waardes vanuit P&P: ############

V_stall = 9.4329                                    #[m/s]       Wing sizing estimation. Frank 15-5
 
V_max = 34.2                                     #[m/s]       Power estimation. Frank 15-5

#P_a = 9557.6211097                               #[W]         Power available
P_a = 10419.6299                                  #[W]         Power available - Frank - power calculations

#CL_mindrag = 0.531736155272                      #[-]         CL @ minimum drag 
CL_mindrag = 0.9496                                #[-]         CL @ minimum drag - Frank 15-5

#CD_mindrag = 0.02                                #[-]         CD @ minimum drag         
CD_mindrag = 0.0614                                  #[-]         CD @ min. drag - Frank 15-5

CLCD_mindrag = 15.4661                             #[-]         CL/CD for min drag (optimal Cl/CD) Frank 15-5

#V_mindrag = 16.9159263147                        #[m/s]       V  @ minimum drag
V_mindrag = 13.3428                               #[m/s]       V  @ minimum drag from drag diagram - Frank 15-5

#D_min = 57.1723743512                            #[N]         The minimum drag (steady symmetric flight)
D_mindrag = 90.6724                              #[N]         The minimum drag (steady symmetric flight) - Frank - 15-5

P_mindrag = 1209.825                             #[W]         Power required during min. drag flight - Frank - 15-5
 
#CL_minpower = 0.920994037152                     #[-]         CL @ minimum power required
CL_minpower = 1.6448                               #[-]         CL @ minimum power required from power diagram - Frank 15-5

#CD_minpower = 0.04                               #[-]         CD @ minimum power required
CD_minpower = 0.1228                                 #[-]         CD @ minimum power required from power diagram - Frank 15-5

CLCD_minpower = 13.3941                            #[-]         CL/CD for min power (optimal Cl^3/CD^2) Frank 15-5

#V_minpower = 12.8533244698                       #[m/s]       V  @ minimum power required
V_minpower = 10.1384                                #[m/s]       V  @ minimum power required - Frank 15-5

D_minpower = 104.6995                             #[N]         Min. drag during min. power flight - Frank 15-5

#P_r_min = 848.537541237                          #[W]         The minimum power required (steady symmetric flight)
P_minpower = 1061.4802                            #[W]         The minimum power required (steady symmetric flight) - Frank 15-5

P_climbrate = 2884.5364                           #[W]          Power required for 1.3 m/s climbrate from power diagram - Frank 15-5

Max_climbrate = 6.6732                           #[m/s]        Max climbrate Frank from power diagram - Frank 15-5

Batcap_30min_cruise = 0.5307                      #[kWh]        Battery capacity for 30 min cruise from Power diagram - Frank 15-5

Batcap_4min_climb = 0.1923                        #[kWh]        Battery capacity for 4 min. 1.3 m/s climb from power diagram - Frank 15-5

#Einde waardes vanuit P&P

noise = 82.800                                    #[dB]       Noise at 200ft, uit noise2.py. Rens 17-5
