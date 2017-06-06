# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:14:36 2017

@author: Frank
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp
import math


def PowerWing():
    
    W_S = np.arange(1,350,1)            #[N/m²]     Wing loading

    ## CL-CD CLEAN CONFIG. ##
    C_L_clean = np.arange(0, C_Lmax_clean, 0.01)
    C_D_clean = C_D0_clean + ((C_L_clean**2)/(np.pi * A * e_clean))


    ## CL-CD TAKEOFF CONFIG. ##
    e_takeoff = e_clean + delta_e_takeoff #Roskam ADSEE 1 slides #0.05
    C_D0_takeoff = C_D0_clean + delta_C_D0_takeoff #ADSEE 1 slides #0.010 + 0.025

    C_L_takeoff = np.arange(0, C_Lmax_takeoff, 0.01)
    C_D_takeoff = C_D0_takeoff + ((C_L_takeoff**2)/(np.pi * A * e_takeoff))


    ## CL-CD LANDING CONFIG ##
    e_landing = e_clean + delta_e_landing #Roskam ADSEE 1 slides #0.10
    C_D0_landing = C_D0_clean + delta_C_D0_landing #ADSEE 1 slides #0.055 + 0.025

    C_L_landing = np.arange(0, C_Lmax_landing, 0.01)
    C_D_landing = C_D0_landing + ((C_L_landing**2)/(np.pi * A * e_landing))


    ## DESIGN FOR STALL SPEED ##
    W_S_stall_clean = 0.5 * rho_0 * (V_stall_max **2.) * C_Lmax_clean
    W_S_stall_takeoff = 0.5 * rho_0 * (V_stall_max **2.) * C_Lmax_takeoff 
    W_S_stall_landing = 0.5 * rho_0 * (V_stall_max **2.) * C_Lmax_landing


    ## DESIGN FOR TAKEOFF ##
    W_P_TO = (TOP * C_Lmax_takeoff * sigma) / (W_S * 1.21) #1.21 KIJK IN ADSEE 1 SLIDES LECTURE 3 SLIDE 32 NOTES 

    
    ## DESIGN FOR LANDING ##
    W_S_landing = (C_Lmax_landing * rho_0 * (s_land / 0.5915))/(2. * f)      #0.5915 due to requirements from CS 23


    ## DESIGN FOR CRUISE ##
    W_P_cruise = efficiency_prop * ((rho/rho_0)**(3./4.)) * ((C_D0_clean * 0.5 * V_cruise**3/W_S)+W_S/(np.pi*A*e_clean*0.5*rho*V_cruise))**(-1.)


    ## DESIGN FOR CLIMBRATE ##
    W_P_climbrate = efficiency_prop /(climbrate + ((np.sqrt(W_S)*np.sqrt(2./rho_0))/(1.345*(( A * e_clean )**(3./4.))/(C_D0_clean**(1./4.)))))
    

    ## DESIGN FOR CLIMB GRADIENT ##
    #one could use for V_climbgradient 1.2*V_stall
    V_climbgradient = 1.2* V_stall_max
    CD_climbgradient = C_D0_clean + ((C_Lmax_clean/1.2)**2/(np.pi*A*e_clean))
    
    W_P_climbgradient = efficiency_prop / (np.sqrt(W_S)*((climbrate/V_climbgradient)+(CD_climbgradient/(C_Lmax_clean/1.2))) * np.sqrt(1.2*2./(rho_0*C_Lmax_clean)))

   

    ## Design for Maneuvering performance ##
    W_P_maneuver = ((((C_D0_clean*0.5*rho_0*V_cruise**3.)/W_S) + (W_S*(n_max**2.)/(np.pi*A*e_clean*0.5*rho_0*V_cruise)))/efficiency_prop)**(-1.)


    ## Calculate design point ##
    min_W_S = min(W_S_stall_clean,W_S_stall_takeoff,W_S_stall_landing,W_S_landing)
    Intersect = min( (efficiency_prop /(climbrate + ((np.sqrt(min_W_S)*np.sqrt(2./rho_0))/(1.345*(( A * e_clean )**(3./4.))/(C_D0_clean**(1./4.)))))), ((TOP * C_Lmax_takeoff * sigma) / (min_W_S * 1.21)), ( ((((C_D0_clean*0.5*rho_0*V_cruise**3.)/min_W_S) + (min_W_S*(n_max**2.)/(np.pi*A*e_clean*0.5*rho_0*V_cruise)))/efficiency_prop)**(-1.) ) )

    Wing_S = weight_TO / min_W_S
    P_a = weight_TO / Intersect

    V_stall = np.sqrt((weight_TO*2.)/(Wing_S*rho_0*C_Lmax_clean))
    
    return min_W_S, Intersect, Wing_S, P_a, V_stall
    
    
    
