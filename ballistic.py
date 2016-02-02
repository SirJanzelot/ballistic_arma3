# Ballistischer Rechner für ArmA:3, tested with Python 3.5.1
# Muzzle velocities by SMPCrafter and SirJanzelot
# todo: check(vel_veh), drag, Crosswind, MRSI

import math, sys, numpy as np
	
class CooError(Exception):
	pass

class RngError(Exception):
	pass
	
g= 9.80665
Temp= 273.15 + 20
shell_mass= [0,0,0,0]
drag_coeff= [0,0,0,0] #K_d for 155mm HE at M= 
velVeh= np.array([[70,140,'nan','nan','nan'],[212.5,425,637.5,772.5,'nan'],[153.9,243,388.8,648,810],[153.9,243,388.8,648,810]]).astype(np.float)
maxDist= np.array([[499,1998,4078,'nan','nan'],[4604,18418,41442,73674,'nan'],[2415,6021,15414,42818,66903],[2415,6021,15414,42818,66903]]).astype(np.float)
minDist= np.array([[34,139,284,'nan','nan'],[799,3918,7196,12793,'nan'],[826,2059,5271,14644,22881],[826,2059,5271,14644,22881]]).astype(np.float)
v_c= 1.4*Temp*8.314459

def findTheta(vT,B_x,B_y,B_h,T_x,T_y,T_h):
	alt_diff= T_h - B_h
	t_range= 10*math.sqrt((T_x-B_x)**2 + (T_y-B_y)**2)
	for murot in range(0,len(minDist)):
		if t_range <= maxDist[vT][murot] and t_range >= minDist[vT][murot]:
			f_mode= murot
			v= velVeh[vT][murot]
			break
	highTheta= math.atan((v**2 + math.sqrt(v**4-g*(g*t_range**2 + 2*alt_diff*v*22)))/(g*t_range))
	highWinkelVer= (highTheta*360)/(2*math.pi)
	lowTheta= math.atan((v**2 - math.sqrt(v**4-g*(g*t_range**2 + 2*alt_diff*v*22)))/(g*t_range))
	lowWinkelVer= (lowTheta*360)/(2*math.pi)
	if (T_x - B_x) >= 0:
		grad= 90;
	elif (T_x - B_x) <= 0:
		grad= 270;
	winkelHor= grad - math.atan((T_y-B_y)/(T_x-B_x))*360/(2*math.pi)
	tudlow= t_range/(v*math.cos(lowTheta))
	tudhigh= t_range/(v*math.cos(highTheta))
	print('Vert: low: {:.2f}° high: {:.2f}°\nHor: {:.2f}\nToF: low: {:.1f}s high: {:.1f}s\nUse Mode: {:d}\nRange: {:.0f}m\n'.format(lowWinkelVer,highWinkelVer,winkelHor,tudlow,tudhigh,f_mode+1,t_range))
	#return lowWinkelVer, highWinkelVer, winkelHor, tudlow, tudhigh
	
		
print('WARNING! Make sure to be on an even surface!')
vehType= int(input('1:MK6, 2:M5 MLRS, 3:M4 Scorcher, 4:2S9 Sochor: '))  - 1
while vehType < 0 or vehType >= 4:
	print('Unknwon vehicle type.')
	vehType= int(input('1:MK6, 2:M5 MLRS, 3:M4 Scorcher, 4:2S9 Sochor: ')) - 1

while True:
	try:
		cooB_x, cooB_y, cooB_h= input('Coordinates battery: [xxxx yyyy h]: ').split()
		if len(cooB_x) < 4 or len(cooB_y) < 4:
			raise CooError
		cooB_x, cooB_y, cooB_h= int(cooB_x), int(cooB_y), int(cooB_h)
	except ValueError:
		print('Check your battery coordinates!')
	except CooError:
		print('Check the format of your battery coordinates!')
	else:
		break
	
while True:
	try:
		cooT_x, cooT_y, cooT_h= input('Coordinates target:  [xxxx yyyy h]: ').split()
		if len(cooT_x) < 4 or len(cooT_y) < 4:
			raise CooError
		cooT_x, cooT_y, cooT_h= int(cooT_x), int(cooT_y), int(cooT_h)
		t_range= int(10*math.sqrt((cooT_x-cooB_x)**2 + (cooT_y-cooB_y)**2))
		if not (t_range <= np.nanmax(maxDist[vehType]) and t_range >= np.nanmin(minDist[vehType])):
			raise RngError
	except ValueError:
		print('Check your target coordinates!')
	except CooError:
		print('Check the format of your target coordinates!')
	except RngError:
		print('Target out of Range ({:d}m). Check your coordinates!'.format(t_range))
		sys.exit(0)
	else:
		break

findTheta(vehType, cooB_x, cooB_y, cooB_h, cooT_x, cooT_y, cooT_h)





# ENDE
