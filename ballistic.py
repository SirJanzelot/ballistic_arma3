# Ballistic calculator for  ArmA III, tested with Python 3.5.1
# Muzzle velocities by SMPCrafter and SirJanzelot
# todo: check(vel_veh), Crosswind, MRSI

# version: 0.02
# lchange: 2016-07-18 0917h

import math
import sys
# import tkinter


# Graviational constant:
g= 9.80665

# MK6 Mortar, M5 MLRS, M4 Scorcher, 2S9 Sochor
# Muzzle velocities:
velVeh= [[70, 140, 0, 0, 0],\
         [212.5, 425, 637.5, 772.5, 0],\
         [153.9, 243, 388.8, 648, 810],\
         [153.9, 243, 388.8, 648, 810]]
# Maximum shooting distance:
maxDist= [[499, 1998, 4078, 0, 0],\
          [4604, 18418, 41442, 73674, 0],\
          [2415, 6021, 15414, 42818, 66903],\
          [2415, 6021, 15414, 42818, 66903]]
# Minimal shooting distance:
minDist= [[34, 139, 284, 0, 0],\
          [799, 3918, 7196, 12793, 0],\
          [826, 2059, 5271, 14644, 22881],\
          [826, 2059, 5271, 14644, 22881]]


### Finding the angle of attack
def findTheta(vT, B_x, B_y, B_h, T_x, T_y, T_h):
  alt_diff= T_h - B_h
  t_range= 10*math.sqrt((T_x - B_x)**2 + (T_y - B_y)**2)
  for murot in range(0, len(minDist)):
    if t_range <= maxDist[vT][murot] and t_range >= minDist[vT][murot]:
      f_mode= murot
      v= velVeh[vT][murot]
      break
  highTheta= math.atan((v**2 + math.sqrt(v**4 - g*(g*t_range**2 + 2*alt_diff*v**2)))/(g*t_range))
  highWinkelVer= (highTheta*360)/(2*math.pi)
  if f_mode == 1:
    highWinkelVer= highWInkelVer - 1.58
  lowTheta= math.atan((v**2 - math.sqrt(v**4 - g*(g*t_range**2 + 2*alt_diff*v**2)))/(g*t_range))
  lowWinkelVer= (lowTheta*360)/(2*math.pi)
  if (T_x - B_x) >= 0:
    grad= 90;
  elif (T_x - B_x) <= 0:
    grad= 270;
  winkelHor= grad - math.atan((T_y - B_y)/(T_x - B_x))*360/(2*math.pi)
  tudlow=    t_range/(v*math.cos(lowTheta))
  tudhigh=   t_range/(v*math.cos(highTheta))
  print('Vert: low: {:.2f}° high: {:.2f}°'.format(lowWinkelVer, highWinkelVer))
  print('Hor: {:.2f}\nToF: low: {:.1f}s high: {:.1f}s'.format(winkelHor, tudlow, tudhigh))
  print('Use Mode: {:d}\nRange: {:.0f}m'.format(f_mode+1, t_range*10))

### Checking input coordinates
def chckInpCoo(inStr):
  status= 0
  CooList= inStr.split(' ')
  if len(CooList) == 3:
    for kl in range(len(CooList)):
      strTemp= str(CooList[kl])
      if str.isdecimal(strTemp):
        if (kl == 0 or kl == 1) and len(strTemp) == 4:
          # Coordinates have the correct length
          status= 1
          continue
        elif kl == 2 and len(strTemp) >=1:
          continue
        else: 
          status= 2
          break
      else:
        # Coordinates aren't decimal numbers
        status= 3
        break
  else:
    # Number of Input items wrong
    status= 4
  print('Status: {0}'.format(status))
  return status

### Which Battery type?
print('WARNING! Make sure to be on an even surface!')
while True:
  rwInVeh= input('1:MK6, 2:M5 MLRS, 3:M4 Scorcher, 4:2S9 Sochor: ')
  if(str.isdecimal(rwInVeh)):
    vehType= int(rwInVeh) - 1  # -1 to adjust to pythons array numbering
    if vehType >= 0 and vehType <= 3:
      break
    else:
      print('Check your Input. Vehicle ID not found.')
  else:
    print('Check your Input. Not a Number.')


### Input of Battery Coordinates
while True:
  rawCooSelf= input('Coordinates battery: [xxxx yyyy h]: ')
  status = chckInpCoo(rawCooSelf)
  if status != '1':
    cooB_x, cooB_y, cooB_h= map(int, rawCooSelf.split(' '))
    break
  else:
    print('Error!')
    sys.exit(0)

### Input of Target Coordinates
rechoice= True
while rechoice == True:
  rawCooSelf= input('Coordinates target: [xxxx yyyy h]: ')
  status= chckInpCoo(rawCooSelf)
  if status != '1':
    cooT_x, cooT_y, cooT_h= map(int, rawCooSelf.split(' '))
    t_range= 10*math.sqrt((cooT_x - cooB_x)**2 + (cooT_y - cooB_y)**2)
    print(t_range)
    if t_range <= max(maxDist[vehType]) and t_range >= minDist[vehType][0]:
	  # Calculating angles of attack
      findTheta(vehType, cooB_x, cooB_y, cooB_h, cooT_x, cooT_y, cooT_h)
      rej= input('Next target? y/n ')
      if rej == 'y':
        rechoice = True
      elif rej == 'n':
        rechoice = False
      else:
        print('Error, wrong input')
    else:
      print('Target out of range!')
  else:
    print('Error!')
    sys.exit(0)



# ENDE

