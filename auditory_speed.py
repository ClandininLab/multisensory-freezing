#!/usr/bin/env python3

#!/usr/bin/env python3

# Example client program that walks through all available stimuli.

from time import sleep, time
from datetime import datetime
import pyaudio
import numpy as np


from multi_sensory_traj import audioList

def main():
    audio = audioList()
    restt=5
    audio.audlist(T=600, dur=1, restt=restt)
    fileName='audioSpeed'+datetime.now().strftime('%Y%m%d%H%M%S')+'.txt'
    F=open(fileName,'w')
    
    p = pyaudio.PyAudio()
    volume = 1.0
    # range [0.0, 1.0]
    fs = 44100      # sampling rate, Hz, must be integer
    pcycle=0.05*4.4
    ncycle=0.05*4.4
    cycles=10
    duration = cycles*(pcycle+ncycle)
    ff = 225.0        # sine frequency, Hz, may be float
    
    carier = np.sin(2*np.pi*np.arange(fs*duration-1)*ff/fs)
    tunning = np.zeros(int(fs*duration))
    wdur=int(fs*pcycle)
    for i in range(cycles):
        tunning[wdur*i+1:wdur*(i+1)]=np.sin(np.pi*np.arange(wdur-1)/(wdur))
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*ff/fs)).astype(np.float32)
    #samples = (tunning*carier).astype(np.float32)
    
    for i in range(audio.rate.__len__()):
        if audio.rate[i]==0:
            F.write(str(audio.rate[i])+','+str(time())+','+'\n') #just before start stimulating
            F.flush()

            sleep(audio.dur[i])
        
        else:
            stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

            F.write(str(audio.rate[i])+','+str(time())+','+'\n') #just before start stimulating
            F.flush()
            print(time())
            stream.write(volume*samples)
            stream.stop_stream()
            stream.close()

        sleep(restt)
    
    p.terminate()
    F.close()

if __name__ == '__main__':
    main()
