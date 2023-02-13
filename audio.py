import numpy as np
import scipy.signal as sgn
import scipy.io.wavfile as sciwav
import wave


def load(path):

    audiowave = wave.open(path, 'rb')
    params = audiowave.getparams()
    audiowave.close()

    audiorate, data = sciwav.read(path)

    return data, params


def process(srcdata, srcsr, dstsr, dstsecs):
    SRC_SR = srcsr
    DST_SR = dstsr
    SRC_LENGTH = srcdata.shape[0]
    SRC_SECS = SRC_LENGTH/SRC_SR
    DST_LENGTH = int(SRC_SECS*DST_SR) #we don't "time crop" now to keep all data, see below  

    #resample
    if SRC_SR == DST_SR:
        dstdata = srcdata.copy()
    else: #if src has less sr, interpolate. if src has more sr, subsample. scipy signal does both using fourier transform.
        dstdata = sgn.resample(srcdata, DST_LENGTH, domain="time").astype(np.int16) #requires astype:https://gist.github.com/alexjaw/09af24d58ac99e1e4cafba092e063fe3

    #cropping
    SRC_LENGTH = dstdata.shape[0]
    DST_LENGTH = int(dstsr * dstsecs) #we "time crop" now, see above

    if SRC_LENGTH == DST_LENGTH:
        pass
    elif SRC_LENGTH < DST_LENGTH: #padding
        dif = DST_LENGTH - SRC_LENGTH
        difsplit = int(dif/2)
        dstdata = np.pad(dstdata, (difsplit, dif - difsplit)) #pad_width is not difsplit on both sided because of uneven difs
    else: #cropping
        dif = SRC_LENGTH - DST_LENGTH
        difsplit = int(dif/2)
        dstdata = dstdata[difsplit:dif-difsplit] #crop is not difsplit on both sided because of uneven difs
    
    return dstdata