#Reallybstarts with imports
import numpy
import scipy
#Start with getting own data. Heading starts at north
print('Own speed (knots):')
ov = float(input())
print('Own heading (degrees from north):')
oho = numpy.radians(float(input()))
oh = (90 - oho) % 360
#This particular part has caused me no shortage of headscratching and
#general confusion. This is my note to be absolutely positive about
#angles before doing anything in the future. Coordinate systems, kids.
onv = numpy.sin(oh)*ov
oev = numpy.cos(oh)*ov
aonv = round(numpy.abs(onv),2)
aoev = round(numpy.abs(oev),2)
#Was going to make this a big else if thing but that's silly. Just define a string variable based on values. Two three option elseifs instead of a huge, ugly one
fonv = round(float(onv),2)
if fonv > 0:
    ons = "moving north at " + str(aonv) + " knots"
elif fonv < 0: 
    ons = "moving south at " + str(aonv) + " knots"
else:
    ons = "not moving north-south "

foev = round(float(oev),2)
if foev > 0:
    oes = "moving east at " + str(aoev) + " knots"
elif foev < 0: 
    oes = "moving west at " + str(aoev) + " knots"
else:
    oes = "not moving east-west "

print("Your ship is " + ons + " & " + oes + ".")
#I should make the enemy rangefinding a callable function, early speed determinatiom was basically this done over and over again. (can i add a notepad?)
def enemyrange():
    print("What is your estimate of enemy distance (kilometers)?")
    er = float(input())
    print("What is enemy angle off the bow (degrees)?")
    eh = float(input())
    #Note: put loop here or something, to give user multiple chances?
    print("Port (left) or starboard (right)? Answer 'P' or 'S'.")
    ps = input()
    if ps == "P":
        eh = 360 - eh
    return [er, numpy.radians(eh)]
edata = enemyrange()
#This gives us distance and angle (clockwise starting at our bow) which we can use to get enemy ship location as a point in an our ship centered coordinate system, with positive y axis springing from bow and positive x being starboard. 
#I keep on doing this. this being getting angle off the vertical instead of horizontal.
ecoord = [numpy.sin(edata[1])*edata[0],numpy.cos(edata[1])*edata[0],edata[1]]
#Keep in mind that ecoord might be expanding a lot in the future. It might actually be best to move this all into the function?
tim = 0
ear = numpy.array([["Time Since First Sighting","X Coordinate","Y Coordinate","Heading"],[tim,round(float(ecoord[0]),2),round(float(ecoord[1]),2),float(ecoord[2])]])

print("How long do you wait until your next observation (seconds)?")
tim = int(input()) + tim
#I think including distance moved in that time could be relevant
knot = 1.852/3600
edist = foev*knot*tim
ndist = fonv*knot*tim
andist = round(abs(ndist),2)
aedist = round(abs(edist),2)
if edist > 0:
    emo = "moved east " + str(aedist) + " kilometers."
elif edist < 0: 
    emo = "moved west " + str(aedist) + " kilometers."
else:
    emo = "didn't move east-west."
#Emo for e motion, not the music. But it's funny so keep it in.
if ndist > 0:
    nmo = "moved north " + str(andist) + " kilometers"
elif ndist < 0: 
    nmo = "moved south " + str(andist) + " kilometers"
else:
    nmo = "didn't move north-south "
print("In that time, you " + nmo + " & " + emo)

#From here we can repeat the rangefinding from above
edata = enemyrange()
ecoord = [numpy.sin(edata[1])*edata[0],numpy.cos(edata[1])*edata[0],edata[1]]
ear2 = numpy.array([tim,round(float(ecoord[0]),2),round(float(ecoord[1]),2),float(ecoord[2])])
ear = numpy.vstack([ear,ear2])
#print(ear)
#Next should be getting speed. Should start with taking data from the bottommost two rows of the set (for most recent speed). But we also need enemy heading
#We want range rate and bearing rate. Might be best to do two, actually? Degrees per minute and knots. Either way, range rate will require speed in knots in bearing based coordinate system
recent = ear[-2:,:]
tdiff = float(recent[1,0])-float(recent[0,0])
xdiff = float(recent[1,1])-float(recent[0,1])
ydiff = float(recent[1,2])-float(recent[0,2])
hdiff = float(recent[1,3])-float(recent[0,3])
#hdiff for heading. Still in radians, eww.
xsp = xdiff/tdiff
ysp = ydiff/tdiff
hsp = numpy.degrees(hdiff/tdiff)
#Now we change the coordinate system. Yay. To remind myself: it is
#based on the line between us and enemy ship at time of second
#observation. It is our previously found heading plus degrees from
#east, which is what my current coordinate system is. 
th = oh + float(ear[1,3])
#print("Test, theta is" + str(th))
#Comment above out once I've got this theta thing licked

#th is shorter than theta, I'll be typing it a lot
rot = numpy.array([[numpy.cos(th),-numpy.sin(th)],[numpy.sin(th),numpy.cos(th)]])
speed = numpy.array([[xsp],[ysp]])
newspeed = numpy.dot(rot,speed)
#Before really putting this to bed, I could put the stuff above into strings.
#Realized that trying to fit all the math inside the string portion
#got big and quite clunky. Moving it out. ns for new speed, ks knot speed.
nsx = 1000*round(float(numpy.squeeze(newspeed[0])),)
nsy = 1000*round(float(numpy.squeeze(newspeed[1])),4)
ksx = abs(nsx * 1.94384)
ksy = abs(nsy * 1.94384)
#Each of these can be given a similar treatment to the east/west portion above.
ansx = abs(nsx)
ansy = abs(nsy)
ahsp = abs(hsp)
if nsx > 0:
    rr = str(ansx) + " meters per second or " + str(ksx) + "knots away from you"
elif nsx < 0:
    rr = str(ansx) + " meters per second or " + str(ksx) + "knots toward you"
else:
    rr = "zero"

if nsx > 0:
    br = str(ansx) + " meters per second or " + str(ksx) + "knots port, "
elif nsx < 0:
    br = str(ansx) + " meters per second or " + str(ksx) + "knots starboard, "
else:
    br = "zero knots, "
#degs for degree string
if hsp > 0:
    degs = str(ahsp) + "degrees per second clockwise"
elif hsp < 0:
    degs = str(ahsp) + "degrees per second counterclockwise"
else:
    degs = "zero degrees per second"

print("Enemy range rate is " +  rr  + " and bearing rate is " + br + degs + ".")