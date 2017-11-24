import numpy as np

def rot_mtx_2D( theta ):
    rot_mtx = np.identity(2)
    rot_mtx[0, 0] = np.cos(theta)
    rot_mtx[0, 1] = -np.sin(theta)
    rot_mtx[1, 0] = np.sin(theta)
    rot_mtx[1, 1] = np.cos(theta)
    return rot_mtx

def signedpow(x, p):
    return np.sign(x) * np.power(np.abs(x), p)