def TD(P_a):

    V = np.arange(6,60.,0.01)

    D = ((0.5 * rho_0 * V**3 * Wing_S * C_D0_clean) + ((weight_TO**2) / (0.5 * rho_0 * Wing_S * V * np.pi * A * e_clean))) / V
    T = P_a / V

    D_min = min(D)
    
    for i in range(len(T)):
        if T[i] - D[i] <= 0.0001:
            T_max = T[i]
    
    #Minimum Drag
    #(CL/CD)_max - (CD/CL)_min
    CL_mindrag = np.sqrt(C_D0_clean/(1./(np.pi * A * e_clean)))
    CD_mindrag = C_D0_clean + (CL_mindrag**2.)/(np.pi * A * e_clean)
    V_mindrag = np.sqrt((weight_TO * 2.)/(rho_0 * Wing_S * CL_mindrag))
    
    return D_min, CL_mindrag, CD_mindrag, V_mindrag, T_max
    
    

def PaPr(P_a):
    
    V = np.arange(4,60.,0.01)

    P_r = (0.5 * rho_0 * V**3. * Wing_S * C_D0_clean) + ((weight_TO**2.) / (0.5 * rho_0 * Wing_S * V * np.pi * A * e_clean))
    P_r_min = min(P_r)
    

    for i in range(len(P_r)):
        if P_a - P_r[i] < 0.01:
            V_max = V[i]
            break
        if i == len(P_r)-1:
            V_max = 0.
            

    
    #Minimum Power Req.
    #(Cl^3/CD^2) max - (CD/CL^(3/2)) min
    CL_minpower = np.sqrt((3. * C_D0_clean) / (1./(np.pi * A * e_clean)))
    CD_minpower = C_D0_clean + (CL_minpower**2.)/(np.pi * A * e_clean)
    V_minpower = np.sqrt((weight_TO * 2.)/(rho_0 * Wing_S * CL_minpower))
    
    P_a_climb = (1.3 * weight_TO) + P_r_min
    RC = (P_a - P_r) / weight_TO
    RC_max = max(RC)
    
    Bat_power = (fl_time/60.)*P_r_min/1000.

    return P_r_min, CL_minpower, CD_minpower, V_minpower, V_max, RC_max, Bat_power, P_a_climb



