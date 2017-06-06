# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 13:53:19 2017

@author: Frank
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp
import math

from parameters import *


axial_induction = 0.
axial_induction_prime = 0.

C_T = 0.5

A = T /  ( C_T * 0.5 * rho * V_Tcruise ** 2)

C_P = P_a / (0.5 * rho * V_cruise ** 3 * A)

R = np.sqrt(A/np.pi)