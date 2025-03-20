#So begins the great and terrible ballistics sim. I think that figuring
#out iteration, etc in vacuum is a good place to start.
#I can check against simple kinematics.
import numpy as np
import scipy as sp
#Define constants. This might vary later if I do my multiplanetary idea
#Using metric, not imperial, should build in conversions.
g = 9.81
sm = 636  #Shell mass for an AP Round for 14 inch 45 cal naval gun, kg
mv = 790  #Muzzle velocity for APm m/s
bl = 16   #Barrel length, m
#Starting point. Logically y should be above the ground a bit. Let's
#say one meter. Barrel length at angle will be added.
x = 0
y = 1
z = 0
#Making x direction the ship's bow would be easy, but I think treating
#it as east would be better for this long term. That's to be added
#with the dumaresq stuff later though. To start with, our unfortunate
#battleship is stuck pointing east.

#Let's do input validation. Might be updated to include proper
#elevation angles for ships in the future. Or could be replaced
#entirely if I make a ballistics function with these things as inputs..
goodin = 0
while goodin == 0:
    print('What is your gun elevation, in degrees?')
    el = input()
    try:
        el = int(el)
    except:
        print('Please input a number.')
    else:
        goodin = 1

elr = np.radians(el)

#I want to record data for this, so I can get make pretty charts of it.
#But this compels me to use yet another input validation for traverse
goodin2 = 0
while goodin2 == 0:
    print('What is your gun traverse, in degrees, negative being counterclockwise?')
    tra = input()
    try:
        tra = int(tra)
    except:
        print('Please input a number.')
    else:
        goodin2 = 1

trr = np.radians(tra)

#We multiply barrel length and muzzle belocity by sin(elr) for y values
#but x and z will be cos(trr)*cos(elr) and sin(trr)*cos(elr)
#respectively.
x += np.cos(trr) * np.cos(elr) * bl
y += np.sin(elr) * bl
z += np.sin(trr) * np.cos(elr) * bl
#Add a v before for velocity. Should include boat motion later.
vx = np.cos(trr) * np.cos(elr) * mv
vy = np.sin(elr) * mv
vz = np.sin(trr) * np.cos(elr) * mv
#These can all be put into an array for graphing purposes. Sh because
#it's data about the position of the shell.
time = 0
shdata = [time,x,y,z,vx,vy,vz]
#Make a while loop that ends when y <= 0, to represent striking sea
#or the enemy. I will define step length out here.
step = 0.01
while y > 0:
    #This isn't much of a loop without air resistance, is it? Ha.
    vy -= step*g
    x += step*vx
    y += step*vy
    z += step*vz
    time += step
    nshdata = [time,x,y,z,vx,vy,vz]
    shdata = np.vstack((shdata,nshdata))
    
print('Calculations done! Your shell flew ' + str(round(nshdata[1],2)) + ' meters in the x direction and ' + str(round(nshdata[3],2)) + ' meters in the z direction, taking ' + str(round(time,2)) + ' seconds.')
#This, I think, is a good place to save a simple version as a memo.
#It's not much more than a simple kinematics solver, but it's mine.