def weight():
    # [Name,Empty Mass (kg), Pilot weight range (kg) min, max]
    #filter 
    Hang_glider = [["Mars 150", 23.6, 41., 82.],["GTR 148", 30., 54., 100.],["Condor 5+",28. ,60. ,90.],["Fun Air", 32., 60. , 100.],["Atlas 14", 24.5, 50., 75.],["Tropi 16", 34., 50., 110.],["Firebird Classic", 32., 60., 100.],["Kompozit UT",19. ,65. ,95. ],["Dream 165",28.1, 59., 91.]]
    #[Name,Empty,MTOW]
    Sailplanes = [["Akaflieg SB-13", 285., 425.],["Marske Pioneer II", 163., 295.],["Strojnik S-2A", 280., 444.],["Maupin Windrose", 232., 335.],["Maupin Carbon Dragon", 54.5, 136.],["Advanced Aviation Sierra", 70., 181.], ["Marske Monarch", 100., 204.], ["Oskins Bro-23KR", 83.5, 185.5]]
    #[Name, empty, MTOW] 
    Unconventional_HG = [["Ruppert", 54., 164.],["Ariane Swift light", 48., 158.], ["Maupin carbon Dragon", 54.5, 136.],["Rensselaer RP1", 53., 120.],["Ariane Swift engine", 95., 191.],["Hall Vector 1", 68., 154.]]
    
    Hang_glider = np.array(Hang_glider)
    Sailplanes = np.array(Sailplanes)
    Unconventional_HG = np.array(Unconventional_HG)
      
    #Hang gliders
    Hang_X = Hang_glider[:,1].astype(float) + Hang_glider[:,3].astype(float)
    Hang_Y = Hang_glider[:,1].astype(float)
    slope, intersect, r2, p, stderr = sp.linregress(Hang_X, Hang_Y)
    
    Sailplanes
    Sail_X = Sailplanes[:,2].astype(float)
    Sail_Y = Sailplanes[:,1].astype(float)
    slope1,intersect1,r2_1,p_1,stderr1 = sp.linregress(Sail_X,Sail_Y)
    
    #unconventional
    Uncon_X = Unconventional_HG[:,2].astype(float)
    Uncon_Y = Unconventional_HG[:,1].astype(float)
    slope2,intersect2,r2_2,p_2,stderr2 = sp.linregress(Uncon_X,Uncon_Y)
    
    #Combined
    Combined_X = np.concatenate((Hang_X, Uncon_X), axis=0)
    Combined_Y = np.concatenate((Hang_Y, Uncon_Y), axis=0)
    slope3,intersect3,r2_3,p_3,stderr3 = sp.linregress(Combined_X,Combined_Y)
    
    ##Now for the empty weight, we want to have the empty weight as a function of the take-off weight, therefore 
    ##the slope of one of the above has to be used (More reference aircraft can be added if necessary)##
    
    #Since no fuel is used, due to electrical propulsion Wf is equal to zero. Thus, the bresquet equation can be neglected#
    #W_tfo is the trapped fuel/oil in the aircraft, however no fuel can be trapped in the aircraft. However, dust etc. can be included as 'tfo'. Thus, we take the minimum 0.001#
    M_tfo = 0.001 #of W_TO#
    
    W_takeoff_maxHG = (weight_pilot_max + intersect) / (1.-slope-M_tfo)
    W_emptyweight_maxHG = slope * W_takeoff_maxHG + intersect
    
    W_takeoff_maxSail = (weight_pilot_max + intersect1) / (1.-slope1-M_tfo)
    W_emptyweight_maxSail = slope1 * W_takeoff_maxSail + intersect1
    
    W_takeoff_maxUncon = (weight_pilot_max + intersect2) / (1.-slope2-M_tfo)
    W_emptyweight_maxUncon = slope2 * W_takeoff_maxUncon + intersect2
    
    return W_takeoff_maxHG, W_takeoff_maxSail, W_takeoff_maxUncon, W_emptyweight_maxHG, W_emptyweight_maxSail, W_emptyweight_maxUncon



    
