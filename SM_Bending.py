import numpy as np

#Rectangular spar dimensions (buitenmaten!)
Spar_w_root = 0.2       #[m] Spar width root
Spar_w_tip = 0.1        #[m] Spar width tip
Spar_h_root = 0.15      #[m] Spar height root
Spar_h_tip = 0.1        #[m] Spar height tip
Spar_htc = 2.*10**(-3)  #[m] Spar height thickness constant
Spar_wtc = 2.*10**(-3)  #[m] Spar width thickness constant


#Circular spar dimensions 
Spar_r_root = 0.1       #[m] Spar radius root
Spar_r_tip = Spar_r_root#[m] Spar radius tip
Spar_t_root = 2.*10**(-3)#[m] Spar thickness root
Spar_t_tip = Spar_t_root #[m] Spar thickness tip

#Make a list
##Rectangular
n_sparpoints = 20 #[-]
Spar_w = []
for i in range(n_sparpoints):
    a = (Spar_w_root-Spar_w_tip)/(n_sparpoints-1.)
    Spar_w.append(Spar_w_root-i*a)
Spar_w = np.array(Spar_w)

Spar_h = []
for i in range(n_sparpoints):
    a = (Spar_h_root-Spar_h_tip)/(n_sparpoints-1.)
    Spar_h.append(Spar_h_root-i*a)
Spar_h = np.array(Spar_h)

ones = np.ones(n_sparpoints)
Spar_ht = Spar_htc*ones
Spar_wt = Spar_wtc*ones

##Circular
Spar_r = []
for i in range(n_sparpoints):
    a = (Spar_r_root-Spar_r_tip)/(n_sparpoints)
    Spar_r.append(Spar_r_root-i*a)
Spar_r = np.array(Spar_r)
Spar_t = []
for i in range(n_sparpoints):
    a = (Spar_t_root-Spar_t_tip)/(n_sparpoints)
    Spar_t.append(Spar_t_root-i*a)
Spar_t = np.array(Spar_t)

###Origin in center
##Rectangular
I_xxr = 1/12.*Spar_w*Spar_h**3 - 1/12.*(Spar_w-2.*Spar_wt)*(Spar_h-2.*Spar_ht)**3
I_yyr = 1/12.*Spar_h*Spar_w**3 - 1/12.*(Spar_h-2.*Spar_ht)*(Spar_w-2.*Spar_wt)**3
I_xyr = 0.

##Circle
I_xxc = np.pi/4.*(Spar_r**4-(Spar_r-Spar_t)**4)
I_yyc = I_xxc
I_xyc = 0.

M_x = 5000*ones #[N] Lift (positieve Mx is lift) - UIT MIJN DUIM GEZOGEN
M_y = 1000*ones #[N] Drag (positieve My is drag) - UIT MIJN DUIM GEZOGEN

##Rectangle
Stress_r_list = []
for i in range(4):
    if i ==0:               #Rechtsonder
        xr = Spar_w/2.
        yr = Spar_h/2.
    if i == 1:              #Linksonder
        xr = -Spar_w/2.
        yr = Spar_h/2.
    if i==2:                #Linksboven
        xr = -Spar_w/2.
        yr = -Spar_h/2.
    if i==3:                #Rechtsboven
        xr = Spar_w/2.
        yr = -Spar_h/2.

    Stress_r = ((M_y*I_xxr-M_x*I_xyr)/(I_xxr*I_yyr-I_xyr**2))*xr + ((M_x*I_yyr-M_y*I_xyr)/(I_xxr*I_yyr-I_xyr**2))*yr
    Stress_r_list.append(Stress_r)
    
Stress_r_max = max(max(Stress_r_list[0]),max(Stress_r_list[1]),max(Stress_r_list[2]),max(Stress_r_list[3]))
Stress_r_min = min(min(Stress_r_list[0]),min(Stress_r_list[1]),min(Stress_r_list[2]),min(Stress_r_list[3]))
#Which corner has the highest stress?
if max(Stress_r_list[0]) > max(max(Stress_r_list[1]),max(Stress_r_list[2]),max(Stress_r_list[3])):
    cornermax = 0
if max(Stress_r_list[1]) > max(max(Stress_r_list[0]),max(Stress_r_list[2]),max(Stress_r_list[3])):
    cornermax = 1
if max(Stress_r_list[2]) > max(max(Stress_r_list[1]),max(Stress_r_list[0]),max(Stress_r_list[3])):
    cornermax = 2
if max(Stress_r_list[3]) > max(max(Stress_r_list[1]),max(Stress_r_list[2]),max(Stress_r_list[0])):
    cornermax = 3
#Which corner has the lowest stress?
if min(Stress_r_list[0]) < min(min(Stress_r_list[1]),min(Stress_r_list[2]),min(Stress_r_list[3])):
    cornermin = 0
if min(Stress_r_list[1]) < min(min(Stress_r_list[0]),min(Stress_r_list[2]),min(Stress_r_list[3])):
    cornermin = 1
if min(Stress_r_list[2]) < min(min(Stress_r_list[1]),min(Stress_r_list[0]),min(Stress_r_list[3])):
    cornermin = 2
if min(Stress_r_list[3]) < min(min(Stress_r_list[1]),min(Stress_r_list[2]),min(Stress_r_list[0])):
    cornermin = 3

##Circle
n_circle = 4  #Op hoe veel punten checkt hij de stress in de circle doorsnede?
theta=[]  # Vanaf de x-as clockwise
xc =[]
yc =[]
Stress_c_list = []
Stress_c_maxlistvalue = []
Stress_c_maxlistindex = []
Stress_c_minlistvalue = []
Stress_c_minlistindex = []
for i in range(n_circle):
    deltatheta = 2.*np.pi/n_circle
    thetavalue = i*deltatheta
    theta.append(thetavalue)
    xc_value = (Spar_r*np.cos(thetavalue))
    xc.append(xc_value)
    yc_value = Spar_r*np.sin(thetavalue)
    yc.append(yc_value)
    Stress_c = ((M_y*I_xxc-M_x*I_xyc)/(I_xxc*I_yyc-I_xyc**2))*xc_value + ((M_x*I_yyc-M_y*I_xyc)/(I_xxc*I_yyc-I_xyc**2))*yc_value
    Stress_c_list.append(Stress_c)
    Stress_c_maxlistvalue.append(max(Stress_c))
    Stress_c_maxlistindex.append(np.argmax(Stress_c))
    Stress_c_minlistvalue.append(min(Stress_c))
    Stress_c_minlistindex.append(np.argmin(Stress_c))
Stress_c_max = [max(Stress_c_maxlistvalue), Stress_c_maxlistindex[np.argmax(Stress_c_maxlistvalue)], 
                np.argmax(Stress_c_maxlistvalue)] #[Stress, point along span, point along crossection]
Stress_c_min = [min(Stress_c_minlistvalue), Stress_c_minlistindex[np.argmin(Stress_c_minlistvalue)], np.argmin(Stress_c_minlistvalue)] #[Stress, point along span, point along crossection]
    

    
#Stress-maxc = 










