#!/usr/bin/env python3

#!/usr/bin/env python3

# Example client program that walks through all available stimuli.
from math import pi, sqrt
from time import sleep, time
from datetime import datetime

from flystim.stim_server import launch_stim_server
from flystim.screen import Screen
from flystim.trajectory import Trajectory


from multi_sensory_traj import loomingList, loomingEdge #Note: loomingList is for randomizing the stimulus projection, loomingEdge is for designing looming patch with parameters

def dir_to_tri_list(dir):
	
	# this function sets the screens


    north_w = 2.956e-2
    side_w = 2.96e-2

    # set coordinates as a function of direction
    if dir == 'w':
       # set screen width and height
       h = 3.10e-2
       pts = [
            ((+0.4900, -0.3400), (-north_w/2, -side_w/2, -h/2)),
            ((+0.4900, -0.6550), (-north_w/2, +side_w/2, -h/2)),
            ((+0.2850, -0.6550), (-north_w/2, +side_w/2, +h/2)),
            ((+0.2850, -0.3400), (-north_w/2, -side_w/2, +h/2))
        ]
    elif dir == 'n':
       # set screen width and height
       h = 3.29e-2
       pts = [
            ((+0.1850, +0.5800), (-north_w/2, +side_w/2, -h/2)),
            ((+0.1850, +0.2800), (+north_w/2, +side_w/2, -h/2)),
            ((-0.0200, +0.2800), (+north_w/2, +side_w/2, +h/2)),
            ((-0.0200, +0.5800), (-north_w/2, +side_w/2, +h/2))
        ]

    elif dir == 'e':
        # set screen width and height
        h = 3.40e-2
        pts = [
            ((-0.1350, -0.3550), (+north_w/2, +side_w/2, -h/2)),
            ((-0.1350, -0.6550), (+north_w/2, -side_w/2, -h/2)),
            ((-0.3500, -0.6550), (+north_w/2, -side_w/2, +h/2)),
            ((-0.3500, -0.3550), (+north_w/2, +side_w/2, +h/2))
        ]
    else:
        raise ValueError('Invalid direction.')

    return Screen.quad_to_tri_list(*pts)

def make_tri_list():
    return dir_to_tri_list('w') + dir_to_tri_list('n') + dir_to_tri_list('e')

def main():
    bg =1.0  # background brightness
    lm=0.005 # brightness of the looming patch
    screen = Screen(server_number=1, id=1,fullscreen=True, tri_list=make_tri_list())

    manager = launch_stim_server(screen)
    manager.set_idle_background(bg)


    loom = loomingList()
    loom.loominglist(T=600)
    loomtraj=loomingEdge(cx=90, cy=50, wStart=10, hStart=10, wEnd=100, hEnd=100, T=1, c=lm)    
	# cx, cy: center of looming patch; wStart, hStart: width and height of the looming patch when starting
	# wEnd, hEnd: width and height of the looming patch at the end
	# T: length of looming presentation, in seconds
	# c: brightness of the patch

    fileName='looming'+datetime.now().strftime('%Y%m%d%H%M%S')+'.txt' # for saving the time when looming starts
    F=open(fileName,'w')

    for i in range(loom.rate.__len__()):
        print('looping')

        manager.set_idle_background(bg)
        if loom.rate[i]>0: # randomizing the presentation

	        manager.load_stim('MovingPatch', trajectory=loomtraj, background = bg)

        F.write(str(loom.rate[i])+','+str(time())+','+'\n') #write the time in file just before start stimulating
        F.flush()

        manager.start_stim()
        sleep(loom.dur[i])

        manager.stop_stim()
        sleep(5)  # make the screen bright again for 5 seconds
    
    F.close()

if __name__ == '__main__':
    main()