for i in range(1):
    
    for j in range(1):
        j = 0
        

        if i == 0:
            from parameters import *
    
        W_takeoff_maxHG, W_takeoff_maxSail, W_takeoff_maxUncon, W_emptyweight_maxHG, W_emptyweight_maxSail, W_emptyweight_maxUncon = weight()
        min_W_S, Intersect, Wing_S, P_a, V_stall = PowerWing()
        P_r_min, CL_minpower, CD_minpower, V_minpower, V_max, climbrate, Bat_power, P_a_climb = PaPr(P_a)
        D_min, CL_mindrag, CD_mindrag, V_mindrag, T_max = TD(P_a) 

       
        if j == 0:   
            
           
            print "\nConcept", concept,":"
            
            if i == 0 or i == 5:
                weight_calc_OEW = W_emptyweight_maxHG
                weight_calc_TO = W_takeoff_maxHG
                print "Hang Glider: "
            elif i == 1 or i == 3:
                weight_calc_OEW = W_emptyweight_maxSail
                weight_calc_TO = W_takeoff_maxSail
                print "Sail Plane: "
            elif i == 2 or i == 4:
                weight_calc_OEW = W_emptyweight_maxUncon
                weight_calc_TO = W_takeoff_maxUncon
                print "Unconventional a/c: "
        
            print "OEW: "+str(round(weight_calc_OEW,4))+" kg"
            print "OEW used: "+str(round(weight_OEW,4))+ " kg"
            print "takeoff weight: "+str(round(weight_calc_TO,4))+" kg"
            print "takeoff weight used: "+str(round(weight_TO/g,4))+" kg\n" 
            
            print "Stall speed: "+str(round(V_stall,4))+" m/s - "+str(round(V_stall*1.94384449,4))+" kts"
            print "Maximum speed: "+str(round(V_max,4))+" m/s - "+str(round(V_max*1.94384449,4))+" kts\n"
            
            print "Wing loading: "+str(round(min_W_S,4))+" N/m2"  
            print "Power loading: "+str(round(Intersect,4))+" N/W"
            print "Wing size: "+str(round(Wing_S,4))+" m2"
#            print "Wing span: "+str(round(np.sqrt(A*Wing_S),4))+" m"
#            print "Wing chord: "+str(round(np.sqrt(A*Wing_S)/A,4))+" m"
            print "Power available: "+str(round(P_a,4))+" W"
            print "Max thrust :", str(round(T_max,4)), "N\n"
                
            print "Minimum power: "
#            print "Optimum CL: "+str(round(CL_minpower,4))+" [-]"
#            print "Optimum CD: "+str(round(CD_minpower,4))+" [-]"
#            print "CL/CD: "+str(round(CL_minpower/CD_minpower,4))+" [-]"
            print "Optimum speed: "+str(round(V_minpower,4))+" m/s - "+str(round(V_minpower*1.94384449,4))+" kts"
            print "Drag: "+str(round(P_r_min/V_minpower,4))+" N"
            print "Power: "+str(round(P_r_min,4))+" W\n"
            
            print "Mimimum drag: "
#            print "Optimum CL: "+str(round(CL_mindrag,4))+" [-]"
#            print "Optimum CD: "+str(round(CD_mindrag,4))+" [-]"
            print "CL/CD: "+str(round(CL_mindrag/CD_mindrag,4))+" [-]"
            print "Optimum speed: "+str(round(V_mindrag,4))+" m/s - "+str(round(V_mindrag*1.94384449,4))+" kts"
            print "Drag: "+str(round(D_min,4))+" N"
            print "Power: "+str(round(D_min*V_mindrag,4))+" W\n"
    
            print "Climb:"
            print "1.3 m/s climbrate: "+str(round(P_a_climb,4))+" W"
            print "Max. climbrate: "+str(round(climbrate,4))+" m/s\n"
            
            print "Battery capacity (30 min. cruise): "+str(round(Bat_power,4))+" kWh"
            print "Battery capacity (4 min. climb): "+str(round(P_a_climb*(4./60.)/1000.,4))+" kWh"
            print "\n------------------------------"
            
            
        if j == 1:
#
            from parameters import *
            
