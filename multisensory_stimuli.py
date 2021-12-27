#!/usr/bin/env python3



from time import sleep, time
from datetime import datetime
from math import pi, sqrt
import pyaudio
import numpy as np
import concurrent.futures

from flystim.stim_server import launch_stim_server
from flystim.screen import Screen
from flystim.trajectory import Trajectory

from multi_sensory_traj import multisensoryList, loomingEdge


def dir_to_tri_list(dir):


    north_w = 2.956e-2
    side_w = 2.96e-2

    # set coordinates as a function of direction
    if dir == 'w':
       # set screen width and height
       h = 3.10e-2
       pts = [
            ((+0.4850, -0.3450), (-north_w/2, -side_w/2, -h/2)),
            ((+0.4850, -0.6500), (-north_w/2, +side_w/2, -h/2)),
            ((+0.2900, -0.6500), (-north_w/2, +side_w/2, +h/2)),
            ((+0.2900, -0.3450), (-north_w/2, -side_w/2, +h/2))
        ]
    elif dir == 'n':
       # set screen width and height
       h = 3.29e-2
       pts = [
            ((+0.1800, +0.5750), (-north_w/2, +side_w/2, -h/2)),
            ((+0.1800, +0.2850), (+north_w/2, +side_w/2, -h/2)),
            ((-0.0250, +0.2850), (+north_w/2, +side_w/2, +h/2)),
            ((-0.0250, +0.5675), (-north_w/2, +side_w/2, +h/2))
        ]

    elif dir == 'e':
        # set screen width and height
        h = 3.40e-2
        pts = [
            ((-0.1400, -0.3600), (+north_w/2, +side_w/2, -h/2)),
            ((-0.1400, -0.6500), (+north_w/2, -side_w/2, -h/2)),
            ((-0.3450, -0.6500), (+north_w/2, -side_w/2, +h/2)),
            ((-0.3450, -0.3600), (+north_w/2, +side_w/2, +h/2))
        ]
    else:
        raise ValueError('Invalid direction.')

    return Screen.quad_to_tri_list(*pts)

def make_tri_list():
    return dir_to_tri_list('w') + dir_to_tri_list('n') + dir_to_tri_list('e')


def play_stream(stream, samples_int):
    stream.write(samples_int, num_frames=len(samples_int))

def play_vid(manager):
    manager.start_stim()


def main():

    ## set up visual stimulus
    sound = 2 #1 for pure tone stimulus and 2 for pulse train stimulus
    bg = 0.01
    lm = 0.005
    restt = 5 # was 2, 5
    dur = 1 # was 1
    vel = 100 # was 90
    screen = Screen(server_number=1, id=1,fullscreen=True, tri_list=make_tri_list())

    manager = launch_stim_server(screen)
    manager.set_idle_background(bg)

    loomtraj=loomingEdge(cx=80, cy=50, wStart=10, hStart=10, wEnd=10+vel*dur, hEnd=10+vel*dur, T=dur, c=lm)

    
    ## set up auditory stimulus  
    p = pyaudio.PyAudio()
    volumn = 1.0
    # range [0.0, 1.0]
    fs = 44100      # sampling rate, Hz, must be integer
    
    if sound == 2:
        pcycle = 0.016
        ncycle = 0.020
        cycles = 30
        duration = cycles*(pcycle+ncycle)
        ff = 125.0       # sine frequency, Hz, may be float
    
        sigm = pcycle/4
        K = 0.5*sigm**2

        seg = (pcycle+ncycle)*fs
        seg=int(seg)
        t=np.linspace(0, (seg-1)/fs, seg)
        t=t-np.mean(t)
        y=np.exp(-t**2/K)*np.cos(2*np.pi*ff*t)

        samples = np.zeros(seg*cycles)
        for i in range(cycles):
            samples[seg*i:seg*(i+1)]=y
        samples = np.delete(samples,slice(0,int(seg/4)))
        samples = volumn * samples
    
    elif sound == 1:
        duration = 1
        ff = 225.0        # sine frequency, Hz, may be float; was 225
        t=np.linspace(0, duration, int(duration)*fs)
        samples =  volumn * np.sin(2*np.pi*ff*t)

    samples_int=np.floor(samples*2**15).astype(np.int16)



    ## randomized stimulus list
    msi = multisensoryList()
    msi.msilist(T=2000, dur=dur, restt=restt)

    fileName='multisensory'+datetime.now().strftime('%Y%m%d%H%M%S')+'.txt'
    F=open(fileName,'w')
    
    #sleep(200)
    for i in range(msi.rate.__len__()):
        if msi.rate[i]==0:
            F.write(str(msi.rate[i])+','+str(time())+','+'\n') #just before start stimulating
            F.flush()
            sleep(msi.dur[i])
        
        elif msi.rate[i]==1:
            manager.load_stim('MovingPatch', trajectory=loomtraj, background = bg)
            F.write(str(msi.rate[i])+','+str(time())+','+'\n') #just before start stimulating
            F.flush()
            manager.start_stim()
            sleep(msi.dur[i])
            manager.stop_stim()

        elif msi.rate[i]==2:
            stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=fs,
                output=True)

            F.write(str(msi.rate[i])+','+str(time())+','+'\n') #just before start stimulating
            F.flush()
            stream.write(samples_int, num_frames=len(samples_int))
            stream.stop_stream()
            stream.close()


        else:
            manager.load_stim('MovingPatch', trajectory=loomtraj, background = bg)
            stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=fs,
                output=True)

            F.write(str(msi.rate[i])+','+str(time())+','+'\n') #just before start stimulating
            F.flush()
            print(time())
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(play_stream, stream, samples_int)
                #sleep(0.05)
                #print(time())
                executor.submit(play_vid, manager)
                #sleep(0.05)
                #executor.submit(play_stream, stream, samples_int)
                #print(time())
            #print(time())
            #print('n')

            stream.stop_stream()

            stream.close()
            manager.stop_stim()

        sleep(restt)
    
    p.terminate()
    F.close()



if __name__ == '__main__':
    main()
