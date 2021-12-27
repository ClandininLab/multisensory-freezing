#from flystim.options import OptionParser
#import flystim.stim_server
import random
from flystim.trajectory import RectangleTrajectory, Trajectory
from datetime import datetime




def loomingEdge(cx=0,
             cy=0,
             wStart=1,
             hStart=1,
             wEnd=0,
             hEnd=0,
             T=10,
             c=1.0):
    h=[(0,hStart),(T,hEnd)]
    w=[(0,wStart),(T,wEnd)]
    trajectory=RectangleTrajectory(x=cx,y=cy,w=w,h=h,color=c)

    return trajectory.to_dict()
 



class loomingList:
    def __init__(self):
        self.rate=[]
        self.dur=[]

    def loominglist(self, T=1000, dur=1, restt=5):
        rates=[0, 1]

        N=int(T/(dur+restt))


        for i in range(N):
            self.rate.append(rates[random.randint(0,rates.__len__()-1)])
            self.dur.append(dur)


        return self





class audioList:
    def __init__(self):
        self.rate=[]
        self.dur=[]

    def audlist(self, T=1000, dur=1, restt=3):
        rates=[0, 1]

        N=int(T/(dur+restt))


        for i in range(N):
            self.rate.append(rates[random.randint(0,rates.__len__()-1)])
            self.dur.append(dur)

            #self.rate.append(0)
            #self.dur.append(restt)

        return self



class multisensoryList:
    def __init__(self):
        self.rate=[]
        self.dur=[]

    def msilist(self, T=1200, dur=1, restt=5):
        rates=[0, 0, 1, 2, 3]

        N=int(T/(dur+restt))


        for i in range(N):
            self.rate.append(rates[random.randint(0,rates.__len__()-1)])
            self.dur.append(dur)

            #self.rate.append(0)
            #self.dur.append(restt)

        return self