#            A = 1.01 * A   
#            C_D0_clean = 1.01 * C_D0_clean
#            e_clean = 1.01 * e_clean
            C_Lmax_clean = 1.01 * C_Lmax_clean            
            
            
            W_takeoff_maxHG_SENS, W_takeoff_maxSail_SENS, W_takeoff_maxUncon_SENS, W_emptyweight_maxHG_SENS, W_emptyweight_maxSail_SENS, W_emptyweight_maxUncon_SENS = weight()
            min_W_S_SENS, Intersect_SENS, Wing_S_SENS, P_a_SENS, V_stall_SENS = PowerWing()
            P_r_min_SENS, CL_minpower_SENS, CD_minpower_SENS, V_minpower_SENS, V_max_SENS, climbrate_SENS, Bat_power_SENS, P_a_climb_SENS = PaPr(P_a_SENS)
            D_min_SENS, CL_mindrag_SENS, CD_mindrag_SENS, V_mindrag_SENS = TD(P_a_SENS)
        
            
            print "\nConcept "+ str(i+1), concept,":\n"

            print "Stall speed: "+str(round(((V_stall_SENS-V_stall)/V_stall)*100.,2))+" %"
            print "Maximum speed: "+str(round(((V_max_SENS-V_max)/V_max)*100.,2))+" %\n"
            
            print "Wing loading: "+str(round(((min_W_S_SENS-min_W_S)/min_W_S)*100.,2))+" %"  
            print "Wing size: "+str(round(((Wing_S_SENS-Wing_S)/Wing_S)*100.,2))+" %\n"
#            print "Power available: "+str(round((P_a_SENS-P_a)/P_a,4))+" W\n"
                
            print "Minimum power: "
            print "Optimum CL: "+str(round(((CL_minpower_SENS-CL_minpower)/CL_minpower)*100.,2))+" %"
            print "Optimum CD: "+str(round(((CD_minpower_SENS-CD_minpower)/CD_minpower)*100.,2))+" %"
            print "CL/CD: "+str(round((((CL_minpower_SENS/CD_minpower_SENS)-(CL_minpower/CD_minpower))/(CL_minpower/CD_minpower))*100.,2))+" %"
            print "Optimum speed: "+str(round(((V_minpower_SENS-V_minpower)/V_minpower)*100.,2))+" %"
            print "Drag: "+str(round((((P_r_min_SENS/V_minpower_SENS)-(P_r_min/V_minpower))/(P_r_min/V_minpower))*100.,2))+" %"
            print "Power: "+str(round(((P_r_min_SENS-P_r_min)/P_r_min)*100.,2))+" %\n"
            
            print "Mimimum drag: "
            print "Optimum CL: "+str(round(((CL_mindrag_SENS-CL_mindrag)/CL_mindrag)*100.,2))+" %"
            print "Optimum CD: "+str(round(((CD_mindrag_SENS-CD_mindrag)/CD_mindrag)*100.,2))+" %"
            print "CL/CD: "+str(round((((CL_mindrag_SENS/CD_mindrag_SENS)-(CL_mindrag/CD_mindrag))/(CL_mindrag/CD_mindrag))*100.,2))+" %"
            print "Optimum speed: "+str(round(((V_mindrag_SENS-V_mindrag)/V_mindrag)*100.,2))+" %"
            print "Drag: "+str(round(((D_min_SENS-D_min)/D_min)*100.,4))+" %"
            print "Power: "+str(round((((D_min_SENS*V_mindrag_SENS)-(D_min*V_mindrag))/(D_min*V_mindrag))*100.,2))+" %\n"
    
            print "Climb:"
            print "1.3 m/s climbrate: "+str(round(((P_a_climb_SENS-P_a_climb)/P_a_climb)*100.,2))+" %"
            
            print "Battery capacity (30 min. cruise): "+str(round(((Bat_power_SENS-Bat_power)/Bat_power)*100.,2))+" %"
            print "Battery capacity (4 min. climb): "+str(round((((P_a_climb_SENS*(4./60.)/1000.)-(P_a_climb*(4./60.)/1000.))/(P_a_climb*(4./60.)/1000.))*100.,2))+" %"
            print "\n------------------------------"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
